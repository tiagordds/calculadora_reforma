# Experiência da calculadora rápida

[EXECUTADO] O comparador usa um formulário comum com refinamentos expansíveis. Em desktop, as trajetórias ocupam duas colunas. A 320 px elas seguem em sequência. O resultado parcial indica o dado a refinar. As três sensibilidades exigem seleção deliberada do exemplo pela pessoa usuária. [Telas e roteiro em navegador](PHASE_04.md)

[EXECUTADO] A página inicial agora abre a revenda C03. O formulário identifica a base e o preço final desconhecido e exige confirmação da CBS. O POST posiciona o foco no título do resultado. No Chrome, Tab e Enter abriram a memória e o replay com JavaScript desligado nas duas larguras. [Sucesso em desktop](evidencias/02/sucesso-1366.png) · [Falha em 320 px](evidencias/02/indisponivel-320.png)

[DECISÃO] O gestor começa com o preço da venda e chega à primeira estimativa sem cadastro. O contador pode abrir a memória, conferir a janela de receitas e substituir uma premissa sem redigitar o cenário. O percurso principal cabe em uma página de formulário e resultado. Um POST devolve a página com os dados informados, os resultados e as próximas perguntas, inclusive com JavaScript desativado. Na 01, só a apresentação inicial estará disponível. [Cobertura do produto](PRODUCT_SPEC.md)

## Da primeira visita à primeira estimativa

1. **Começar.** A página informa que o primeiro perfil é uma loja do Simples que revende a mercadoria comum descrita e entrega em Florianópolis. A escolha “Explorar o exemplo de março de 2027” abre dados sintéticos identificados. O caminho “Simular minhas vendas” começa com valores em branco.
2. **Informar vendas.** Perguntar “Quanto seus clientes pagam pelas vendas, com os impostos já incluídos?” e “Esse valor é do mês escolhido, uma média mensal ou o total de um ano?”. Usar reais, com exemplo de formato fora do campo. Para total anual, dizer qual ano foi informado, mostrar a divisão por 12 e pedir aceite antes de usar a média. Receita fiscal já conhecida tem campo rotulado no refinamento. Preço, receita fiscal e base da operação têm origens próprias.
3. **Identificar o caso.** Selecionar atividade em linguagem comum, mês/ano editável e confirmar origem/destino se necessário para identificar o perfil. Ex.: “Revendo canetas esferográficas comuns compradas no Brasil”, “Minha loja e as entregas ficam em Florianópolis”. Opções para “Outra mercadoria ou atividade” e “Não sei informar”. Confirmar venda comum sem tratamento especial e se a empresa já estava no 14º mês de atividade ou além no mês escolhido. Perguntar mês de abertura se isso mudar o enquadramento.
4. **Entregar o que já é possível.** Se a pessoa escolher “Utilizar uma estimativa”, mostrar qual valor de receita fiscal será assumido nos 12 meses da janela e para qual cenário. Se os dados não distinguirem o perfil real, apresentar o que falta ou permitir explorar o exemplo. Para calcular o DAS bruto do perfil homogêneo dispensar compras, folha e perfil dos clientes.
5. **Refinar pela pergunta do usuário.** Para conhecer o híbrido, perguntar pela opção em vigor, composição do preço, exclusões e, se desejado, taxa exclusivamente hipotética. Para chegar ao líquido, perguntar por créditos apropriados de cada tributo no mês, saldos e extinções, ou detalhar fornecedor e eventos. Para efeito no cliente, perguntar regime/finalidade. Para margem e caixa, pedir custos, estoque, datas e encargos. Cada resposta volta ao servidor e mantém os campos anteriores na aba.

A próxima pergunta segue uma ordem verificável: primeiro o fato que decide se o caso cabe no produto ou o regime era possível naquele semestre, depois o dado que destrava a grandeza solicitada. Entre premissas substituíveis, priorizar a que produzir a maior diferença em reais **entre ramos já calculados com as mesmas demais entradas**. Se não houver extremos fundamentados, explicar a dependência sem estimar um impacto numérico. Essa prioridade não exige pontuação opaca nem taxas setoriais presumidas.

## Wireframes do percurso

[HIPÓTESE] Textos e valores ilustram a memória sintética da 00B. Os rótulos de estimativa, subtotal e opção condicional integram os cartões, inclusive em tela estreita. [Caso de março](CALCULATION_REFERENCE.md)

