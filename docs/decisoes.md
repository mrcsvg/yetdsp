# Log de decisões

Registro datado de toda escolha metodológica com mais de uma alternativa defensável. Serve para três coisas: não reabrir discussão já fechada, responder revisor com data e motivo, e distinguir o que foi decidido *antes* de ver o dado do que foi decidido depois.

**Formato:** uma entrada por decisão. Nunca editar entrada antiga — adicionar uma nova que a revise, referenciando a anterior.

---

## D-001 · Desenho é ecológico, não individual
**Data:** 2026-09-12
**Decisão:** o tratamento é medido no nível município × mês; o desfecho é o total de motociclistas internados. Não se tenta identificar o indivíduo entregador.
**Motivo:** nenhuma base administrativa pública liga uma internação a uma plataforma. O `CAR_INT` do SIH e o CBO do SINAN são as únicas aproximações e têm preenchimento sofrível.
**Consequência a declarar no paper:** o coeficiente é um piso. Ele dilui o efeito sobre entregadores no universo de todos os motociclistas. Qualquer leitura de magnitude precisa ser reescalada pela participação estimada de entregadores na frota em circulação, com o erro dessa reescala propagado.
**Alternativa rejeitada:** desenho individual via SINAN ACGR com filtro de CBO. Rejeitado por completude de CBO ruim na maioria das UFs e por cobertura heterogênea entre municípios, que é confundidor direto num painel de efeitos fixos.

## D-002 · SINAN e INSS fora do escopo inicial
**Data:** 2026-09-12
**Decisão:** V1 e a estimação principal do V2 usam apenas SIH, SIM, frota RENAVAM e população IBGE. SINAN ACGR e microdados do INSS saem da rota crítica.
**Motivo:** ambos pressupõem registro formal do trabalhador, e a população de interesse é majoritariamente informal — a PNAD indica informalidade acima de 84% entre motociclistas plataformizados e cobertura previdenciária de ~36%. As bases são abertas, mas estruturalmente cegas ao caso.
**Retorno previsto:** voltam como medida de subnotificação, comparando o volume do SIH ao volume de benefícios e CAT por UF e ano. É capítulo próprio, não insumo da estimação.

## D-003 · Denominador é frota, não população
**Data:** 2026-09-12
**Decisão:** taxa de internação de motociclista usa frota de motocicletas RENAVAM do município como denominador.
**Motivo:** usar população confunde o efeito da plataforma com o crescimento da motorização, que é forte e heterogêneo entre municípios no período.
**Exceção:** ciclista roda em contagem bruta com efeito fixo de município. Bicicleta não é veículo automotor, não registra em RENAVAM, e não existe denominador nacional. Estimativas de modal via Censo ou pesquisas OD municipais não têm cobertura nem periodicidade suficientes para um painel mensal.

## D-004 · Ciclista como teste do mecanismo, não como desfecho secundário
**Data:** 2026-09-12
**Decisão:** internações de ciclista (V10–V19) entram como teste da via causal, não como desfecho paralelo.
**Motivo:** entrega por bicicleta responde ao mesmo incentivo de remuneração por corrida e não envolve aquisição de veículo novo nem habilitação. Se o efeito estimado for pressão de entrega, deve aparecer em ciclista; se aparecer só em moto, a objeção "isto é apenas crescimento da frota" ganha força.
**Limitação:** o RENAEST praticamente não captura ciclista — o registro nasce de boletim de ocorrência e queda sem contato com veículo motorizado raramente gera BO. O teste só é viável no SIH.

## D-005 · Placebo é ocupante de automóvel
**Data:** 2026-09-12
**Decisão:** V40–V49 como grupo placebo.
**Critério de falha pré-declarado:** se o efeito estimado sobre ocupante de automóvel for estatisticamente indistinguível do efeito sobre motociclista, o desenho está capturando tendência geral de trânsito e a estimativa não sustenta interpretação causal.

