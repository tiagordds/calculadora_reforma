# Especificação do produto

[CÓDIGO] A partir da apuração mista, o gestor pode comparar a obrigação mensal do CNPJ nas duas modalidades, verificar como os históricos alteram o anexo do serviço e identificar o que falta para fechar as contas de IBS e CBS. [Comparação mista de março de 2027](SIMPLES_MIXED_HYBRID_01.md)

[CÓDIGO] No C09, o gestor informa separadamente a revenda local de canetas e o software sob encomenda do mesmo CNPJ. Vê a receita total de março, a folha e a receita histórica empresariais, os anexos, as duas parcelas e a estimativa consolidada. Pode corrigir um mês ou completar uma atividade mantendo os demais dados. [Jornada tradicional mista](SIMPLES_MIXED_01.md)

[DECISÃO] Em 25/11/2026, a jornada de software sob encomenda passou a responder quanto a obrigação mensal pode mudar ao manter preço e volume e apurar IBS/CBS pelo regime regular. O gestor vê Fator R, anexo e composição do DAS por trajetória e pode refinar as contas antes da comparação. [C08 comparativo interno](SIMPLES_SERVICES_HYBRID_01.md)

[DECISÃO] A partir de 24/11/2026, além do recorte original de revenda descrito abaixo, a página inicial oferece a apuração tradicional de software sob encomenda no estabelecimento em Florianópolis. A pergunta do gestor é quanto a folha dos doze meses muda o enquadramento e o DAS de março de 2027. [Primeiro perfil de serviços e limites](SIMPLES_SERVICES_01.md)

[CÓDIGO] A entrega local da 04 permite comparar março para a mesma revenda. O gestor pode começar por preço e histórico e depois identificar a base regular, os créditos e a situação da opção. O resultado diferencia obrigação, saldo credor e guia pendente. [Comparador e campanha de aceite](PHASE_04.md)

[CÓDIGO][EXECUTADO] A entrega local da Fase 03 permite estimar o DAS tradicional para o perfil da papelaria, ver os seis tributos e substituir a média pelos meses reais no mesmo formulário. A comparação econômica continua prevista para uma fase própria. [Jornada e evidências](PHASE_03.md)

## Para quem e para quê

Um empresário ou gestor de PME deve conseguir estimar o que pagaria e entender por que os cenários divergem. O contador ou consultor deve conseguir revisar os dados, substituir estimativas e reproduzir cada resultado. Personas e diferenciais comerciais são hipóteses a investigar por entrevistas e pesquisa de mercado. O produto é independente de consultoria, sistema de gestão ou cliente específico.

## Jornada pelo navegador

| Modalidade | Entrada e refinamento | Resultado esperado |
|---|---|---|
| Rápida, pública, sem cadastro | Receita média mensal ou anual, atividade compreensível, período editável e município/UF quando necessários. Regime atual, perfil de clientes, compras, folha e margem são opcionais. Oferecer “Não sei informar”. | Estimativa em poucos segundos como meta a medir. Mostrar valores, elegibilidade, premissas determinantes e limitações, com detalhe expandível. Se faltar dado indispensável, apontar qual e por quê. |
| Intermediária | Reaproveitar o cenário, acrescentando CNAE, receita de 12 meses, folha e encargos, pró-labore, compras, custos, margens, fornecedores e clientes. | Identificar os dados cuja revisão mais altera a comparação. |
| Avançada | Segregações, documentos e operações, classificações, contabilidade, DRE, benefícios, ajustes e créditos. | Memória de cálculo, análises de sensibilidade, pontos de mudança e impactos financeiros. |

Não exigir domínio de CST, NCM, NBS, cClassTrib, RBT12 ou Fator R para começar. Derivar códigos somente quando os dados forem suficientes. Preservar entradas entre modalidades. Priorizar legibilidade, contraste, teclado, celular e erros em linguagem acessível. Páginas públicas explicativas terão URLs e metadados indexáveis. Resultados privados e dados financeiros exigem proteção contra indexação.

## Cobertura e metodologia pretendidas

