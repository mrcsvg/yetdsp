# Pré-projeto — o argumento

> Este documento é a espinha do projeto. Tudo que entra no repositório precisa
> servir a uma das quatro pernas abaixo. Se não serve, não entra — ver D-028.
> O título de trabalho é o do inventário de fontes: **remuneração por peça e
> externalidade fiscal**.

## O objetivo, em uma frase

Enquanto as plataformas de entrega lucram, o trabalho do entregador se
precariza, o motociclista morre ou se acidenta, e a conta chega ao SUS — que
é pago por todos nós. A partir dessa medida, propor políticas públicas que
façam quem lucra pagar pelo risco que cria.

Não é uma tese de método. O desenho causal (V2) existe porque, sem ele, o
argumento cai na primeira objeção: "internação de motociclista cresce desde
2008 por causa da frota, não da plataforma". Mas o desenho é a viga, não a
casa. As últimas semanas construíram a viga (D-020 a D-027) e deixaram as
outras três pernas sem documento. Este arquivo corrige isso.

## As quatro pernas

| # | Afirmação | O que o projeto mede | Fonte | Estado no repositório |
|---|---|---|---|---|
| **P1** | **Eles lucram.** | Receita e lucro operacional das plataformas, ano a ano, como série de contraste ao custo público | Relatórios anuais da Prosus (iFood); relatório de sustentabilidade do iFood; DiDi (99Food) e Meituan (Keeta) reportam segmento | **Ausente.** Nenhuma fonte no inventário até esta versão — ver Bloco 6 do anexo A |
| **P2** | **O trabalho é precário.** | Informalidade, cobertura previdenciária, jornada e renda-hora dos plataformizados | PNAD Contínua, módulo de plataformas (2022, 2024, 2025) | **Só como nota de rodapé** (anexo A, 4.1). Nenhum script, nenhuma tabela |
| **P3** | **Nós pagamos.** | (a) Valor pago pelo SUS, deflacionado, por internação de motociclista, e o custo econômico via parâmetros do Ipea; (b) a lacuna entre o que o SUS interna e o que a Previdência reconhece como acidente de trabalho; (c) quanto disso é atribuível à plataforma | SIH `VAL_TOT`; Ipea TD 2565; INSS benefícios (espécies 31 × 91); o próprio estimador do V2 | **Parcial.** `val_tot` está no painel mas nenhum alvo o usa; a deflação e a camada F6 (custo) não existem; a lacuna SIH × INSS foi tirada da rota crítica em D-002 e nunca voltou |
| **P4** | **Eles morrem ou se acidentam — e o sistema não vê.** | Internações, UTI, óbito hospitalar e pré-hospitalar; e a fração com nexo ocupacional registrado | SIH, SIM, `CAR_INT` | **É o que existe.** D-019: 965.714 internações em 2016–2023, 62 com nexo. Uma em 15.576 |

A perna P3(c) é o V2 inteiro. As outras três são descritivas e **não dependem
do pré-registro** (D-006): olhar receita da Prosus, PNAD e `VAL_TOT` não cruza
tratamento com desfecho. Podem — e devem — andar agora, em paralelo à
cronologia de entrada (F3).

## Ordens de grandeza que o argumento precisa carregar

Números de fora do projeto, para ancorar. Cada um precisa ser recalculado
pelo pipeline antes de virar tabela; aqui servem para dizer qual é o tamanho da
história e o que precisa aparecer lado a lado.

**P1 — lucro.**
- iFood, ano fiscal encerrado em março/2026: receita de US$ 1,87 bilhão, alta
  de 40% em dólar (28% em moeda local, sem aquisições). Maior contribuinte
  individual de receita do grupo Prosus, cujo EBITDA ajustado do ecossistema
  foi de US$ 1,3 bilhão (Bloomberg Línea, 29/06/2026; Prosus FY26).
- Ano fiscal anterior (abril/2024 a março/2025): receita de R$ 7,5 bilhões
  (relatório de sustentabilidade do iFood); EBIT ajustado do iFood cresceu 178%
  (Prosus, 23/06/2025).

