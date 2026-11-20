# Roadmap

**Posição em 19/11/2026.** A 00C concluiu o planejamento da arquitetura, do MVP interno e da primeira página. **A Fase 01 está tecnicamente pronta e aguarda autorização do titular.** O daemon Docker indisponível condiciona o ensaio de containers. As referências fiscais de março/2027 e a revisão profissional condicionam a liberação por recorte.

## Abertura da Fase 00C · 19/11/2026

[DECISÃO] O titular autorizou exclusivamente o planejamento da arquitetura, da experiência e das fatias de implementação. O objetivo é permitir que uma nova conversa inicie a fundação web após autorização própria. [EXECUTADO] Na abertura, `git status --short --branch` retornou apenas `## main...origin/main`. O comando `git log -8 --oneline --decorate` mostrou HEAD e origin/main em `bb39b72` (00B), precedido de `99fc807` (00A). A fase dependeu das evidências dessas revisões, da operação sintética de março/2027 e do catálogo de 21 casos.

Plano: delimitar cobertura e pesquisar interfaces e versões, desenhar jornada e contratos, escolher execução local e fronteiras dos motores, vincular testes e bloqueios às fatias e revisar o plano executável da 01. Riscos: extrapolar a revenda, misturar hipótese e incidência, perder o replay, exigir Docker ou homologação cedo demais. Aceite: cinco documentos de projeto, decisões reconciliadas com 00A/00B, roadmap e casos vinculados, checagem de links, exemplos e preservação das evidências. A implementação da 01 e a publicação dependem de novas autorizações.

| Fase | Entrega e critério de conclusão | Estado |
|---|---|---|
| 00A · Motores oficiais | Identificar revisões e contratos, executar operações e erros por motor, registrar cobertura, serviço interno, testes, limitações e questões para a matriz. | Concluída no escopo investigativo |
| 00B · Matriz, metodologia e riscos | Atribuir responsabilidades, reconciliar operação e empresa, delimitar créditos, fontes, comparação e riscos. | Concluída no escopo metodológico |
| 00C · Arquitetura, produto e planejamento | Delimitar recorte, pesquisar ofertas, desenhar jornada e arquitetura mínima, vincular os casos de teste e preparar a 01. Validação com usuários prevista na 05. | Concluída no escopo de planejamento |
| 01 · Fundação web | Django mínimo, página inicial funcional no navegador, ambiente reproduzível, testes e documentação. | Pronta para iniciar mediante autorização |
| 02 · Primeira operação | Formulário, validação, adaptador interno, cálculo oficial, erros e resultado rastreável de um caso suportado. | Planejada |
| 03 · Simples rápido | Estimativa mensal e anual para perfis definidos, sem cadastro, com premissas, RBT12, anexos e memória. | Planejada |
| 04 · Tradicional e híbrido | Comparar opção de IBS/CBS regular com recolhimento tradicional em bases consistentes, incluindo demais parcelas, créditos e elegibilidade. | Planejada |
| 05 · Consolidação do MVP | Refinar cenário sem recadastro, demonstrar sensibilidade, validar cálculos e avaliar interface, segurança e desempenho. | Planejada |
| 06 · Primeira publicação | Escolher hospedagem, configurar domínio/HTTPS, rede privada, limites, monitoramento, atualização, privacidade e recuperação. Depende de validação profissional e autorização de publicação. | Planejada |
| Expansão do Simples · Serviços | Após consolidar a revenda e antes de ampliar para LP, qualificar primeiro serviço, local, folha paga e fronteira III/V. Cobertura por anexo e depois mistos. Independente de a 06 já ter publicado. | Planejada, autorização própria |
| 07 · Lucro Presumido | Acrescentar apuração e comparação verificadas para os perfis cobertos. | Planejada |
| 08 · Lucro Real | Acrescentar apuração e comparação verificadas com os insumos contábeis necessários. | Planejada |
| 09 · Planejamento avançado | Projetar até 2033 conforme vigências, simular sensibilidade, pontos de mudança, preços e impactos financeiros. | Planejada |
| 10 · Plataforma profissional | Autenticação, isolamento entre empresas, permissões, histórico, importação, relatórios e cenários avançados. | Planejada |
| 11 · Integrações e expansão | APIs externas e ERPs. Avaliar monetização, assinaturas, novos canais e PWA conforme necessidade. | Planejada |

