.PHONY: help setup painel diagnostico denominadores custo lint test limpar

PYTHON ?= python

UFS   ?= PR SP BA
INI   ?= 2015-01
# frota municipal so existe a partir de 2016-07 (D-015)
DEN_INI ?= 2016-07
FIM   ?= 2025-12

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "  \033[36m%-14s\033[0m %s\n",$$1,$$2}'

setup: ## instala o pacote em modo editavel com deps de dev
	$(PYTHON) -m pip install -e ".[dev]" && pre-commit install

painel: ## baixa SIH e monta o painel municipio x mes
	$(PYTHON) scripts/sih_pipeline.py --ufs $(UFS) --inicio $(INI) --fim $(FIM)

diagnostico: ## preenchimento do CAR_INT por ano (roda so com o painel ja pronto)
	$(PYTHON) scripts/diagnostico_car_int.py

denominadores: ## frota de moto (Senatran) e populacao (IBGE) -- so precisa de HTTPS
	$(PYTHON) scripts/denominadores.py --inicio $(DEN_INI) --fim $(FIM)

custo: ## val_tot deflacionado (IPCA) e custo social (Ipea) por ano e UF -- so baixa o IPCA
	$(PYTHON) scripts/custo.py

lint:
	ruff check . && ruff format --check .

test:
	$(PYTHON) -m pytest -q

limpar: ## remove intermediarios, preserva data/raw
	rm -rf data/interim/* data/painel/* output/tabelas/* output/figuras/*
