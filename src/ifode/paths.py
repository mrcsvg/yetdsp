"""Caminhos do projeto. Nenhum deles e versionado -- ver D-009 em docs/decisoes.md."""

from __future__ import annotations

from pathlib import Path

#: Raiz do repositorio (src/ifode/paths.py -> src/ifode -> src -> raiz).
RAIZ = Path(__file__).resolve().parents[2]

DATA = RAIZ / "data"
RAW_SIH = DATA / "raw" / "sih"
INTERIM = DATA / "interim"
PAINEL = DATA / "painel"

OUTPUT = RAIZ / "output"
TABELAS = OUTPUT / "tabelas"
FIGURAS = OUTPUT / "figuras"

#: Painel municipio x mes produzido por `scripts/sih_pipeline.py`.
PAINEL_MUNICIPIO_MES = PAINEL / "painel_municipio_mes.parquet"


def garantir(*caminhos: Path) -> None:
    """Cria os diretorios passados, se ainda nao existirem."""
    for caminho in caminhos:
        caminho.mkdir(parents=True, exist_ok=True)