## D-006 · Pré-registro antes de qualquer cruzamento tratamento × desfecho
**Data:** 2026-09-12
**Decisão:** o plano de análise é depositado com timestamp (OSF) antes de cruzar a cronologia de entrada de plataforma com as internações, inclusive em exploração gráfica.
**Motivo:** análise descritiva do SIH isolada não compromete o pré-registro; olhar a relação tratamento–desfecho compromete. Depois do depósito, especificação nova é análise exploratória declarada.

## D-007 · SIH é o desfecho, RENAEST é textura
**Data:** 2026-09-12
**Decisão:** desfecho principal vem do SIH. RENAEST entra como robustez e como fonte de características do sinistro.
**Motivo:** RENAEST é agregado e depende de alimentação pelos Detrans estaduais, com cobertura desigual entre estados e ao longo do tempo — o que o torna perigoso como desfecho num painel de efeitos fixos. O SIH captura qualquer pessoa internada no SUS, com cobertura muito mais estável.
**A verificar:** se o arquivo de Sinistros traz hora do sinistro com completude usável. Entrega tem pico de almoço e jantar; um deslocamento da distribuição horária dos sinistros de moto para 11h–14h e 18h–22h após a entrada da plataforma seria assinatura bem mais específica que o volume agregado.

## D-008 · Má qualidade do `CAR_INT` é resultado, não obstáculo
**Data:** 2026-09-12
**Decisão:** medir e reportar o percentual de internações de motociclista com `CAR_INT` em 03 (acidente no local de trabalho) ou 04 (acidente de trajeto) é um achado do V1.
**Motivo:** quantifica a cegueira do sistema de informação a uma categoria de trabalhador cujo perfil demográfico e mecanismo de lesão são conhecidos. Não é defeito de dado a corrigir — é a lacuna que o paper documenta.
**Atenção:** a tabela de domínio do `CAR_INT` mudou de versão ao longo da série. Confirmar contra a "Estrutura dos arquivos SIHSUS – RD" da competência mais antiga usada antes de encadear.

## D-009 · Microdado não é versionado
**Data:** 2026-09-12
**Decisão:** nenhum arquivo de dado no git. O repositório carrega o código que reconstrói os dados.
**Motivo:** volume, e o inventário de fontes já documenta órgão, formato e caminho de cada base — a reprodutibilidade vem de lá, não de um blob commitado.

## D-010 · O quarto dígito tem duas estruturas, não uma
**Data:** 2026-09-14
**Decisão:** a leitura do quarto caractere do CID passa a depender da categoria. Categorias de colisão e não-colisão (V10–V18, V20–V28, V40–V48) seguem a estrutura padrão; as categorias "outros e não especificados" (V19, V29, V49) seguem a estrutura terminal, que reaproveita `.3`, `.6` e `.8` com outro sentido.

| Dígito | Padrão (V20–V28) | Terminal (V29) |
|---|---|---|
| `.0` `.1` `.2` | condutor / passageiro / não esp., **não-trânsito** | idem, colisão com outro veículo a motor |
| `.3` | pessoa ao embarcar ou desembarcar | **qualquer ocupante, acidente NÃO de trânsito** |
| `.4` `.5` | condutor / passageiro, **trânsito** | idem |
| `.6` | não existe | não especificado, **trânsito** |
| `.8` | não existe | outros acidentes de transporte especificados |
| `.9` | não especificado, **trânsito** | qualquer ocupante, **trânsito** não especificado |

