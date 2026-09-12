"""Testes da definicao de caso e da agregacao do painel."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sih_pipeline as sp  # noqa: E402


@pytest.fixture
def amostra():
    return pd.DataFrame({
        "N_AIH": ["1", "2", "3", "4", "5"],
        "MUNIC_RES": ["410690"] * 3 + ["355030"] * 2,
        "MUNIC_MOV": ["410690"] * 3 + ["355030"] * 2,
        "IDADE": [28, 34, 45, 19, 61],
        "COD_IDADE": [4, 4, 4, 4, 4],
        "SEXO": ["1", "1", "2", "1", "1"],
        "DT_INTER": ["20230105", "20230210", "20230311", "20230415", "20230502"],
        "DT_SAIDA": ["20230110", "20230215", "20230316", "20230420", "20230509"],
        "DIAS_PERM": [5, 5, 5, 5, 7],
        "UTI_MES_TO": [0, 3, 0, 0, 0],
        "MORTE": [0, 1, 0, 0, 0],
        "CAR_INT": ["02", "03", "02", "04", "02"],
        # motociclista condutor/transito, motociclista passageiro, ciclista condutor,
        # auto (placebo), fora do escopo
        "DIAG_PRINC": ["V234", "V285", "V134", "V435", "S720"],
        "DIAG_SECUN": ["S720", "S060", "S823", "S320", ""],
        "VAL_TOT": [1200.0, 8400.0, 900.0, 2300.0, 500.0],
        "VAL_SH": [800.0, 6000.0, 600.0, 1500.0, 300.0],
        "VAL_SP": [400.0, 2400.0, 300.0, 800.0, 200.0],
        "CNES": ["1", "2", "3", "4", "5"],
        "ESPEC": ["3"] * 5,
        "PROC_REA": ["1", "2", "3", "4", "5"],
        "RACA_COR": ["1", "2", "3", "4", "5"],
    })


def test_descarta_fora_do_escopo(amostra):
    out = sp.classificar(sp.normalizar(amostra))
    assert len(out) == 4, "S720 nao e causa externa de transporte, deve sair"


def test_grupos(amostra):
    out = sp.classificar(sp.normalizar(amostra)).set_index("DIAG_PRINC")
    assert out.loc["V234", "grupo"] == "motociclista"
    assert out.loc["V134", "grupo"] == "ciclista"
    assert out.loc["V435", "grupo"] == "auto_placebo"


def test_quarto_digito_separa_condutor(amostra):
    out = sp.classificar(sp.normalizar(amostra)).set_index("DIAG_PRINC")
    assert out.loc["V234", "condutor_transito"], ".4 = condutor em transito"
    assert not out.loc["V285", "condutor_transito"], ".5 = passageiro"
    assert out.loc["V285", "em_transito"]


def test_nexo_ocupacional(amostra):
    out = sp.classificar(sp.normalizar(amostra))
    assert out["nexo_ocupacional"].sum() == 2, "CAR_INT 03 e 04"


def test_agregacao_nao_perde_aih(amostra):
    out = sp.classificar(sp.normalizar(amostra))
    painel = sp.agregar(out, "PR", 2023, 1)
    assert painel["internacoes"].sum() == len(out)