- Distinguir cálculo de item/operação, apuração da empresa por competência e comparação econômica. A primeira operação de ponta a ponta precede a simulação empresarial. A prioridade temporal de 2027 depende de cobertura comprovada para o recorte escolhido.
- Comparar inicialmente Simples Nacional com recolhimento tradicional e com opção de apuração regular de IBS/CBS (“híbrido”). Depois incluir Lucro Presumido, Lucro Real e projeções até 2033. Considerar tributos de consumo em transição, tributos sobre o lucro, CPP e encargos, faixas, anexos, Fator R, benefícios, limites, sublimites, vedações, condições e prazos de opção conforme o caso.
- Registrar elegibilidade como **elegível**, **não elegível**, **elegibilidade não confirmada** ou **fora da cobertura**. A recomendação de uma opção legal exige elegibilidade confirmada.
- Declarar a base econômica antes da comparação: faturamento e preço final, tributos incluídos/destacados, receita líquida, custos, encargos, margem e tratamento de créditos. Futuramente oferecer preço final, receita antes dos tributos sobre consumo ou resultado constante. Separar carga bruta, créditos próprios, líquido devido, carga efetiva, crédito ao cliente, margem, caixa e custo administrativo. Evitar dupla contagem. A menor guia, por si só, não define a vantagem econômica.
- Diferenciar compra potencialmente elegível, crédito apurado, apropriado e compensado. Verificar o direito do adquirente individualmente. Perfil B2B/B2C informa a análise comercial e é insuficiente para confirmar esse direito.

## Premissas e reprodução

Identificar a origem de cada dado como informado pelo usuário, obtido de fonte oficial, derivado, estimado ou não disponível. Manter premissas configuráveis e versionadas fora das regras de cálculo. Por exemplo, quando aplicável, estimar RBT12 por média mensal × 12 e permitir trocar pela série real. Se faltar folha, margem ou crédito, calcular cenários explícitos com parâmetros substituíveis. Os extremos correspondem a cenários calculados. Evitar crédito zero implícito, probabilidade arbitrária e faixa sem cálculo.

Regras e tabelas dependem de território e vigência. Identificar alíquota oficial vigente ou futura já definida, projeção, premissa ajustável e regra pendente de regulamentação. Registrar entradas, premissas, período, fonte legal, versões recuperáveis do software e das bases, arredondamentos, intermediários, resultado, limitações e data. Avaliar entrega do registro ao usuário sem persistência financeira anônima. O lançamento pressupõe validação fiscal independente, com casos de referência e tolerâncias explícitas.

## Distribuição e arquitetura preferida

Aplicação web responsiva, cálculos no servidor. Priorizar monólito modular em Python/Django com templates, HTML, CSS e JavaScript proporcional à necessidade. Isolar núcleo, premissas, serviços de aplicação e adaptadores internos. Futuras páginas públicas especializadas e API devem reutilizar o núcleo. Dimensionar chamadas, latência e concorrência por simulação. Chaves de cache precisam considerar dados, premissas, vigência e versões.

Área profissional e API externa são evoluções posteriores: autenticação, empresas isoladas por usuário, cenários salvos, histórico, importação/exportação, relatórios e integração com ERPs. Freemium é hipótese futura. Docker/Compose e Pytest são preferências para as etapas de implementação. Banco da plataforma, bibliotecas de gráficos, filas, CI e outros serviços dependem de necessidade demonstrada.

Controles previstos incluem validação no servidor, CSRF, XSS, injeção SQL, limites de tamanho e frequência, isolamento, tratamento de segredos, HTTPS, atualização e recuperação. Aplicar minimização de dados, finalidade e retenção compatíveis com LGPD. A disponibilização pública e a contratação de infraestrutura são decisões posteriores.

## Recorte de referência após a 00B

[DECISÃO] A primeira comparação especificada é uma revenda interna convencional do Simples em março/2027, mantendo o preço final e o volume vendidos. A estimativa pode começar por atividade e receita média, com mês e destino adequados. Quando faltarem taxa regular, autorização da opção ou créditos, a saída apresenta fórmula, hipótese ou subtotal identificado. Documentos por item refinam a apuração empresarial. O usuário deve conseguir distinguir custo próprio, potencial crédito do cliente e efeito no caixa. [Exemplo completo](CALCULATION_REFERENCE.md) · [Premissas](ASSUMPTIONS.md) · [Critérios de apresentação](RESULT_STATUS.md)

## MVP interno recomendado na 00C