**Motivo:** a versão anterior aplicava uma regra única (`{3,4,5,6,7,8,9}` = trânsito) sobre o quarto dígito, independente da categoria. Isso classificava **V19.3, V29.3 e V49.3 como acidente de trânsito quando o CID-10 os define como explicitamente não-trânsito**. V29 é categoria de alto volume no SIH — é onde cai o registro sem detalhe do veículo antagonista —, então o erro não é marginal: contamina o numerador do desfecho principal e o do placebo em magnitudes diferentes, o que é pior que contaminar os dois igualmente.
**Consequência:** `internacoes_transito` cai em relação ao que a versão anterior produziria. Qualquer número gerado antes desta data está inflado e não deve ser comparado com os novos.
**Ponto em aberto — `.3` da estrutura padrão.** "Pessoa ao embarcar ou desembarcar" não traz a distinção trânsito/não-trânsito na definição da OMS. Adotamos **contar como trânsito**, seguindo a faixa `V20-V28[.3-.9]` da definição padrão do NCHS. É convenção, não definição: o painel traz `internacoes_embarque` isolando essas AIH para que a sensibilidade seja calculável sem reprocessar o SIH.
**Alternativa rejeitada:** manter a regra única e tratar a diferença como ruído. Rejeitada porque o erro é sistemático por categoria, não aleatório, e V19/V29/V49 têm peso desigual entre os três grupos do desenho.

## D-011 · `CAR_INT` em branco não é `CAR_INT` preenchido
**Data:** 2026-09-14
**Decisão:** `car_int_preenchido` conta apenas códigos do domínio (`01`–`06`). Ficam de fora string vazia e as sentinelas `00` e `99`, que circulam como "ignorado" em parte da série.
**Motivo:** a versão anterior contava `CAR_INT.notna()`, e o campo em branco no arquivo RD chega como string vazia, não como nulo — passava por preenchido. Como a taxa de nexo é `nexo / car_int_preenchido` (ver D-008 e `docs/dicionario-painel.md`), um denominador inflado por brancos **subestima a subnotificação**, que é exatamente o achado do V1. O erro empurrava o resultado na direção conveniente, o que é o pior tipo.
**A conferir antes de encadear a série:** se `00` e `99` de fato aparecem como sentinela nas competências mais antigas, ou se são código válido em alguma versão do layout. A lista está em `ifode.cid.CAR_INT_AUSENTE`, num lugar só, e é o que os testes cobrem.

## D-012 · A lógica vive no pacote, o script é entrypoint
**Data:** 2026-09-14
**Decisão:** definição de caso em `src/ifode/cid.py`, download em `ifode.extract`, limpeza e agregação em `ifode.transform`, diagnóstico em `ifode.analyze`. `scripts/` só faz parsing de argumento, I/O e log.
**Motivo:** a definição de caso é o artefato metodológico do projeto — precisa ser testável sem rede, citável por caminho de arquivo e revisável isoladamente. Enquanto morava dentro de um script, o teste a alcançava por `sys.path.insert`, e nada impedia que uma segunda cópia da regra do quarto dígito nascesse no script seguinte.

## D-013 · A frota do denominador é a que casa com V20–V29, não a coluna `MOTOCICLETA`
**Data:** 2026-09-14
**Decisão:** o denominador de motociclista soma **`MOTOCICLETA` + `MOTONETA` + `CICLOMOTOR` + `SIDE-CAR`** do arquivo "Frota por Município e Tipo" do Senatran. `TRICICLO` e `QUADRICICLO` ficam de fora.
**Motivo:** o denominador tem que casar com o numerador, e o numerador é V20–V29. A nota de inclusão do próprio CID-10 brasileiro resolve a questão:

> **V20-V29** Motociclista traumatizado em um acidente de transporte
> *Inclui:* bicicleta motorizada · motocicleta com "side-car" · **motoneta** · patinete motorizado
> *Exclui:* **triciclo motorizado (V30-V39)** · veículo motorizado de três rodas (V30-V39)
>
> — DATASUS, CID-10 v2008

Motoneta e side-car estão nomeados; ciclomotor é a "bicicleta motorizada"/moped da mesma lista. Triciclo é mandado explicitamente para V30–V39, que não é o desfecho deste projeto.
**Magnitude, para não parecer detalhe:** em Curitiba, dezembro de 2023, `MOTOCICLETA` sozinha dá 170.754; a frota que corresponde a V20–V29 dá **204.058**. Usar a coluna óbvia inflaria a taxa em 19%, e no sentido conveniente.
**Os dois erros possíveis andam em direções opostas e nenhum aparece no resultado:** usar só `MOTOCICLETA` subestima a exposição e infla a taxa; somar triciclo e quadriciclo conta veículo cujo acidente nunca entra no numerador. A regra mora em `src/ifode/frota.py`, num lugar só, com teste por tipo.

