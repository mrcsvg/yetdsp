# iFode

Remuneração por peça em plataformas de entrega e internações de motociclistas no SUS: carga, custo público e identificação causal.

**Status:** em construção. Nada aqui foi submetido, revisado ou publicado.

---

## A pergunta

A remuneração por corrida cria incentivo à velocidade e ao volume. A hipótese é que a entrada e o adensamento de plataformas de entrega em um município elevam a incidência de internações de motociclistas por acidente de transporte, e que esse custo é absorvido pelo SUS sem contrapartida.

A dificuldade central é que **o trabalhador de plataforma não é registrado em nenhuma base administrativa como tal.** Nenhum registro público liga uma internação a uma plataforma específica. Isso torna o desenho necessariamente ecológico: tratamento no nível do município, desfecho no total de motociclistas internados. O coeficiente estimado é, por construção, um piso — ele dilui o efeito sobre entregadores no universo de todos os motociclistas.

## Os dois produtos

| | Escopo | Afirmação | Dependências |
|---|---|---|---|
| **V1 — descritivo** | Carga e custo das internações de motociclistas no SUS, série municipal | Nenhuma causal | SIH, SIM, frota RENAVAM, população IBGE |
| **V2 — causal** | Efeito da entrada de plataforma sobre incidência | Diferenças em diferenças com adoção escalonada | V1 + cronologia de entrada por município |

O V1 não é piloto descartável: todo artefato que ele produz é insumo do V2. O critério de inclusão no V1 é esse — se não reaparece no paper causal como tabela, figura ou input, não entra agora.

## Definição de caso

CID-10, capítulo XX. O quarto dígito das categorias V10–V29 separa condutor de passageiro e trânsito de não-trânsito.

| Grupo | CID-10 | Papel |
|---|---|---|
| Motociclista | V20–V29 | Desfecho principal |
| Ciclista | V10–V19 | Teste do mecanismo — entrega por bike não entra em frota nova |
| Ocupante de automóvel | V40–V49 | Placebo — se o efeito aparecer aqui, é tendência geral de trânsito |

Denominador de moto: frota RENAVAM municipal. **Bicicleta não tem denominador** — não é veículo automotor, não registra. Roda em contagem bruta com efeito fixo de município.

## Estrutura

```
docs/          pré-projeto, inventário de fontes, dicionário do painel, decisões
docs/pre-registro/   plano de análise (depositar no OSF antes de cruzar tratamento × desfecho)
src/ifode/     pacote: extract / transform / analyze
scripts/       entrypoints executáveis
data/          NÃO VERSIONADO — ver docs/fontes-de-dados.md para reconstruir
output/        tabelas e figuras geradas
tests/
```

## Reprodutibilidade

Nenhum dado vive neste repositório. Todas as fontes são públicas e baixáveis; o inventário em `docs/anexo-a-inventario-fontes-de-dados.md` traz órgão, granularidade, cobertura temporal, formato, dicionário e latência de cada uma.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make painel        # baixa SIH e monta o painel município × mês
make diagnostico   # preenchimento do CAR_INT por ano
```

## Duas regras do projeto

**Nada de microdado no git.** Nem SIH, nem SIM, nem Parquet intermediário. O `.gitignore` cobre isso, mas a regra é anterior ao arquivo: o repositório carrega o código que reconstrói os dados, não os dados.

**O pré-registro vem antes do cruzamento.** Olhar a distribuição descritiva do SIH é livre. Cruzar cronologia de entrada de plataforma com internação, mesmo num gráfico exploratório, exige que o plano de análise já esteja depositado e com timestamp. Depois disso, especificação nova é análise exploratória declarada.

## Licença

Código sob MIT (`LICENSE`). Texto, figuras e documentação sob CC BY 4.0 (`LICENSE-docs`).
