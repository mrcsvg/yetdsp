"""Download dos arquivos RD do SIH/SUS via PySUS.

Unico modulo do pacote que toca a rede. Exige acesso a `ftp.datasus.gov.br`.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

from ifode.paths import RAW_SIH

log = logging.getLogger("ifode.extract.sih")


@lru_cache(maxsize=1)
def _sih():
    """Cliente PySUS do SIH, carregado uma vez por processo.

    O `load()` varre o FTP e e caro; a versao anterior refazia isso a cada
    competencia. Import adiado para que o pacote funcione sem PySUS instalado.
    """
    from pysus.ftp.databases.sih import SIH

    return SIH().load()


def baixar_mes(uf: str, ano: int, mes: int, destino: Path | None = None) -> pd.DataFrame | None:
    """Baixa `RD<UF><AAMM>.dbc` e devolve o DataFrame bruto, ou None se nao houver."""
    sih = _sih()
    arquivos = sih.get_files("RD", uf=uf, year=ano, month=mes)
    if not arquivos:
        log.warning("sem arquivo RD para %s %04d-%02d", uf, ano, mes)
        return None

    destino = destino or (RAW_SIH / "_tmp")
    destino.mkdir(parents=True, exist_ok=True)
    baixados = sih.download(arquivos, local_dir=str(destino))
    if not isinstance(baixados, list):
        baixados = [baixados]

    quadros = [
        d.to_dataframe() if hasattr(d, "to_dataframe") else pd.read_parquet(d) for d in baixados
    ]
    return pd.concat(quadros, ignore_index=True) if quadros else None


def salvar_bruto(df: pd.DataFrame, uf: str, ano: int, mes: int) -> Path:
    """Grava as AIH ja filtradas, particionadas por UF/ano/mes."""
    pasta = RAW_SIH / f"uf={uf}" / f"ano={ano}" / f"mes={mes:02d}"
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / "parte.parquet"
    df.to_parquet(caminho, index=False)
    return caminho


def meses(inicio: str, fim: str) -> list[tuple[int, int]]:
    """Competencias de `AAAA-MM` a `AAAA-MM`, inclusive nas duas pontas."""
    return [(p.year, p.month) for p in pd.period_range(inicio, fim, freq="M")]
