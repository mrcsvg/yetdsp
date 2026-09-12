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