**Página inicial e entrada no computador**

```text
Simulação tributária
Veja como uma venda entra na carga mensal da empresa.
Cobertura inicial   Revenda interna comum · Florianópolis · março de 2027
[Simular minhas vendas]       [Explorar o exemplo de março de 2027]

Calculadora rápida
O que a empresa vende?                  [Escolher atividade                 v]
Quanto os clientes pagam pelas vendas?  R$ [           ] [Mês / Média / Ano v]
Para qual mês?                          [03/2027 v]
Onde ficam a loja e a entrega?          [Florianópolis/SC v] [Outro] [Não sei]
[Conferir meu perfil]       [Utilizar uma estimativa]       [Informar valores reais]
```

A confirmação curta revela apenas os fatos do perfil que ainda faltam. Sugerir o mês do único exemplo e expor sua cobertura; a escolha de outro mês retorna orientação antes de pedir mais dados. Quando a aba já tiver dados reais, a mudança para o exemplo conserva a distinção entre as duas origens.

**Resultado e comparação no computador**

```text
Março de 2027 · Exemplo sintético · R$ 100.000,00 pagos pelos clientes
                              Tradicional                  Com IBS/CBS regulares
Estimativa mensal             R$ 8.825,00 · DAS bruto       Total em aberto
Alíquota efetiva do DAS       8,825% da receita fiscal      Ver DAS remanescente
Projeção anual                Ver condições                 Faltam meses e opções
Opção da empresa              Situação a confirmar          Situação a confirmar

Preço e volume mantidos. No híbrido, a receita fiscal muda com o tributo da venda.
Faltam taxa da CBS, composição do preço e créditos do mês para o líquido.
[Explorar outros cenários]    [Informar os valores reais]

▸ Composição do DAS e tributos regulares       ▸ Créditos da empresa e do cliente
▸ Premissas e limitações                       ▸ Memória, fontes e versões
```

**Refinamento, premissas e memória**

```text
Refinar o histórico
Receitas fiscais usadas para a faixa de março · fev/2026 a jan/2027
Estimativa atual   R$ 100.000,00 em cada mês
[Informar a série mês a mês]   [Manter esta estimativa]   [Recalcular]

Premissas                      Origem                   Ação
Mesmo preço e volume           Convenção da comparação  [Ver efeito]
Receita constante              Estimativa aceita        [Substituir]
CBS regular                    Pendente                 [Simular uma taxa]

Memória do tradicional
1  Histórico que entrou na faixa            fev/26 a jan/27 · R$ 1.200.000,00
2  Faixa e alíquota                         Anexo I · faixa 4 · 8,825%
3  Parcela do mês                           R$ 8.825,00 · antes da guia
▸ Ver repartição, centavos e fontes         ▸ Ver revisões e estado de validação
```

**Smartphone, mesma ordem de leitura**

```text
Simulação tributária
[Simular minhas vendas]
[Explorar o exemplo]
        ↓
Vendas do mês   R$ [      ]
Atividade          [    v]
Mês e local        [    v]
[Conferir perfil e estimar]
        ↓
Março/2027 · Exemplo
Tradicional
DAS bruto estimado   R$ 8.825,00
Alíquota efetiva     8,825%
[Ver ano e condições]
        ↓
Com IBS/CBS regulares
Total em aberto
[Falta informar créditos]
[Ver valores já calculados]
        ↓
[Comparar o mesmo componente]
▸ Premissas      ▸ Memória
[Refinar dados]  [Limpar simulação]
```

Na comparação móvel repetir o nome do regime em cada valor, agrupar pelo componente selecionado e manter visíveis base, período e unidade. O botão do próximo dado abre o campo com contexto. Exibir ajuda legal e siglas por expansão, preservando a leitura inicial.

**Erro de campo ou limite de cobertura**

```text
Não foi possível estimar esta venda
[Revisar valor das vendas]   Informe o valor em reais com até duas casas decimais.
Os demais campos continuam preenchidos.

A entrega foi em outro município.
O exemplo disponível usa loja e entrega em Florianópolis.
[Corrigir o local]   [Explorar o exemplo identificado]
```

## O que cada estado diz ao usuário

