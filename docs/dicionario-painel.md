# Dicionário do painel município × mês

Gerado por `scripts/sih_pipeline.py`. Uma linha por município de residência ×
ano × mês × grupo de vítima.

| Campo | Tipo | Descrição |
|---|---|---|
| `uf` | str | UF do arquivo SIH de origem |
| `ano`, `mes` | int | Competência |
| `municipio_res` | str | Código IBGE de 6 dígitos do município de residência (`MUNIC_RES`) |
| `grupo` | str | `motociclista` (V20–V29), `ciclista` (V10–V19), `auto_placebo` (V40–V49) |
| `internacoes` | int | AIH no grupo, **inclusive as de não-trânsito** — o filtro de trânsito é do desfecho, não da inclusão no painel |
| `internacoes_condutor` | int | Quarto dígito `.4` — condutor em acidente de trânsito. Vale nas duas estruturas |
| `internacoes_transito` | int | Quarto dígito indicando acidente de trânsito, **lido conforme a estrutura da categoria** (D-010) |
| `internacoes_embarque` | int | Subconjunto de `internacoes_transito`: `.3` da estrutura padrão (embarque/desembarque). Isolado para análise de sensibilidade — ver D-010 |
| `homens` | int | `SEXO` = 1 |
| `idade_media` | float | Média de idade em anos completos |
| `faixa_18_39` | int | Internações na faixa de 18 a 39 anos |
| `dias_perm_total` | int | Soma de `DIAS_PERM` |
| `internacoes_uti` | int | `UTI_MES_TO` > 0 |
| `obitos` | int | `MORTE` = 1 (óbito hospitalar; não captura óbito pré-hospitalar — ver SIM) |
| `val_tot` | float | Soma de `VAL_TOT` em reais nominais. **Deflacionar antes de usar.** Valor pago pelo SUS, não custo econômico |
| `nexo_ocupacional` | int | `CAR_INT` em {03, 04} |
| `car_int_preenchido` | int | `CAR_INT` com código do domínio (`01`–`06`). Branco e as sentinelas `00`/`99` **não** contam — ver D-011 |

## Leitura do quarto dígito

`internacoes_transito` não sai de uma regra única sobre o quarto dígito. As
categorias terminais — **V19, V29, V49** — reaproveitam `.3`, `.6` e `.8` com
outro sentido, e `.3` ali é acidente **não** de trânsito. A tabela completa está
em D-010 no log de decisões e a implementação em `src/ifode/cid.py`, num lugar
só. V29 é categoria de alto volume no SIH: tratar as duas estruturas como uma
infla o desfecho.

## As duas taxas do `CAR_INT`

Não se confundem, e a segunda é a que responde à H4:

| Taxa | Fórmula |
|---|---|
| Preenchimento | `car_int_preenchido / internacoes` |
| Nexo ocupacional | `nexo_ocupacional / car_int_preenchido` |

O denominador do nexo é o preenchimento, **nunca** `internacoes`. Dividir por
`internacoes` mistura duas coisas distintas — o campo estar vazio e o campo
dizer "não foi trabalho" — e faz a subnotificação parecer menor do que é.
Ambas saem prontas de `ifode.analyze.car_int` e de `make diagnostico`.

## Advertências

- `municipio_res` ≠ município do acidente. Em região metropolitana a divergência
  é material.
- `val_tot` é limite inferior do custo. Não inclui pré-hospitalar, reabilitação,
  perda de produção nem custo material.
- `idade_media` trata menor de um ano (`COD_IDADE` ≠ 4) como 0. Não afeta a
  faixa de interesse do projeto, mas afeta a média.