**P2 — precariedade.**
- 1,7 milhão de plataformizados em 2024, contra 1,3 milhão em 2022 (+25,4%).
  Só **35,9%** contribuem para a Previdência. Informalidade de **84,3%** entre
  motociclistas. Entregadores: 46,4 horas semanais. Renda-hora de R$ 15,4,
  **8,3% abaixo** dos demais ocupados (IBGE, PNAD Contínua, 17/10/2025).
- O contraste com o Portal de Dados do iFood (R$ 29,65/hora "em rota",
  modalidade nuvem) é o debate que o paper precisa travar: hora em rota não é
  hora trabalhada, e a modalidade nuvem é selecionada.

**P3 — a conta pública.**
- Internações de motociclista no SUS, janeiro a novembro de 2024: 148.797,
  custando R$ 233,3 milhões (Abramet sobre SIH). Em 2023: 145.761 internações
  (nosso D-019), R$ 221,5 milhões, R$ 1.561 por AIH. Isso é **o valor pago**,
  não o custo — `VAL_TOT` é piso declarado (dicionário do painel).
- Ipea: o SUS gastou R$ 449 milhões com vítimas de trânsito em 2024, e desde
  2021 deixou de receber cerca de **R$ 580 milhões por ano** do DPVAT, cujos 45%
  eram vinculados ao custeio dessas vítimas. A fonte de financiamento que
  existia para essa conta foi extinta exatamente no período em que a frota de
  entrega se expandiu.
- Empregador formal paga a contribuição do RAT (Riscos Ambientais do
  Trabalho), de 1% a 3% da folha, que financia o benefício acidentário. A
  plataforma não tem folha: com 84% de informalidade, **ninguém paga o RAT do
  entregador**. Essa é a externalidade fiscal em uma linha, e é o que a lacuna
  SIH × INSS (espécie 91 quase vazia) vai mostrar em número.

**P4 — mortes e invisibilidade.**
- 13.477 motociclistas mortos em 2023 (Ministério da Saúde, SIM). Perfil:
  homens de 20 a 39 anos; mais de 60% dos óbitos de trânsito são de moto
  (Abramet).
- 62 internações com nexo ocupacional em 965.714 (D-019). O sistema de
  informação é cego ao trabalho — e isso é achado (D-008), não defeito.

## O que o desenho causal faz aqui — e o que não faz

O V2 responde a uma pergunta só: **quanto do crescimento das internações é da
plataforma.** É a fração que converte P3 de "o SUS paga por acidentes de moto"
em "o SUS paga por acidentes que a remuneração por corrida causou". Sem essa
fração, a proposta de política é uma opinião; com ela, é um número a cobrar.

O que o V2 **não** faz: não mede lucro, não mede precariedade, não mede a
lacuna previdenciária, e não propõe nada. As três razões de piso (D-001, D-021,
D-027) continuam valendo — mas o paper precisa dizê-las em uma frase, não em
três seções. **A profundidade do método vai para o anexo; o argumento vai para
o texto.**

## Políticas públicas — o cardápio a avaliar com a evidência

Candidatas, não conclusões. Cada uma se ancora numa perna, e a evidência do
projeto é o que diz se ela é proporcional. A ordem é da mais direta à mais
estrutural.

