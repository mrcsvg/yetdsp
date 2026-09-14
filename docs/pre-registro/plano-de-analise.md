# Plano de análise — pré-registro

> **Não depositar ainda.** Este arquivo é o esqueleto. Preencher as seções marcadas
> com `[ ]` e só então depositar no OSF. Depois do depósito, este arquivo fica
> congelado — qualquer mudança vai para `docs/decisoes.md` como análise exploratória
> declarada.

## 1. Pergunta e hipóteses

- **H1** — a entrada de plataforma de entrega em um município eleva a incidência
  de internações de motociclistas por acidente de transporte.
- **H2** — o efeito é crescente na intensidade de operação. `[ ]` **Parcialmente
  identificada**: volume de pedidos por município é dado privado. Declarar o proxy
  usado e o sinal esperado do viés.
- **H3** — `[ ]`
- **H4** — o nexo ocupacional é sistematicamente subregistrado no SIH.

## 2. Dados

Ver `docs/anexo-a-inventario-fontes-de-dados.md`. Fontes da estimação principal:
SIH/SUS (desfecho), RENAVAM (denominador), IBGE (população), cronologia de entrada
por município (tratamento, construída — ver seção 4).

## 3. Definição de caso

| Grupo | CID-10 | Papel |
|---|---|---|
| Motociclista | V20–V29, quarto dígito de condutor em trânsito | Desfecho |
| Ciclista | V10–V19 | Teste do mecanismo |
| Ocupante de automóvel | V40–V49 | Placebo |

A leitura do quarto dígito não é uniforme entre as categorias: V19, V29 e V49
usam outra tabela, em que `.3` é acidente **não** de trânsito. A regra está em
`src/ifode/cid.py` e a justificativa em D-010 (`docs/decisoes.md`).

## 4. Construção do tratamento

`[ ]` Data de início de operação de cada plataforma em cada município.
Codificação independente por dois codificadores, com cálculo de concordância
(kappa) e protocolo de resolução de divergência documentado antes de começar.
Fontes: releases das empresas, imprensa local, Wayback Machine sobre páginas de
cobertura, registros em junta comercial, prefeituras.

## 5. Especificação

`[ ]` Diferenças em diferenças com adoção escalonada. Estimador de Callaway &
Sant'Anna (2021) como principal, dada a heterogeneidade de timing e a conhecida
inconsistência do TWFE nesse caso. Sun & Abraham como robustez.

- Unidade: município × mês
- Efeitos fixos: município e mês-calendário
- Grupo de comparação: `[ ]` not-yet-treated ou never-treated — justificar
- Erros-padrão: `[ ]` cluster em município; considerar bootstrap wild
- Janela de evento: `[ ]`

## 6. Testes pré-declarados de falha do desenho

1. Efeito sobre ocupante de automóvel indistinguível do efeito sobre motociclista
   → desenho captura tendência geral de trânsito.
2. Pré-tendências não paralelas na janela pré-tratamento → reportar e não
   interpretar causalmente.
3. `[ ]`

## 7. Análises exploratórias (declaradas como tais)

- Deslocamento da distribuição horária dos sinistros de moto no RENAEST para as
  faixas de pico de entrega, condicional à existência do campo de hora.
- Preenchimento do `CAR_INT` por ano e por município.

## 8. Desvios

Qualquer desvio deste plano vai para `docs/decisoes.md` com data e motivo.