[DECISÃO] A primeira versão de desenvolvimento entrega a página local (01) e uma experiência de **uma operação** com dados sintéticos (02). O MVP interno (03–05) responde a outra pergunta: “quanto dos meus R$ 100 mil em vendas do mês corresponde a tributos próprios, e o que falta saber para comparar as duas opções?”. A primeira publicação terá a lista de casos aprovados explicitamente por competência e finalidade. A lista pública começa vazia. [Critérios e etapas](ROADMAP.md)

| Dimensão | Cobertura inicial para desenvolver e conferir | Decisão na entrada |
|---|---|---|
| Empresa e atividade | Uma loja, optante do Simples, pelo menos 14 meses de atividade no PA, Anexo I, uma única receita ordinária de revenda de mercadoria nacional adquirida de terceiros | Perguntar abertura se houver dúvida. Empresa nova, filial, caixa de períodos anteriores, serviços, indústria, receitas mistas ou receita não segregável ficam fora da estimativa integral |
| Objeto e documento | Caneta esferográfica comum de escritório nas condições da referência, NF-e 55, NCM 96081000, CST 000, cClassTrib 000001, atividade SN 01, tpRBSN 1, CFOP 5.102 como hipótese do caso | Descrição, destino e condições confirmam o perfil. “Papelaria” ou um código isolado é insuficiente. Outra mercadoria, NFC-e 65 ou benefício exige um novo caso de qualificação |
| Operação e território | Venda onerosa interna e entrega em Florianópolis/SC, IBGE 4205407, estabelecimento na mesma cidade, volume e mix fixos. Compra local do fornecedor regular para revenda na sensibilidade da 00B | Confirmar correspondência ou oferecer o exemplo separado. Excluir interestadual, exportação, ST, monofasia, antecipação, isenção, devoluções, tratamentos especiais e casos com IS controverso |
| Tempo e faixa | Março/2027, RBT12 **maior que R$ 720.000 e até R$ 1.800.000**, faixa 4. Ponto de referência R$ 1,2 milhão de histórico e R$ 100 mil de preço do PA. Toda a faixa é alvo de desenvolvimento, apenas o ponto tem memória completa da referência | Testar fronteiras e requisitos antes de habilitar. Outros meses/faixas só entram após comprovar tabela, janela, territorialidade e casos de fronteira. RBA do ano, receita global e sublimite têm triagem própria. Excesso, transposição ou falta de segregação bloqueiam atribuição integral |
| Regimes e direito à opção | Tradicional e contrafactual com opção conjunta regular de IBS/CBS, demais tributos no SN, mesmo preço e volume. Verificar situação SN, impedimentos, limites, opção vigente no semestre, cancelamentos e ressarcimento | Sem confirmação, só estimativa condicional. Opção intempestiva para o PA retira o regime das alternativas disponíveis. Situação comprovada fica vinculada ao semestre e à referência que a demonstra. Evitar coletar recibos na experiência rápida |
| Entradas e premissas | Preço final das vendas, unidade temporal, descrição e competência para iniciar. Destino e maturidade para aplicar este perfil. Histórico fiscal real ou média explicitamente aceita, mês estável somente sob hipótese, exclusões do preço e taxas de cenário identificadas | Dados reais de compras, regime do fornecedor, eventos de apropriação, perfil dos clientes, saldos, custos e margem entram ao refinar a pergunta correspondente. Folha é dispensável para determinar o anexo deste caso |
| Entregas | Mês, faixa, alíquota efetiva e DAS bruto tradicional, repartição e memória. No híbrido, recálculo da receita, DAS remanescente e débitos por tributo conforme dados. Líquido exige saldos, créditos e extinções. Crédito gerado ao cliente em coluna própria | Exibir parcela conhecida com faltantes. Diferença numérica apenas entre grandezas de mesmo perímetro. Um ano requer trajetória qualificada ou projeção simplificada com condições explícitas. Sem custos, estoque e datas, margem e caixa ficam em aberto |