| Política | Perna | O que a evidência do projeto precisa mostrar | Onde está o debate hoje |
|---|---|---|---|
| **Contribuição acidentária das plataformas** — equivalente ao RAT, calculada sobre o valor das corridas, vinculada ao SUS e ao benefício acidentário | P3 | Custo público atribuível por município e por ano; o V2 dá a fração atribuível, a camada de custo dá o valor | O PLP 12/2024 prevê alíquota previdenciária mínima, mas cobre só motoristas de passageiros; entregadores ficaram fora do acordo |
| **Repasse por corrida ao SUS**, no molde do que o DPVAT fazia (45% ao SUS) | P3 | O buraco de R$ 580 mi/ano desde 2021 contra a curva de internações no mesmo período | DPVAT extinto em 2021; SPVAT em transição — ver anexo A, 3.4 |
| **Seguro de acidentes obrigatório**, permanente, custeado pela plataforma | P4 | Internações, UTI e óbito por município tratado; o que o seguro voluntário do iFood cobre e o que não cobre | Lei 14.297/2022 obrigou durante a emergência sanitária e caducou; PL 391/2020 no Senado |
| **Nexo ocupacional registrado na AIH e no SINAN** — campo "trabalho por plataforma" | P4 | A taxa de 1 em 15.576 (D-019) e o preenchimento do `CAR_INT` por município (`make diagnostico`) | Não existe proposta; é a mais barata e a única que faz o Estado enxergar o problema |
| **Transparência obrigatória**: volume de corridas, entregadores ativos e sinistros reportados ao regulador, por município | P1, P3 | A lacuna 4.3 do inventário — sem volume de pedidos, a H2 fica parcialmente identificada. É o dado que só a lei consegue abrir | Sem proposta federal; a liminar da Bahia obrigou preservação de dados via MPT |
| **Limite de jornada e piso por hora trabalhada** (não por hora em rota) | P2 | 46,4 h semanais e R$ 15,4/hora da PNAD contra os R$ 29,65 "em rota" da empresa | PLP 12/2024 fixa teto diário e piso, só para motoristas; Convenção 193 da OIT (12/06/2026) é o marco internacional novo |
| **Desincentivo à velocidade**: proibição de bônus por corrida rápida e de penalidade por recusa | P4 | É o mecanismo da H1. O deslocamento horário dos sinistros (RENAEST, seção 7 do plano) é a assinatura | Sem proposta; é o que a pesquisa acrescenta ao debate, que hoje é só sobre vínculo |

**Contexto de setembro de 2026.** O STF suspendeu em 24/06/2026 o julgamento
sobre vínculo empregatício (RE 1.446.336, Uber; Rcl 64.018, Rappi), a pedido da
DPU, por causa da Convenção 193 da OIT aprovada doze dias antes. O Congresso
discute o PLP 12/2024 na Câmara. **Todo o debate público é sobre vínculo.
Nenhuma das partes está discutindo quem paga a conta do SUS.** É esse o espaço
que o projeto ocupa: não precisa decidir se há vínculo para mostrar que há
externalidade.

## Critério de inclusão

Substitui o do README ("se não reaparece no paper causal, não entra"):

**Se não sustenta uma das quatro pernas ou uma linha da tabela de políticas,
não entra.** O V2 continua sendo a maior peça, mas não é o critério.

## O que falta, em ordem

1. **P3(a) — custo.** Deflacionar `val_tot` (IPCA), converter em custo
   econômico com os parâmetros do Ipea (camada F6), e escrever a série
   nacional 2008– por ano. É um alvo de `make` e uma tabela. Não depende de
   pré-registro.
2. **P3(b) — lacuna SIH × INSS.** Baixar benefícios concedidos (espécies 31 e
   91) com CID V20–V29, por UF e ano, e pôr ao lado do SIH. D-002 prometeu
   isso como "capítulo próprio" e nunca foi agendado.
3. **P1 — série de lucro.** Tabela anual a partir dos relatórios da Prosus,
   em reais, no mesmo eixo temporal que a série de custo. Fonte nova no
   inventário (Bloco 6).
4. **P2 — PNAD.** Baixar o módulo de 2022, 2024 e 2025 e tirar as quatro
   estatísticas (informalidade, previdência, jornada, renda-hora) por região.
5. **F3 — cronologia de entrada.** Continua sendo o caminho crítico do V2.
   Anda em paralelo, não antes.
6. Migrar aqui o documento original `pre-projeto-remuneracao-entrega-acidentes.md`
   (fases F0–F4, desenhos A e B, cronograma), que não está no repositório.