## D-014 · Município do Senatran casa por tabela revisada, nunca por fuzzy match
**Data:** 2026-09-14
**Decisão:** a ponte entre o nome de município do Senatran e o código IBGE usa normalização exata (caixa alta, sem acento, sem pontuação) e, para o que sobra, uma **tabela fixa e revisada a mão** em `src/ifode/municipios.py`. Município não reconhecido é **reportado, nunca descartado nem chutado**.
**Motivo:** a normalização exata casa 5.533 de 5.572 linhas (99,3%). As 39 sobras são de três tipos: grafia divergente (`LAGEDO`/`LAJEDO`, `PARATI`/`PARATY`, e um `BARAO D0 MONTE ALTO` com zero no lugar da letra O), truncamento em 30 caracteres (`VILA BELA DA SANTISSIMA TRINDA`), e **município renomeado**, com o Senatran carregando o nome antigo.
**A evidência contra o fuzzy.** Rodamos `difflib` uma vez sobre as sobras, sob revisão, e ele **errou cinco** — todos do terceiro tipo, onde o nome novo não se parece com o velho:

| Senatran | Fuzzy sugeriu | Correto |
|---|---|---|
| `SANTAREM` (PB) | Santo André | **Joca Claudino** (2513653) |
| `SAO DOMINGOS DE POMBAL` (PB) | S. Domingos do Cariri | **São Domingos** (2513968) |
| `FORTALEZA DO TABOCAO` (TO) | Porto Alegre do Tocantins | **Tabocão** (1708254) |
| `SAO VALERIO DA NATIVIDADE` (TO) | Chapada da Natividade | **São Valério** (1720499) |
| `BOA SAUDE` (RN) | — | **Januário Cicco** (2405306) |

Um join errado num denominador não deixa rastro: a frota de um município entra na conta de outro e a taxa sai plausível e errada. Denominador que some deixa `NaN`, que se vê; denominador que casa errado, não.
**Consequência operacional:** a tabela é revisável em diff, os testes fixam cada par, e `agregar_frota` grita quando o número de não-casados passa de 20 — sinal de que o layout mudou. Com os apelidos, 2016, 2019, 2023 e 2025 casam 5.570 de 5.570 municípios reais; a única sobra é `MUNICIPIO NAO INFORMADO`, que é exclusão deliberada.

## D-015 · Cobertura dos denominadores: dois buracos a declarar
**Data:** 2026-09-14
**Decisão:** registrar como limitação, não contornar com imputação silenciosa.

**1. Frota municipal só existe a partir de julho de 2016.** A página do Senatran de 2015 publica apenas "Frota por UF e Tipo de Veículo", sem abertura municipal; 2016 tem só julho a dezembro. A janela padrão do `Makefile` começava em 2015-01, o que dá 18 meses sem denominador de frota. **Isso encurta a janela pré-tratamento disponível para o V2** e precisa entrar na escolha da janela de evento do pré-registro (seção 5).

**2. Estimativa populacional municipal não tem 2022 nem 2023.** O agregado 6579 do IBGE publica 2001–2021 e retoma em 2024: 2022 foi ano de Censo e a estimativa não foi divulgada. Quem precisar de 2022 tem que ir ao Censo, que é outra definição de população — encadear os dois sem dizer é comparar coisas diferentes. `ifode.extract.ibge.populacao` devolve os anos que faltaram em vez de omitir linha.

**Por que não interpolar:** os dois buracos são no denominador. Interpolar população entre 2021 e 2024 embute a revisão do Censo 2022 como se fosse crescimento suave — em Curitiba a estimativa cai de 1.963.726 (2021) para 1.829.225 (2024), e essa queda é rebasing, não migração. Se a interpolação for feita depois, que seja declarada e testada contra a alternativa.