Entrada inválida impede usar o valor correspondente. Fora do perfil, explicar o limite e permitir explorar o exemplo sintético por escolha. Uma lacuna exclusiva do híbrido preserva o tradicional. Falta de CBS regular definitiva, crédito desconhecido e falta de confirmação da opção têm tratamentos diferentes. O TCU calculou referência de 11,3% e o ensaio utilizou 10% por escolha explícita. O registro C27 da 00B continua sendo o corte utilizado, com mecanismo transitório e vigência a reconsultar para habilitação. [Fontes](TAX_SOURCES.md) · [Premissas](ASSUMPTIONS.md) · [Estados](RESULT_STATUS.md)

Serviços sujeitos ao Fator R, demais anexos, todas as competências até 2033, Lucro Presumido e Real, atividades mistas, importação de DF-e, ERP e área profissional seguem como expansão. Cada habilitação associa objeto, local, documento, período, combinação técnica, referência de cálculo e limites. [Memória do caso](CALCULATION_REFERENCE.md) · [Exclusões](KNOWN_LIMITATIONS.md)

## O que já existe no mercado

[DOCUMENTADO] Consulta em 19/11/2026 a páginas dos próprios fornecedores. A facilidade abaixo é inferida dos campos e do percurso divulgado. A pesquisa não incluiu contratação, envio de dados empresariais, auditoria dos algoritmos ou teste de usabilidade.

| Referência e acesso | O que o usuário precisa saber | Resultado, transparência e fricção observável |
|---|---|---|
| Calculadora de Tributos da Receita, beta aberta, simulador web. Cadastro na conclusão do fluxo não aferido | Dados da operação, local, item, classificação e base | Memória e fundamento por operação. Responde bem a uma questão documental, exige conhecimento da mercadoria. [Apresentação oficial de julho/2025](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2025/julho/receita-federal-libera-ferramenta-oficial-de-calculo-da-reforma-tributaria-sobre-o-consumo) · [Contratos examinados](API_INTEGRATION.md) |
| Simulador da Reforma do Sebrae, gratuito. O link do anúncio conduziu à entrada da conta AMEI | CNAE, faturamento, perfil de vendas | Compara dois caminhos e estima créditos transferíveis aos clientes. Linguagem voltada ao pequeno negócio. O anúncio qualifica o resultado como preliminar. Fórmulas e versões internas não foram examinadas. [Sebrae, 21/08/2026](https://agenciasebrae.com.br/economia-e-politica/simulador-da-reforma-tributaria-ja-esta-disponivel-no-portal-sebrae/) |
| Comparador da Graph, página anuncia uso sem cadastro e cálculo no navegador | Faturamento, histórico RBT12, anexo e custos | Cenários lado a lado, DRE e alíquota efetiva. A página explica a faixa e chama a taxa futura de estimativa. O preenchimento pressupõe saber o anexo. [Simulador da Graph](https://graphcontabilidade.com.br/simulador-simples-nacional/) |
| Omie, módulo do ERP acessado após login | Cenário fiscal da empresa, tributos por NCM, CST e classificação | Cadastro reutilizado em pedidos, notas e consultas. A configuração por produto fica visível ao operador e exige preparação fiscal. [Regras do ERP](https://ajuda.omie.com.br/pt-BR/articles/10947561-configurando-uma-regra-geral-de-tributacao) · [IBS e CBS no Omie](https://ajuda.omie.com.br/pt-BR/articles/13291407-configurando-o-ibs-e-o-cbs-no-omie) |
| Econet SPTE, acesso demonstrativo solicitado ao fornecedor | Período, UF, receita anterior, receitas, deduções, custos e despesas | Planejamento em vários regimes, bases detalhadas, memória e relatórios gerenciais. Maior preparação, especialmente para lucro. Avaliação limitada ao tour. [Tour do SPTE](https://lp.econeteditora.com.br/spte-teste-simulador-de-planejamento-tributario/) · [Catálogo Econet](https://www.econeteditora.com.br/solucoes.php?anchor=ferramentas) |

[HIPÓTESE] Vale testar se o gestor consegue começar pelo preço que o cliente paga e perceber por que créditos desconhecidos deixam o líquido aberto. Para o contador, o valor proposto é conseguir trocar a média pela série da competência e explicar cada diferença com a revisão exata. Comparação, memória e estimativas de crédito já aparecem na amostra. O teste da 05 observará se essas duas tarefas funcionam com o nosso recorte. [Jornada e protocolo de uso](WEB_EXPERIENCE.md)
