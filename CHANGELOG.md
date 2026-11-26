# Histórico de alterações

## 24/11/2026 · Primeiro serviço do Simples Nacional

[CÓDIGO][EXECUTADO] Jornada local para desenvolvimento de software sob encomenda, com FS12, RBT12r, Fator R, Anexos III/V, DAS e repartição de março/2027. O C08 inclui dois replays da fronteira, regressão da revenda e teste móvel sem JavaScript. [Relatório de serviços](docs/SIMPLES_SERVICES_01.md)

## 21/11/2026 · Consolidação do MVP interno

[CÓDIGO][EXECUTADO] Corrigidos o atalho de exemplo com campo duplicado, o vínculo de erros, a leitura do DAS bruto, a identificação da CBS hipotética e o refluxo da página inicial ampliada. As três jornadas passaram por regressão, navegador, carga controlada e recuperação em Windows e Compose. A matriz C01–C21 e o dossiê orientam o confronto fiscal posterior. O JAR preservado contém uma revisão do Tomcat abrangida por avisos de segurança. A prontidão se limita a ensaio local sintético. [Resultados, bloqueios e reprodução](docs/PHASE_05.md)

## 20/11/2026 · Comparador mensal da Fase 04

[CÓDIGO][EXECUTADO] A loja pode comparar as obrigações de março sob o mesmo preço e volume, informar históricos fiscais próprios e examinar as contas separadas de IBS e CBS. As três sensibilidades reproduzem a referência da 00B. O cálculo agregado funciona sem JVM, conserva os dados durante o POST e permite replay local. [Relatório da fase](docs/PHASE_04.md)

## 20/11/2026 · Estimativa empresarial da Fase 03

[CÓDIGO][EXECUTADO] Nova calculadora do Simples tradicional no navegador, com histórico estimado ou real, catálogo local fixado por revisão, triagem anual e memória reproduzível. C01 retornou R$ 8.825,00 de DAS bruto. A soma das rubricas exibidas excede o total global em R$ 0,01. A entrega preserva a apuração da caneta da Fase 02. [Relatório, comandos e evidências](docs/PHASE_03.md)

## 20/11/2026 · Operação real da Fase 02

- [CÓDIGO] A página inicial dá acesso ao exemplo C03. O formulário exige confirmação da CBS hipotética e apresenta os valores, as cinco dimensões de estado e a memória da revenda.
- [EXECUTADO] O regular 1.6.1/V0059 reproduziu o corpo da 00B no Windows e em containers Linux. As provas incluem NF-e 55 separada, lote parcial, exclusão offline de 820001, falhas de contrato, indisponibilidade e recuperação no navegador.
- [DECISÃO] Ensaio interno local, com mTLS entre backend e JVM. Revisão fiscal e autorização de fases seguintes permanecem pendentes. [Execução e comandos](docs/PHASE_02.md)

## 20/11/2026 · Fundação web local da Fase 01

- [CÓDIGO] Entregue a rota inicial Django com a apresentação do perfil de revenda, a comparação futura e navegação por âncora. A página usa um template e uma folha CSS local.
- [EXECUTADO] Reprodução em checkout e ambiente virtual novos no Windows, oito testes aprovados e verificação no Chrome com teclado e JavaScript desativado em 1366 e 320 px.
- [DOCUMENTADO] Configuração por ambiente, dependências fixadas e comandos nos dois sistemas. A execução nativa em Linux permanece pendente.

[Iniciar a aplicação](README.md#executar-localmente) · [Registro de aceite](docs/PHASE_01_PLAN.md#encerramento--20112026)

## 19/11/2026 · Arquitetura web, experiência e planejamento 00C

- Delimitado o primeiro MVP interno à revenda de referência. Pesquisa de cinco ofertas públicas orientou uma entrada por preço final, com refinamento e memória por competência.
- Definidos monólito Django, contratos decimais, catálogo JSON versionado, hipóteses separadas, manifesto por execução, adaptadores privados e política para calcular e descartar os dados anônimos.
- Desenhados wireframes para computador e celular, testes por fase vinculados aos 21 casos, critérios de publicação por recorte, metas de desempenho e alternativas de hospedagem.
- Conferido ambiente Windows. Python 3.14.0 e JDK portátil disponíveis. O cliente Docker 28.5.1 e Compose responderam; a conexão ao daemon falhou. A fundação local independe dos motores.
- Entregue plano executável da 01, pendente de autorização. Homologação de março/2027, qualificação de containers e restauração fora da estação permanecem pendentes.

[Arquitetura](docs/ARCHITECTURE.md) · [Plano da 01](docs/PHASE_01_PLAN.md) · [Roadmap](docs/ROADMAP.md)

## 19/11/2026 · Matriz tributária e metodologia 00B

- Delimitadas a apuração mensal do Simples tradicional e a opção semestral por IBS/CBS regulares. Mapeadas as responsabilidades, as fontes, os parâmetros de 2027, os eventos de crédito e os limites de comparação.
- Documentada a revenda sintética de março em Florianópolis, com DAS bruto estimado de R$ 8.825,00, memória por tributo, DAS remanescente condicional e três cenários de crédito. Proposto segundo perfil sujeito ao Fator R.
- Executados dois POSTs em combinações preservadas, conferida a repartição com aritmética decimal e examinados os leiautes NF-e/NFS-e e as migrações posteriores em clone separado. A NFS-e 820001 foi excluída da cobertura empresarial.
- Definidos estados independentes, registro de replay, 21 casos de referência e condições para apresentação e validação. A próxima fase aguarda autorização.

[Memória e resultados](docs/CALCULATION_REFERENCE.md) · [Riscos](docs/RISKS_AND_OPEN_QUESTIONS.md) · [Roadmap](docs/ROADMAP.md)

## 19/11/2026 · Inicialização documental e investigação 00A

- Registradas a visão de produto, as instruções permanentes e as etapas até a expansão profissional.
- Investigados os motores regular 1.6.1 e Simples 0.0.6. Preservadas as entradas e respostas HTTP sintéticas, as medições locais e os hashes de fontes, JARs e bases.
- Registradas duas falhas da suíte do Simples em V0059 para a classificação 820001 e o controle com V0058. Documentadas as condições do cálculo de 2027, os limites dos créditos e a necessidade de apuração empresarial própria.

[Relatório](docs/OFFICIAL_ENGINES.md) · [Pendências](docs/RISKS_AND_OPEN_QUESTIONS.md) · [Roadmap](docs/ROADMAP.md)