| Situação | Texto ou valor principal | Detalhe ou ação |
|---|---|---|
| Tradicional com série completa no exemplo | “DAS bruto estimado de março: R$ 8.825,00. Alíquota efetiva: 8,825%.” | Abrir série fiscal, repartição e resíduo de centavos. Distinguir obrigação bruta, extinções e guia pendente de conferência |
| Histórico estimado | “Usamos R$ 100.000 em cada mês de fev/26 a jan/27. Sua faixa pode mudar.” | “Informar os valores reais”. A cifra fica rotulada como estimativa |
| Híbrido com CBS hipotética | “Neste cenário, você escolheu CBS de 10%. Alterar a taxa muda o débito e a receita fiscal.” | Se também selecionar as exclusões e créditos intermediários **da 00B**, mostrar R$ 14.202,31 como exploração daquele conjunto de hipóteses. Exibir condições, sem pré-selecionar taxa ou crédito |
| Híbrido com créditos desconhecidos | “Os débitos da venda estão calculados. Quanto deste mês poderá ser compensado em IBS e em CBS?” | Se taxa/base conhecidas, abrir brutos e DAS remanescente. Mostrar “líquido em aberto” e “Não sei informar”. Propor extremos só quando houver base para calculá-los |
| Resultado parcial | “Subtotal de 1 dos 2 itens calculados. Falta classificar o segundo item.” | Detalhar item faltante e ação de correção. Suspender total/diferença global |
| Regime não elegível | “O pedido de opção em março não habilita a apuração regular em março.” | Identificar semestre e data de efeito, retirar a alternativa praticável desse PA |
| Elegibilidade não confirmada | “Este cenário depende de a opção estar em vigor no primeiro semestre.” | “Conferir a data e a situação da opção”. Permitir contrafactual identificado |
| Operação fora da cobertura | “Esta versão cobre a venda local descrita. Sua atividade inclui serviços.” | Explicar a cobertura e oferecer exemplo separado, sem atribuir número à empresa |
| Indisponibilidade do motor | “O cálculo deste documento está indisponível. Você pode consultar a estimativa mensal já calculada.” | Preservar dados e mostrar a última revisão. “Tentar novamente” revalida e usa a mesma edição se disponível |
| Divergência entre bases | “As versões da base deram respostas diferentes para este tipo de nota. Esta operação ficou fora da comparação.” | Detalhe profissional identifica NFS-e 820001, V0058/V0059 e pendência fiscal. Zero em campo documental não é o total da empresa |

Na expansão anual do tradicional, R$ 105.900,00 é apresentado apenas se o usuário aceitar as condições constantes do exemplo, com a legenda “projeção simplificada”. Na comparação, abrir separadamente tributos próprios, crédito potencial do comprador, margem e caixa. Quando faltarem custos/estoque ou datas, explicitar as duas últimas lacunas. Uma diferença de tributos não basta para indicar o melhor regime.

## Acessibilidade e aceite da experiência

[DECISÃO] Meta de projeto WCAG 2.2 AA. Usar rótulos associados, legendas para grupos, títulos em ordem, contraste de texto e foco visível, controles por teclado e números acompanhados de unidade. Identificar erro com texto e vínculo ao campo, levar foco ao resumo após submissão inválida e ao título do resultado após sucesso. Em melhorias dinâmicas, anunciar atualização curta ao leitor de tela. Indicar estado por texto além da cor. Testar refluxo a 320 px, zoom, teclado e leitor de tela; tabelas extensas oferecem leitura vertical por componente. [WCAG 2.2, recomendação de 12/12/2024](https://www.w3.org/TR/WCAG22/)

Na 02 testar correção de um campo e leitura do estado do item. Na 03 trocar média por série e localizar o mês mais antigo. Na 04 exigir que o usuário identifique o motivo do líquido em aberto e o titular do crédito. Na 05, observar gestor e profissional, em celular e computador, com caso sintético. Registrar tarefa, conclusão sem ajuda, confusões entre subtotal e total, tempo e observações sem valores reais. Aceite: ambos localizam a limitação e o gestor consegue refinar sem reiniciar; o profissional consegue apontar a origem de um valor e a edição usada. Aplicar correções e repetir a tarefa que falhou. A pesquisa de mercado e os wireframes são evidência documental, ainda sem entrevistas ou ensaio com usuários.