## D-016 · Frota vem da página do Senatran, não do RENAVAM de dados abertos
**Data:** 2026-09-14
**Decisão:** a frota é lida de "Frota por Município e Tipo" (`gov.br/transportes`, ~1,2 MB/mês), não do dataset `registro-nacional-de-veiculos-automotores-renavam` do portal de dados abertos.
**Motivo:** o dataset do portal traz `UF; Município; Marca Modelo; Ano Fabricação; Qtd. Veículos` — **sem coluna de tipo de veículo** — em ~136 MB por mês. Derivar "motocicleta" dali exigiria classificar dezenas de milhares de strings de marca/modelo em categorias, e o erro dessa classificação entraria direto no denominador, sem medida. O arquivo do Senatran já vem com uma coluna por tipo.
**Nota de implementação:** o nome do arquivo não é chave — o mesmo relatório aparece como `frota_por_municipio_e_tipo-dez_16.xlsx`, `frota_munic_modelo_dezembro_2019.xls`, `FrotaporMunicipioetipoDEZEMBRO2025.xlsx` e `copy2_of_Frota_por_municipio_tipo_Maro_2025.xlsx`. O **rótulo do link** é estável, e é por ele que `ifode.extract.senatran` localiza o mês.

## D-017 · A causa externa não está no diagnóstico principal
**Data:** 2026-09-16
**Decisão:** o filtro de caso passa a procurar V10–V49 numa **união ordenada** de campos de diagnóstico — `DIAG_SECUN`, `DIAGSEC1`…`DIAGSEC9`, `DIAG_PRINC` — ficando com o **primeiro código que cai na definição de caso**, não o primeiro campo preenchido. A AIH registra de qual campo veio (`campo_causa`).
**Motivo:** a versão anterior filtrava `DIAG_PRINC`. Pela norma do próprio SIH/SUS:

> "As internações provocadas por causas externas devem ser classificadas, **no diagnóstico principal, segundo o tipo de traumatismo** (capítulo XIX, causas S e T). **No diagnóstico secundário, deve ser codificado segundo a origem da causa externa** — capítulo XX (causas V a Y). Existem situações em que é permitido que o diagnóstico principal seja classificado diretamente pelo capítulo XX."
> — DATASUS, *Morbidade Hospitalar do SUS por Causas Externas*, notas técnicas

**Isto não era imprecisão: era o desfecho inteiro.** Medido no SIH (Base dos Dados, Brasil):

| ano | motociclista na causa externa | motociclista em `DIAG_PRINC` |
|---|---|---|
| 2016 | 107.385 | **0** |
| 2019 | 117.577 | **0** |
| 2023 | 145.184 | **0** |

O pipeline produzia painel vazio em todo ano da série. Nenhum teste pegou porque as fixtures punham o código V no principal — o único lugar onde ele não está.

**Por que união e não só o secundário:** a norma permite o principal, e o dado confirma que a cauda existe. Em junho/2023, 14.235 das 14.295 AIH tiveram a causa em `DIAGSEC1`, mas **60 vieram de `DIAGSEC2`–`DIAGSEC5`** — que uma regra fixada em `DIAGSEC1` perderia.
**Por que "o primeiro que casa" e não "o primeiro preenchido":** o campo de maior precedência quase sempre traz a lesão (`S825`, `T111`). Parar no primeiro campo não nulo descartaria a AIH inteira por causa de um S no caminho.
**Precedência declarada:** `DIAG_SECUN` → `DIAGSEC1..9` → `DIAG_PRINC`. Havendo mais de um código válido, vence o de maior precedência; a regra é fixa e testada. Casos com dois códigos V distintos são raros e merecem contagem própria antes de qualquer estimação.
**Consequência:** qualquer número produzido antes desta data é vazio, não apenas enviesado.