## Aceite da 00A

| Critério da investigação | Evidência |
|---|---|
| Versões, objetivos, licenças, granularidade, cobertura e limites dos dois motores e triagem de DANFSe | [Relatório técnico](OFFICIAL_ENGINES.md) |
| Contratos, entradas indispensáveis, dados derivados, estados, alíquotas e créditos | [Integração](API_INTEGRATION.md) |
| Execução local e sem dependência remota de cálculo, classificações, operação válida e inválida, períodos e concorrência | [Regular](evidencias/00a/regular.json) · [Simples](evidencias/00a/simples.json) |
| Recursos, instalação, dependências, testes oficiais e recuperação de versões | [Infraestrutura](INFRASTRUCTURE.md) · [Inventário](evidencias/00a/inventario.json) · [Restauração de duas bases](evidencias/00a/replay.json) |
| Divergências, limitações de 2027, validação profissional e trabalhos para a matriz | [Pendências](RISKS_AND_OPEN_QUESTIONS.md) · [Decisões](DECISIONS.md) |

## Aceite da 00B

| Critério | Entrega e condição |
|---|---|
| Objetivo, plano, dependências e riscos da abertura | [Registro de abertura](evidencias/00b/PLANO.md) |
| Responsáveis, legislação, parâmetros de 2027 e apuração | [Matriz](TAX_RESPONSIBILITIES.md) · [Fontes](TAX_SOURCES.md) · [Catálogo](TAX_PARAMETERS.md) · [Regras](TAX_RULES.md) |
| Memória e confronto dos motores | [Revenda e segundo perfil de serviços](CALCULATION_REFERENCE.md) · [Experimento e fontes técnicas](evidencias/00b/FONTES_TECNICAS.md) |
| Estimativa rápida, estados e validação | [Premissas](ASSUMPTIONS.md) · [Estados e qualificação das combinações](RESULT_STATUS.md) · [Cenários de teste](TEST_SCENARIOS.md) |
| Divergência V0058/V0059, IS e bloqueios | [Exclusões](KNOWN_LIMITATIONS.md) · [Registro vigente de riscos](RISKS_AND_OPEN_QUESTIONS.md) |

### Perguntas deixadas pela 00B à 00C (registro histórico)

1. Confirmar o primeiro recorte e o resultado que o usuário pode obter só com dados agregados. Definir quando solicitar descrição do item, opção, histórico ou compras.
2. Especificar as fronteiras entre entrada econômica, motor por operação, apuração empresarial, catálogo versionado e planejamento. Definir a semântica de estado e o formato mínimo exportável de replay.
3. Escolher casos prioritários para homologação, profissional responsável e referência do PGDAS/conta assistida para março de 2027. Decidir o que pode ficar restrito a simulação hipotética até haver fonte aplicável.
4. Definir atualização e qualificação de atos, notas, tabelas e combinações de JAR/base, orçamento de chamadas e comportamento em indisponibilidade.

A escolha de arquitetura, a implementação e a disponibilização pública permanecem etapas com autorizações próprias.

## Fatias autorizáveis após a 00C

