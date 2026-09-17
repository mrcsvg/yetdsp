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

**O evento é a entrada da logística própria, não a do aplicativo.** O iFood
operou como marketplace de 2011 a 2017 — pedido pelo app, entrega pelo motoboy
do restaurante — e só passou a entregar com frota própria em 2018. Remuneração
por corrida, que é a hipótese do projeto, só existe a partir daí. Ver D-020.

`[ ]` Data de início de **operação de frota própria** de cada plataforma em cada
município. Codificação independente por dois codificadores, com cálculo de
concordância (kappa) e protocolo de resolução de divergência documentado antes
de começar. Fontes: releases das empresas, imprensa local, Wayback Machine sobre
páginas de cobertura, registros em junta comercial, prefeituras.

**⚠️ Risco específico deste desenho:** a imprensa local noticia a chegada do
*aplicativo*, não a da frota. "iFood chega a [cidade]" em 2016 é marketplace.
Dois codificadores podem concordar — com kappa alto — sobre o evento errado.
O protocolo precisa de regra explícita para distinguir os dois e de critério de
desempate declarado antes da codificação; kappa alto não protege contra viés
comum aos dois codificadores.

`[ ]` **Saídas também são evento.** Uber Eats saiu do Brasil em março/2022 e a
99Food em 2023. Onde a saída deixou o município sem operação própria, é
tratamento reverso — variação rara e valiosa, a codificar, não a ignorar.

## 5. Especificação

`[ ]` Diferenças em diferenças com adoção escalonada. Estimador de Callaway &
Sant'Anna (2021) como principal, dada a heterogeneidade de timing e a conhecida
inconsistência do TWFE nesse caso. Sun & Abraham como robustez.

- Unidade: município × mês
- Efeitos fixos: município e mês-calendário
- Grupo de comparação: **not-yet-treated** (D-022). Os ~3.900 municípios nunca
  tratados existem, mas são pequenos e rurais por construção — é o porte que
  determina a entrada da plataforma. Compará-los aos tratados compara
  urbanização, não plataforma, e urbanização move motorização, tráfego e oferta
  hospitalar de uma vez. Never-treated volta como robustez, pareado por porte e
  frota; divergência entre os dois é diagnóstico de seleção urbana, não fracasso.
  **Reportar o tamanho do grupo de comparação por coorte**: a saturação encolhe
  o conjunto no fim da janela.
- Erros-padrão: `[ ]` cluster em município; considerar bootstrap wild
- Janela de evento: `[ ]` **O que restringe a escolha.** O denominador de frota
  municipal começa em **julho/2016** (D-015) e o tratamento começa em **2018**
  (D-020) — sobra pré-período, e para os municípios tratados a partir de 2020 ele
  passa de três anos. A restrição que sobra é assimétrica: a janela pré é curta
  para as coortes de 2018–2019 e confortável para as posteriores. Ao escolher,
  declarar se a janela é fixa (e corta as coortes iniciais) ou variável por
  coorte (e a agregação precisa lidar com isso). Ver também o custo de saturação
  no grupo de comparação, acima.

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
