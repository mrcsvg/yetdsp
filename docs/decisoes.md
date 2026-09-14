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