| Fase | Objetivo | Escopo | Dependências | Entregáveis | Testes | Critérios de conclusão | Bloqueios |
|---|---|---|---|---|---|---|---|
| 01 | Abrir a plataforma no navegador | Uma página local do perfil em pt-BR | Autorização 01, Python, Git e pacotes | Django + templates, venv, testes e README | Instalação limpa, GET/HEAD, 404, settings, CSS, móvel e teclado | Outro checkout inicia e abre a página pelos comandos documentados, com evidência por SO | Para começar, autorização. Java, Docker e parâmetros futuros dispensáveis |
| 02 | Mostrar uma operação até o retorno real | C03, um item da 00B no regular 1.6.1/V0059 com taxa hipotética explícita | 01 e autorização 02, JAR/base íntegros, Java 21 | Formulário, validação, adaptador privado, item, estado e memória no navegador | C03, C15, C16 como exclusão, C20; E2E real e tentativa de Compose Linux | Reproduzir resposta e falhas localizadas no navegador, demonstrar resultado simulado. Registrar separadamente ambiente nativo e container | Falta do motor impede o aceite E2E. Docker ausente deixa pendência de container, permite a prova nativa |
| 03 | Responder ao gestor para o Simples tradicional | Revenda e faixa delimitadas, março/27, estimativa anual simplificada só sob as hipóteses da 00B | 02 técnica e autorização 03, referências legais e política de histórico/centavos | RBT12, faixa e DAS mensal, catálogo inicial, origem da média, memória e formulário | C01, C10–C14, C17 e C21; triagem de C08/C09 | Série real e estimada se distinguem; janela deslocada e fronteiras corretas, teste sem Java e bloqueio fora do recorte | PGDAS futuro bloqueia homologação da guia. Falta de histórico aceito bloqueia apenas a faixa exata ou a estimativa que dependa dele |
| 04 | Comparar tradicional e híbrido | Mesmo preço e volume, receita fiscal recalculada, DAS remanescente, débitos, créditos e saldos mensais | 03 e autorização 04, regra da opção, parâmetros identificados e hipóteses quando necessárias | Dois cenários em perímetro comum, totais condicionais e componentes abertos, memória por tributo | C02–C07, C14, C17–C20, isolamento de crédito do cliente e prazo | Reproduzir a sensibilidade da 00B só sob as hipóteses nomeadas, impedir ranking se parcial, indicar possível efeito de refinar | CBS definitiva, direito a crédito e prova de opção bloqueiam o respectivo resultado confirmado. Desenvolvimento por fórmulas e hipóteses continua |
| 05 | Consolidar MVP interno | Refinamento progressivo, reprodutibilidade, qualificação e operação | 04 e autorização 05, instalação de ensaio e casos sintéticos | Jornada completa móvel/desktop, manifesto reproduzível, relatório separado de homologação/pendências | Regressão dos casos do recorte, UI com usuários, E2E, segurança, Linux/Compose, carga e restauração | Registrar recortes liberáveis, parciais e retirados. Aceite operacional requer container e recuperação. MVP pode ficar experimental interno com pendência fiscal explícita | Falta de referência/profissional impede promoção fiscal, falha de segurança/infra impede publicação |
| 06 | Primeira disponibilização controlada | Apenas funcionalidades e competências aprovadas, oferta pública posterior por decisão | 05, aceite fiscal do que for oferecido, licenças, privacidade, capacidade e autorização específica | Deploy controlado, rede privada, HTTPS, operação, monitoramento e rollback | Exercício no destino, revisão de logs/limites, restauração independente, rechecagem do escopo publicado | Publicar os recortes com revisão profissional registrada e aprovação do titular, monitorar e poder retirar caso isolado | Sem referências essenciais ou autorização, permanece interna. Contratação e publicação são decisões próprias |

[DECISÃO] A primeira operação usa o regular porque C03 tem resposta capturada com um único item e dispensa alíquotas efetivas do SN determinadas pela apuração empresarial. Serviços entram depois da estabilização da revenda: o segundo perfil exige outro documento, local de incidência, folha paga, correlação NBS e fronteira do Fator R. As fases 07–11 preservam os rumos anteriores, inclusive projeções até 2033, análises avançadas, histórico profissional, ERP e hipótese de monetização. [Planejamento dos testes por ID](TEST_SCENARIOS.md)

## Estágios de uso e critérios de liberação

