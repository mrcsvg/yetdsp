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

CID-10, capítulo XX. Duas coisas que parecem detalhe e não são:

**O código V não está no diagnóstico principal.** A norma do SIH põe a lesão (capítulo XIX, S/T) no principal e a causa externa no secundário. Filtrar `DIAG_PRINC` devolve zero AIH em todo ano da série — o filtro varre `DIAG_SECUN` → `DIAGSEC1..9` → `DIAG_PRINC` (D-017).

**O quarto dígito não tem a mesma tabela em todas as categorias.** As terminais (V19, V29, V49) reaproveitam `.3`, `.6` e `.8` com outro sentido, e `.3` ali é acidente *não* de trânsito. V29 sozinha é 67% do desfecho, então isso move 6,3% dos casos (D-010). Implementação em `src/ifode/cid.py`.

| Grupo | CID-10 | Papel |
|---|---|---|
| Motociclista | V20–V29 | Desfecho principal |
| Ciclista | V10–V19 | Teste do mecanismo — entrega por bike não entra em frota nova |
| Ocupante de automóvel | V40–V49 | Placebo — se o efeito aparecer aqui, é tendência geral de trânsito |

Denominador de moto: frota RENAVAM municipal. **Bicicleta não tem denominador** — não é veículo automotor, não registra. Roda em contagem bruta com efeito fixo de município.

## Estrutura

```
docs/                pré-projeto, inventário de fontes, dicionário do painel, decisões
docs/pre-registro/   plano de análise (depositar no OSF antes de cruzar tratamento × desfecho)
src/ifode/cid.py     definição de caso: grupos CID-10 e leitura do quarto dígito
src/ifode/frota.py   tipos de veículo do RENAVAM que correspondem a V20–V29
src/ifode/municipios.py  ponte nome ↔ código IBGE, com a tabela de apelidos revisada
src/ifode/extract/   download das fontes — única camada que toca a rede
                     (sih.py = FTP DATASUS; bigquery.py = espelho Base dos Dados)
src/ifode/transform/ limpeza, classificação e agregação do painel
src/ifode/analyze/   diagnóstico e estimação
scripts/             entrypoints executáveis (argumento, I/O e log — sem regra)
data/                NÃO VERSIONADO — ver docs/anexo-a-inventario-fontes-de-dados.md
output/              tabelas e figuras geradas
tests/
```

A definição de caso mora em `src/ifode/cid.py`, sozinha, sem pandas e sem rede.
É o artefato que um revisor precisa conseguir ler inteiro sem abrir o pipeline —
e o único lugar onde a regra existe.

## Reprodutibilidade

Nenhum dado vive neste repositório. Todas as fontes são públicas e baixáveis; o inventário em `docs/anexo-a-inventario-fontes-de-dados.md` traz órgão, granularidade, cobertura temporal, formato, dicionário e latência de cada uma.

```bash
python -m venv .venv && source .venv/bin/activate
make setup         # instala o pacote em modo editável + pre-commit
make test          # roda sem rede e sem dado — a definição de caso é testável isolada
make painel        # baixa SIH e monta o painel município × mês  (precisa de FTP do DATASUS)
make diagnostico   # preenchimento do CAR_INT por ano, UF e município
make denominadores # frota de moto (Senatran) e população (IBGE) — só HTTPS
```

`make diagnostico` lê o painel já montado e escreve `car_int_por_ano.csv`,
`car_int_por_uf_ano.csv` e `car_int_por_municipio.csv` em `output/tabelas/`.

Os alvos passam pelo interpretador ativo (`$(PYTHON)`, padrão `python`). Para
apontar outro: `make test PYTHON=python3.11`.

## Duas regras do projeto

**Nada de microdado no git.** Nem SIH, nem SIM, nem Parquet intermediário. O `.gitignore` cobre isso, mas a regra é anterior ao arquivo: o repositório carrega o código que reconstrói os dados, não os dados.

**O pré-registro vem antes do cruzamento.** Olhar a distribuição descritiva do SIH é livre. Cruzar cronologia de entrada de plataforma com internação, mesmo num gráfico exploratório, exige que o plano de análise já esteja depositado e com timestamp. Depois disso, especificação nova é análise exploratória declarada.

## Licença

Código sob MIT (`LICENSE`). Texto, figuras e documentação sob CC BY 4.0 (`LICENSE-docs`).
