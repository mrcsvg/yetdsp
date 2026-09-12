# Dicionário do painel município × mês

Gerado por `scripts/sih_pipeline.py`. Uma linha por município de residência ×
ano × mês × grupo de vítima.

| Campo | Tipo | Descrição |
|---|---|---|
| `uf` | str | UF do arquivo SIH de origem |
| `ano`, `mes` | int | Competência |
| `municipio_res` | str | Código IBGE de 6 dígitos do município de residência (`MUNIC_RES`) |
| `grupo` | str | `motociclista` (V20–V29), `ciclista` (V10–V19), `auto_placebo` (V40–V49) |
| `internacoes` | int | AIH no grupo |
| `internacoes_condutor` | int | Quarto dígito do CID = condutor em acidente de trânsito |
| `internacoes_transito` | int | Quarto dígito indicando acidente de trânsito |
| `homens` | int | `SEXO` = 1 |
| `idade_media` | float | Média de idade em anos completos |
| `faixa_18_39` | int | Internações na faixa de 18 a 39 anos |
| `dias_perm_total` | int | Soma de `DIAS_PERM` |
| `internacoes_uti` | int | `UTI_MES_TO` > 0 |
| `obitos` | int | `MORTE` = 1 (óbito hospitalar; não captura óbito pré-hospitalar — ver SIM) |
| `val_tot` | float | Soma de `VAL_TOT` em reais nominais. **Deflacionar antes de usar.** Valor pago pelo SUS, não custo econômico |
| `nexo_ocupacional` | int | `CAR_INT` em {03, 04} |
| `car_int_preenchido` | int | `CAR_INT` não nulo — denominador da taxa de preenchimento |

## Advertências

- `municipio_res` ≠ município do acidente. Em região metropolitana a divergência
  é material.
- `val_tot` é limite inferior do custo. Não inclui pré-hospitalar, reabilitação,
  perda de produção nem custo material.
- A taxa de nexo ocupacional deve sempre ser reportada com
  `nexo_ocupacional / car_int_preenchido`, nunca sobre `internacoes`.