| Estágio | Quem usa e qual evidência permite passar |
|---|---|
| Desenvolvimento local | Engenharia com fixtures sintéticas. Aceite de software por fase. Faltas fiscais futuras ficam vinculadas à pergunta que impedem responder |
| MVP interno | Equipe avalia o fluxo integrado de ambas as opções, com resultados parciais, capacidade medida e limites visíveis por caso |
| Versão experimental | Participantes e finalidade delimitados, por autorização. Pode explorar histórico médio, taxa de CBS escolhida e sensibilidades de crédito ao mesmo preço. Mostrar a hipótese junto a cada valor. Manter a elegibilidade condicional. Qualquer exposição externa ainda requer autorização, revisão do material, privacidade e infraestrutura |
| Homologação tributária | Profissional a designar confronta entradas e competência idênticas com PGDAS e contas assistidas disponíveis, atos vigentes, DF-e e eventos. Reconciliar créditos, compensações, repartições e resíduos de centavos por tributo. Registrar tolerância, diferenças, fontes, versão, parecer e responsável por recorte. Março/2027 é dependência futura |
| Publicação controlada | Titular autoriza expressamente público, escopo e finalidade. Verificar última edição normativa, CBS aplicável, elegibilidade, créditos, licenças de distribuição, segurança e privacidade, runtime Linux, testes, capacidade, monitoração e restauração no destino. Publicar somente o que satisfaz seu nível de evidência |
| Produto público | Ampliar público e recortes após resultados do piloto, revisão dos incidentes e nova decisão de liberação. Manter lista pública de cobertura e limitações por data, canal de correção e retirada por caso |

Um explorador hipotético externo poderia, sob aprovação, permitir variar uma taxa ou um histórico de exemplo e observar o efeito aritmético. Requer revisão da apresentação e de seus limites e deixa a rubrica “apuração fiscal homologada” desabilitada. Qualquer recomendação para uma empresa depende de elegibilidade comprovada, bases equivalentes e escopo validado. O titular ainda não designou profissional nem autorizou essas liberações.

## Aceite de planejamento da 00C

| Pergunta de encerramento | Registro para a implementação |
|---|---|
| Quem começa, qual produto/mercado e quais limites? | [Recorte, pesquisa e personas](PRODUCT_SPEC.md), [jornada, wireframes e estados na tela](WEB_EXPERIENCE.md) |
| Como decompor, integrar e reproduzir? | [Arquitetura e tecnologias](ARCHITECTURE.md), [dados, catálogo e snapshots](DATA_MODEL.md), [política dos motores](API_INTEGRATION.md) |
| Como desenvolver, testar e hospedar? | [Plano executável da 01](PHASE_01_PLAN.md), [ensaios, metas e hospedagem](INFRASTRUCTURE.md), [testes](TEST_SCENARIOS.md) |
| O que impede promoção? | [Segurança e privacidade](SECURITY.md), [registro de riscos por etapa](RISKS_AND_OPEN_QUESTIONS.md) e [decisões de curadoria](DECISIONS.md) |

[DECISÃO] A 00C encerra a etapa de planejamento. Próxima entrega executável: fundação web local da 01, sujeita à autorização do titular.

### Conferência de encerramento · 19/11/2026

[EXECUTADO] No Windows, `python -` com leitura UTF-8 da raiz e de `docs/` verificou os 26 arquivos Markdown, 249 ocorrências de links locais, 64 tabelas com largura consistente e o fechamento dos blocos de código. A verificação comparou a sequência C01–C21 do catálogo com a da matriz de fases, interpretou os dois exemplos JSON do modelo de dados e confrontou preço, DAS, alíquota efetiva e taxa remanescente com `docs/evidencias/00b/reference.json` em aritmética decimal. Também conferiu as cinco dimensões nos dois cenários e na comparação, total híbrido e diferença ausentes e lista de motores vazia no caminho agregado. Retorno 0.

[EXECUTADO] `rg -c '^\| C[0-9]{2} \|' docs/TEST_SCENARIOS.md` retornou 42 linhas de caso (21 no catálogo e 21 na atribuição por fase). `git diff --check` retornou 0. `git diff --exit-code bb39b72 -- docs/evidencias scratch docs/CALCULATION_REFERENCE.md docs/TAX_SOURCES.md docs/TAX_RULES.md docs/TAX_PARAMETERS.md` retornou 0, sem diferenças. `git ls-files --others --exclude-standard` listou apenas os cinco documentos pedidos. As sondas do ambiente e a falha do daemon estão no caderno de infraestrutura. Testes web, execução de containers, pesquisa com usuários e homologação fiscal pertencem às fases de implementação.
