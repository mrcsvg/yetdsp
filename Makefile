.PHONY: help setup painel diagnostico lint test limpar

UFS   ?= PR SP BA
INI   ?= 2015-01
FIM   ?= 2025-12

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "  \033[36m%-14s\033[0m %s\n",$$1,$$2}'

setup: ## instala o pacote em modo editavel com deps de dev
	pip install -e ".[dev]" && pre-commit install

painel: ## baixa SIH e monta o painel municipio x mes
	python scripts/sih_pipeline.py --ufs $(UFS) --inicio $(INI) --fim $(FIM)

diagnostico: ## preenchimento do CAR_INT por ano (roda so com o painel ja pronto)
	python scripts/diagnostico_car_int.py

lint:
	ruff check . && ruff format --check .

test:
	pytest -q

limpar: ## remove intermediarios, preserva data/raw
	rm -rf data/interim/* data/painel/* output/tabelas/* output/figuras/*
