#!/usr/bin/env python3
"""
Pipeline SIH/SUS -> painel municipio x mes de internacoes de motociclistas e ciclistas.

Rodar LOCAL (precisa de rede para ftp.datasus.gov.br).

    pip install "pysus>=0.15" pandas pyarrow duckdb

    python sih_pipeline.py --ufs PR SP BA --inicio 2015-01 --fim 2025-12

Saida:
    data/raw/sih/uf=<UF>/ano=<AAAA>/mes=<MM>/parte.parquet   (AIH filtradas, nivel individual)
    data/painel/painel_municipio_mes.parquet                 (agregado)

NAO TESTADO CONTRA A BASE REAL: o ambiente onde este script foi escrito nao tem
acesso de rede ao DATASUS. Rode primeiro com uma UF e 2 meses e confira o log.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sih")

RAW = Path("data/raw/sih")
OUT = Path("data/painel")

# ---------------------------------------------------------------------------
# Definicao de caso (CID-10, capitulo XX - causas externas de morbidade)
# ---------------------------------------------------------------------------
# O quarto digito das categorias V10-V29 separa condutor/passageiro e
# transito/nao-transito:
#   .0 condutor, acidente NAO de transito      .4 condutor, acidente de transito
#   .1 passageiro, nao de transito             .5 passageiro, acidente de transito
#   .2 nao especificado, nao de transito       .9 nao especificado, de transito
#   .3 ao embarcar ou desembarcar
# V19 e V29 tem estrutura propria (colisao com outro veiculo / nao especificado).

GRUPOS_CID = {
    "ciclista": [f"V{n:02d}" for n in range(10, 20)],    # V10-V19
    "motociclista": [f"V{n:02d}" for n in range(20, 30)],  # V20-V29
    "auto_placebo": [f"V{n:02d}" for n in range(40, 50)],  # V40-V49 (controle)
}

CONDUTOR_TRANSITO = {"4"}          # quarto digito = condutor em acidente de transito
TRANSITO = {"3", "4", "5", "6", "7", "8", "9"}

# Caracter da internacao (campo CAR_INT do arquivo RD).
# CONFERIR contra a "Estrutura dos arquivos SIHSUS - RD" da sua competencia:
# a tabela de dominio mudou de versao ao longo da serie.
CAR_INT_LABEL = {
    "01": "eletivo",
    "02": "urgencia",
    "03": "acid_local_trabalho",
    "04": "acid_trajeto_trabalho",
    "05": "outro_acid_transito",
    "06": "outra_lesao_envenenamento",
}
CAR_INT_OCUPACIONAL = {"03", "04"}

COLS = [
    "N_AIH", "MUNIC_RES", "MUNIC_MOV", "NASC", "IDADE", "COD_IDADE", "SEXO",
    "DT_INTER", "DT_SAIDA", "DIAS_PERM", "UTI_MES_TO", "MORTE", "CAR_INT",
    "DIAG_PRINC", "DIAG_SECUN", "VAL_TOT", "VAL_SH", "VAL_SP", "CNES",
    "ESPEC", "PROC_REA", "RACA_COR",
]


# ---------------------------------------------------------------------------
def meses(inicio: str, fim: str) -> list[tuple[int, int]]:
    per = pd.period_range(inicio, fim, freq="M")
    return [(p.year, p.month) for p in per]


def baixar_mes(uf: str, ano: int, mes: int) -> pd.DataFrame | None:
    """Baixa um arquivo RD<UF><AAMM>.dbc e devolve o DataFrame bruto."""
    from pysus.ftp.databases.sih import SIH

    sih = SIH().load()
    arquivos = sih.get_files("RD", uf=uf, year=ano, month=mes)
    if not arquivos:
        log.warning("sem arquivo RD para %s %04d-%02d", uf, ano, mes)
        return None

    destinos = sih.download(arquivos, local_dir=str(RAW / "_tmp"))
    if not isinstance(destinos, list):
        destinos = [destinos]

    quadros = [d.to_dataframe() if hasattr(d, "to_dataframe") else pd.read_parquet(d)
               for d in destinos]
    return pd.concat(quadros, ignore_index=True) if quadros else None


def normalizar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.upper().strip() for c in df.columns]

    faltando = [c for c in COLS if c not in df.columns]
    if faltando:
        log.warning("colunas ausentes nesta competencia: %s", faltando)
    df = df[[c for c in COLS if c in df.columns]]

    for c in ("MUNIC_RES", "MUNIC_MOV", "DIAG_PRINC", "DIAG_SECUN", "CAR_INT",
              "SEXO", "CNES", "PROC_REA"):
        if c in df:
            df[c] = df[c].astype("string").str.strip()

    for c in ("DIAS_PERM", "UTI_MES_TO", "IDADE", "MORTE"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    for c in ("VAL_TOT", "VAL_SH", "VAL_SP"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    for c in ("DT_INTER", "DT_SAIDA"):
        if c in df:
            df[c] = pd.to_datetime(df[c], format="%Y%m%d", errors="coerce")

    # idade em anos: COD_IDADE 4 = anos, 3 = meses, 2 = dias, 1 = horas
    if "COD_IDADE" in df and "IDADE" in df:
        cod = pd.to_numeric(df["COD_IDADE"], errors="coerce")
        df["idade_anos"] = df["IDADE"].where(cod == 4, 0)
    else:
        df["idade_anos"] = df.get("IDADE")

    return df


def classificar(df: pd.DataFrame) -> pd.DataFrame:
    """Marca grupo de vitima, se e condutor em transito, e o nexo ocupacional."""
    df = df.copy()
    cid = df["DIAG_PRINC"].fillna("")
    cat3 = cid.str[:3]
    dig4 = cid.str[3:4]

    df["grupo"] = pd.NA
    for nome, categorias in GRUPOS_CID.items():
        df.loc[cat3.isin(categorias), "grupo"] = nome

    df["condutor_transito"] = dig4.isin(CONDUTOR_TRANSITO)
    df["em_transito"] = dig4.isin(TRANSITO)

    df["car_int_label"] = df["CAR_INT"].map(CAR_INT_LABEL).fillna("desconhecido")
    df["nexo_ocupacional"] = df["CAR_INT"].isin(CAR_INT_OCUPACIONAL)

    df["uti"] = df.get("UTI_MES_TO", 0).fillna(0) > 0
    df["obito"] = df.get("MORTE", 0).fillna(0) == 1
    return df.dropna(subset=["grupo"])


def salvar_bruto(df: pd.DataFrame, uf: str, ano: int, mes: int) -> None:
    destino = RAW / f"uf={uf}" / f"ano={ano}" / f"mes={mes:02d}"
    destino.mkdir(parents=True, exist_ok=True)
    df.to_parquet(destino / "parte.parquet", index=False)


def agregar(df: pd.DataFrame, uf: str, ano: int, mes: int) -> pd.DataFrame:
    df = df.assign(uf=uf, ano=ano, mes=mes)
    g = df.groupby(["uf", "ano", "mes", "MUNIC_RES", "grupo"], dropna=False)
    painel = g.agg(
        internacoes=("N_AIH", "count"),
        internacoes_condutor=("condutor_transito", "sum"),
        internacoes_transito=("em_transito", "sum"),
        homens=("SEXO", lambda s: (s == "1").sum()),
        idade_media=("idade_anos", "mean"),
        faixa_18_39=("idade_anos", lambda s: s.between(18, 39).sum()),
        dias_perm_total=("DIAS_PERM", "sum"),
        internacoes_uti=("uti", "sum"),
        obitos=("obito", "sum"),
        val_tot=("VAL_TOT", "sum"),
        nexo_ocupacional=("nexo_ocupacional", "sum"),
        car_int_preenchido=("CAR_INT", lambda s: s.notna().sum()),
    ).reset_index()
    return painel.rename(columns={"MUNIC_RES": "municipio_res"})


# ---------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ufs", nargs="+", required=True)
    p.add_argument("--inicio", required=True, help="AAAA-MM")
    p.add_argument("--fim", required=True, help="AAAA-MM")
    p.add_argument("--sem-bruto", action="store_true",
                   help="nao salvar o nivel individual, so o painel")
    args = p.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    paineis: list[pd.DataFrame] = []
    for uf in args.ufs:
        for ano, mes in meses(args.inicio, args.fim):
            try:
                bruto = baixar_mes(uf, ano, mes)
                if bruto is None or bruto.empty:
                    continue
                df = classificar(normalizar(bruto))
                log.info("%s %04d-%02d: %d AIH de interesse (de %d)",
                         uf, ano, mes, len(df), len(bruto))
                if not args.sem_bruto:
                    salvar_bruto(df, uf, ano, mes)
                paineis.append(agregar(df, uf, ano, mes))
            except Exception as e:  # noqa: BLE001
                log.error("falhou %s %04d-%02d: %s", uf, ano, mes, e)

    if not paineis:
        log.error("nada foi processado")
        return

    painel = pd.concat(paineis, ignore_index=True)
    painel.to_parquet(OUT / "painel_municipio_mes.parquet", index=False)
    log.info("painel salvo: %d linhas, %d municipios",
             len(painel), painel["municipio_res"].nunique())

    # diagnostico que interessa antes de qualquer estimacao
    diag = (painel.groupby(["ano", "grupo"])
            .agg(internacoes=("internacoes", "sum"),
                 nexo_ocupacional=("nexo_ocupacional", "sum"))
            .assign(pct_nexo=lambda d: 100 * d.nexo_ocupacional / d.internacoes))
    print("\n=== Preenchimento do nexo ocupacional (CAR_INT 03/04) ===")
    print(diag.round(2).to_string())


if __name__ == "__main__":
    main()
