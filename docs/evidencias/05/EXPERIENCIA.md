# Experiência do gestor e do contador

## Auditoria técnica de 21/11/2026

[EXECUTADO] Chrome 157.0.8103.79 e Playwright 1.65.2 no Windows, com backend nativo e depois em Compose. Os [roteiros de navegador](../../../tests/browser) partem da página inicial e usam formulários reais. O Chrome operou sem JavaScript da aplicação a 1366 × 900 e 320 × 720. O ensaio complementar de acessibilidade usa altura de 800 px. Os comandos de repetição estão no [relatório](../../PHASE_05.md).

| Critério observado | Método, resultado e limite |
|---|---|
| Início, campos e hipóteses | Entrar pelas três ações da home com Tab/Enter. O comparador abre sem CBS ou exclusões preenchidas. Escolher um exemplo identifica sua origem, inclusive após edição. Corrigidos a promessa de estimar a guia na home, o rótulo da origem do histórico e a redação da CBS de cenário. |
| Teclado e ordem de leitura | Percurso de C03 até confirmação, resultado e memória. Percursos de média, histórico real, correção e exclusão de serviço no tradicional e no comparador. Com todos os grupos do comparador abertos, o ensaio percorre os links e controles visíveis por Tab em ordem de documento. Há um h1 por página. Os títulos de resultado e de erro recebem o foco. |
| Nomes, agrupamentos, erros | Verificados nomes acessíveis dos controles visíveis. O tradicional usa fieldset/legend, o comparador usa grupos expansíveis com summary. O resumo repetia o ID do erro de CBS e exibia a chave interna. Depois da correção há uma mensagem vinculada ao campo, o grupo abre e o link do resumo leva o teclado ao campo. |
| Estados e valores | A revenda retorna R$ 10,10 simulados. Ao parar a JVM, o mesmo formulário explica a falha. No comparador, apagar um crédito mantém o bruto visível e deixa a comparação após créditos em aberto. Estado, elegibilidade e titular do crédito têm texto próprio. A inspeção visual do exemplo intermediário em 320 px conferiu ordem tradicional → híbrido e legibilidade de RBT12, DAS e obrigações. |
| Refluxo e ampliação | Os roteiros verificam largura do documento após POST. A tabela do tradicional mostra rótulos por rubrica no celular. A ampliação CSS de 200% a 1366 px expunha largura de 1491 px na home. Permitir quebra da palavra longa na introdução evitou a rolagem. Também se conferiram as quatro páginas a 320 px. Zoom CSS é a técnica ensaiada. Zoom nativo em outros navegadores e gestos em aparelho físico continuam sem prova. |
| Contraste e foco | Cálculo pela luminância relativa sRGB das cores da folha local. Texto/cor de fundo principal 8,50:1, botão branco/verde 8,92:1, erro/branco 9,12:1, texto secundário do perfil 8,47:1, borda de campo/branco 3,40:1. Contorno de foco sobre branco 6,00:1 e sobre o grupo claro 5,14:1. A sonda verificou o contorno do primeiro foco nas quatro páginas. Amostra de pares e estados. |
| Tecnologia assistiva | Nomes, foco e relações de erro foram consultados na semântica exposta pelo Chrome. Acompanhamento com leitor de tela, compreensão auditiva, contraste forçado, outros navegadores e avaliação integral WCAG 2.2 AA permanecem pendentes. |

## Protocolo de observação humana

**Não executado.** Não havia participantes humanos disponibilizados e autorizados. Resultados por pessoa e tempos de realização estão em branco. [DECISÃO] Convidar gestor de comércio e contador/consultor com autorização específica. Explicar finalidade, consentimento e descarte, usar estação ou navegador limpo e entregar os mesmos dados fictícios. Evitar nomes, identificação empresarial, documentos reais e gravação desnecessária. Alternar a ordem de desktop e celular entre sessões. O moderador lê a tarefa sem explicar o caminho. Cronometrar do fim da instrução até o participante explicar o resultado. Registrar ajuda somente após tentativa espontânea.

| Tarefa | Persona e entrada entregue | Evidência observável de conclusão sem ajuda |
|---|---|---|
| Iniciar e obter a estimativa mensal | Gestor. Loja aberta em 2023, revenda comum local, março de 2027, preço e média fiscal R$ 100 mil. | Escolhe a calculadora tradicional, aceita a média e reconhece R$ 8.825,00 como DAS bruto. Explica por que o valor efetivo da guia ainda está aberto. |
| Explicar de onde vieram os 12 meses | Ambos. Partir da estimativa anterior. | Identifica média estimada e janela fev/26–jan/27. Consegue mostrar onde verificou a origem. |
| Refinar sem recadastro | Contador. Entregar os 12 meses com fev/26 = R$ 80 mil e demais de R$ 100 mil. | Localiza a série, preserva a receita de março, lê RBT12 de R$ 1,18 mi e DAS de R$ 8.793,22. |
| Explicar uma comparação incompleta | Gestor. Explorar o exemplo intermediário e depois apagar o crédito de CBS. | Distingue exemplo e dados próprios, reconhece a hipótese de CBS de 10%, identifica o bruto conhecido, a parcela que falta e o motivo de a diferença líquida ficar aberta. |
| Alterar uma premissa e explicar quem se beneficia | Ambos. Restaurar crédito elegível de CBS R$ 1.500 e IBS R$ 15. Alterar o perfil do comprador. | Lê R$ 14.202,31 após créditos no exemplo. Localiza o crédito do cliente em seção própria e explica a diferença entre potencial e utilizado sem subtraí-lo da loja. |
| Conferir opção e base legal | Contador. Pedido ordinário em março e recibo não confirmado. | Encontra a janela de julho, fontes, composição do DAS remanescente, edição e memória. Explica por que a hipótese não prova elegibilidade no PA. |
| Distinguir item e mês, identificar exclusão | Gestor. Testar a caneta e depois informar serviço na apuração empresarial. | Reconhece base de R$ 100,00 e tributos de R$ 10,10 do item, encontra a explicação de fora da cobertura para serviço e evita concluir uma carga mensal a partir do item. |

**Ficha por tarefa** — código anônimo da sessão, persona, dispositivo, largura, recurso assistivo escolhido, revisão do produto, tarefa, conclusão (sim/parcial/não), ajuda (nenhuma/pista/demonstração), tempo, interpretação nas palavras da pessoa, confusão específica e impedimento observado. Sem dados financeiros livres. Consolidar contagens por tarefa e dispositivo, preservando divergências entre as duas personas.

[DECISÃO] Priorizar uma nova iteração se alguém interpretar hipótese como regra oficial, subtotal como guia, cliente como titular da conta da loja ou se perder o histórico ao refinar. Rever rótulo ou sequência no ponto da confusão e repetir a mesma tarefa. Registrar o que foi observado e o que se alterou antes de considerar o critério de compreensão atendido.
