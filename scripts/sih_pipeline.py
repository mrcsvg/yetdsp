#!/usr/bin/env python3
"""
Pipeline SIH/SUS -> painel municipio x mes de internacoes de motociclistas.

Entrypoint fino: a logica esta em `ifode.extract.sih` e `ifode.transform.sih`,
a definicao de caso em `ifode.cid`. Rodar LOCAL -- precisa de rede para
`ftp.datasus.gov.br`.

    pip install -e ".[dev]"
    python scripts/sih_pipeline.py --ufs PR SP BA --inicio 2015-01 --fim 2025-12

Saida:
    data/raw/sih/uf=<UF>/ano=<AAAA>/mes=<MM>/parte.parquet   (AIH filtradas)
    data/painel/painel_municipio_mes.parquet                 (agregado)

NAO TESTADO CONTRA A BASE REAL: o ambiente onde este script foi escrito nao tem
acesso de rede ao DATASUS. Rode primeiro com uma UF e 2 meses e confira o log.
"""

from __future__ import annotations

import argparse
import logging
import sys

import pandas as pd

from ifode.analyze import car_int
from ifode.extract.sih import baixar_mes, meses, salvar_bruto
from ifode.paths import PAINEL, PAINEL_MUNICIPIO_MES, RAW_SIH, garantir
from ifode.transform.sih import agregar, classificar, normalizar

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sih")


def processar(uf: str, ano: int, mes: int, guardar_bruto: bool) -> pd.DataFrame | None:
    """Baixa, classifica e agrega uma competencia. None se nao houver dado."""
    bruto = baixar_mes(uf, ano, mes)
    if bruto is None or bruto.empty:
        return None

    df = classificar(normalizar(bruto))
    log.info("%s %04d-%02d: %d AIH de interesse (de %d)", uf, ano, mes, len(df), len(bruto))
    if df.empty:
        return None
    if guardar_bruto:
        salvar_bruto(df, uf, ano, mes)
    return agregar(df, uf, ano, mes)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--ufs", nargs="+", required=True)
    p.add_argument("--inicio", required=True, help="AAAA-MM")
    p.add_argument("--fim", required=True, help="AAAA-MM")
    p.add_argument(
        "--sem-bruto",
        action="store_true",
        help="nao salvar o nivel individual, so o painel",
    )
    args = p.parse_args(argv)

    garantir(RAW_SIH, PAINEL)

    paineis: list[pd.DataFrame] = []
    falhas: list[str] = []
    for uf in args.ufs:
        for ano, mes in meses(args.inicio, args.fim):
            try:
                parte = processar(uf, ano, mes, guardar_bruto=not args.sem_bruto)
            except Exception as e:  # noqa: BLE001
                log.error("falhou %s %04d-%02d: %s", uf, ano, mes, e)
                falhas.append(f"{uf} {ano:04d}-{mes:02d}")
                continue
            if parte is not None:
                paineis.append(parte)

    if not paineis:
        log.error("nada foi processado")
        return 1

    painel = pd.concat(paineis, ignore_index=True)
    painel.to_parquet(PAINEL_MUNICIPIO_MES, index=False)
    log.info(
        "painel salvo em %s: %d linhas, %d municipios",
        PAINEL_MUNICIPIO_MES,
        len(painel),
        painel["municipio_res"].nunique(),
    )
    if falhas:
        log.warning("%d competencias falharam: %s", len(falhas), ", ".join(falhas))

    # Diagnostico que interessa antes de qualquer estimacao (D-008).
    print("\n=== Preenchimento do CAR_INT e nexo ocupacional ===")
    print("pct_nexo tem o preenchimento como denominador, nao o total de internacoes.\n")
    print(car_int.por_ano(painel).round(2).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