## D-018 · Base dos Dados entra como segunda fonte, não como substituta
**Data:** 2026-09-16
**Decisão:** `ifode.extract.bigquery` lê o SIH do espelho da Base dos Dados no BigQuery, com adapter para o domínio do arquivo RD. O caminho oficial continua sendo o `.dbc` do FTP (`ifode.extract.sih`).
**Motivo:** o FTP do DATASUS não é alcançável de todo ambiente, e o Anexo A já previa a Base dos Dados "para conferência". Duas fontes com a mesma definição de caso tornam a divergência entre elas mensurável — e ela existe.
**Cinco divergências medidas, todas tratadas no adapter.** Cada uma produz erro silencioso, não exceção:

| # | Espelho | Arquivo RD | Efeito se ignorado |
|---|---|---|---|
| 1 | `carater_internacao` = `1`–`6` | `01`–`06` | nexo ocupacional sai **zero** |
| 2 | `sexo_paciente` = `Masculino`/`Feminino` | `1`/`3` | contagem de homens sai **zero** |
| 3 | CID partido em `_categoria` (3 car.) e `_subcategoria` (4 car.) | campo único | perde metade dos códigos, e o quarto dígito mora justamente na outra coluna |
| 4 | `sigla_uf` INTEGER e **inteiramente nula** | — | filtro por UF zera o resultado |
| 5 | `carater_internacao` **100% preenchido, sem nulos** | tem branco | infla o denominador do nexo |

**A divergência 5 é a que importa para o resultado.** A taxa de *preenchimento* desta fonte não é confiável: no RD cru há branco, aqui não há nenhum. O numerador do nexo é piso defensável; o denominador precisa vir do RD. **Reportar taxa de nexo a partir do BigQuery sem essa ressalva seria erro.**
**A conferir:** se o espelho recodificou branco para algum valor do domínio (o que empurraria AIH para `02`, a categoria dominante) ou se descartou as linhas.

## D-019 · Primeiro número do V1
**Data:** 2026-09-16
**Registro** — não é decisão, é o resultado que o V1 existe para produzir. Brasil, SIH via Base dos Dados:

**2016–2023, motociclista (V20–V29): 965.714 internações. 62 com nexo ocupacional declarado — 17 como acidente no local de trabalho, 45 como acidente de trajeto. Uma em 15.576.**

Em 2023 isoladamente: 145.761 internações de motociclista, **10** com nexo. O grupo placebo (ocupante de automóvel) teve **zero**.

**Magnitude do D-010 no dado real:** a regra achatada classificava 60.511 AIH como trânsito indevidamente em 2016–2023 (V29.3, 13.706; V29.8, 46.805) — 6,3% do desfecho. E V29 sozinha é 67% de todas as internações de motociclista, contra a expectativa de "categoria de alto volume" que o D-010 registrava sem número.

Os três números carregam a ressalva do D-018: o denominador do preenchimento vem de fonte que não tem branco. A ordem de grandeza do nexo (dezenas, em centenas de milhares) não depende disso.

## D-020 · Marketplace não é tratamento; a logística própria é
**Data:** 2026-09-17
**Decisão:** o evento de tratamento é **a data em que a plataforma passa a operar frota própria de entregadores remunerados por corrida naquele município** — não a data em que o aplicativo passou a atender a cidade.
**Motivo:** a hipótese do projeto é sobre remuneração por peça criando incentivo à velocidade e ao volume. Isso pressupõe entregador da plataforma, pago por corrida. Entre 2011 e 2017 o iFood era **marketplace**: o pedido vinha pelo app, mas quem entregava era o motoboy do restaurante, remunerado pelo restaurante. A própria empresa data a virada:

> "**It began deliveries in 2018; before then restaurants were responsible.**"
> — iFood, release institucional (`institucional.ifood.com.br/releases/brazilian-delivery-group-ifood-corners-meals-market`)

**Por que isso decide a viabilidade do V2.** O denominador de frota municipal só existe a partir de julho/2016 (D-015). Se o tratamento fosse "iFood existe na cidade", boa parte dos municípios estaria tratada antes do primeiro denominador e não haveria pré-período. Com o tratamento datado na logística própria, o marco nacional é 2018 — e o rollout municipal é escalonado:

| | municípios atendidos |
|---|---|
| 2018 | início da operação própria |
| 2019 | ~900 |
| 2023–2025 | ~1.500 |
| 2026 | ~1.700 |

De **5.570 municípios**. Para os tratados a partir de 2020, o pré-período com denominador passa de três anos.

**Variação de timing além do iFood**, com datas próprias a codificar: Rappi (~2017), Uber Eats (~2016, **saiu em março/2022**), 99Food (**novembro/2019, estreia em Belo Horizonte**; 59 cidades em janeiro/2022; saiu em 2023; retomou em agosto/2025), Keeta/Meituan (dezembro/2025), Loggi (expansão nacional 2018–2019). **As saídas são tratamento reverso** — Uber Eats e 99Food deixando municípios são variação rara e valiosa, e devem ser codificadas como evento próprio, não ignoradas.

**Consequência operacional para o F3, e é séria:** a imprensa local noticia a chegada do *aplicativo*, não a da frota. Um release de 2016 dizendo "iFood chega a [cidade]" é marketplace, não tratamento. **Dois codificadores podem concordar com kappa alto sobre o evento errado.** O protocolo de codificação precisa da distinção explícita e de um critério de desempate documentado antes de começar — ver a seção 4 do plano de análise e o item 4.4 do Anexo A.

## D-021 · O pré-período está parcialmente tratado
**Data:** 2026-09-17
**Decisão:** declarar, como limitação, que o período pré-tratamento não é livre de plataforma — apenas livre de *remuneração por corrida*.
**Motivo:** o marketplace operou de 2011 a 2017. É plausível que ele já tenha elevado o volume de entregas por moto no município, ainda que o entregador fosse do restaurante e não remunerado por corrida. Isso vaza tratamento para o "antes".
**Direção do viés:** atenuação. O contraste medido é "corrida avulsa" contra "marketplace", não contra "sem plataforma" — então o coeficiente subestima o efeito de plataformização em relação a um contrafactual sem nenhuma plataforma. **É a mesma direção do piso que o D-001 já declara, por um motivo diferente e adicional**, e as duas razões precisam aparecer separadas no paper: uma é diluição no universo de motociclistas, a outra é contaminação do período de comparação.
**O que não fazer:** tratar a entrada do marketplace como um segundo evento e estimar os dois. Sem dado de volume de pedidos (lacuna 4.3, fechada), o marketplace não tem intensidade mensurável, e um evento sem intensidade num painel escalonado adiciona ruído sem identificar nada.

## D-022 · Grupo de comparação é not-yet-treated
**Data:** 2026-09-17
**Decisão:** o grupo de comparação do estimador de Callaway & Sant'Anna é **not-yet-treated**, não never-treated. Resolve o `[ ]` da seção 5 do plano de análise.
**Motivo:** os nunca tratados existem em volume — cerca de 3.900 dos 5.570 municípios nunca receberam operação própria de plataforma. Mas não são comparáveis: os tratados são urbanos e maiores, os nunca tratados são pequenos e rurais, por construção, porque é exatamente isso que determina a entrada da plataforma. **Comparar os dois compara urbanização, não plataforma** — e urbanização move motorização, tráfego e oferta hospitalar ao mesmo tempo, todos ligados ao desfecho.
Not-yet-treated compara município tratado em `t` com município que será tratado depois, mantendo a comparação dentro da população que a plataforma considera atendível. O Callaway & Sant'Anna suporta isso nativamente e é a razão de ele ser o estimador principal.
**Custo a declarar:** com a saturação crescendo ao longo da janela, o conjunto de not-yet-treated encolhe no fim do período, e os grupos tratados tardiamente têm comparação mais fina. Reportar o tamanho do grupo de comparação por coorte de tratamento, não só o efeito agregado.
**Alternativa rejeitada:** never-treated como comparação principal. Rejeitada pelo confundimento de urbanização acima. Pode voltar como **robustez**, restrita a municípios nunca tratados pareados por porte populacional e frota — e se o resultado divergir do principal, é sinal de que a seleção urbana está ativa, o que é informação, não fracasso.
