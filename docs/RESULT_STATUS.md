# Estados dos resultados e qualificação

[CÓDIGO] Na 04, a base e a taxa podem permitir o débito bruto mesmo com crédito desconhecido. Uma conta com crédito ou saldo inicial ausente deixa a obrigação após créditos em aberto. O comparador expõe diferenças numéricas apenas no estágio completo para ambas as trajetórias. A elegibilidade e a validação fiscal continuam visíveis inclusive em uma sensibilidade sintética integral. [Memória e limites](PHASE_04.md)

[EXECUTADO] C03 apresenta sucesso técnico, completo no recorte, cenário hipotético, pendência de validação fiscal e elegibilidade não confirmada. No C15, três itens conhecidos compõem um subtotal e o quarto conserva o erro. No C20, o POST com a JVM desligada devolve indisponibilidade e nenhum valor de resultado. [Provas da 02](PHASE_02.md)

[DECISÃO] Atribuir **cinco dimensões independentes** a cada componente, item, documento, competência e cenário. Registrar escopo esperado e processado, itens faltantes, valor conhecido, motivo, origem e ação de recuperação. O estado do total é calculado a partir dos filhos e das obrigações externas esperadas. [Casos executados](evidencias/00a/replay.json)

| Dimensão e valor | Condição | O que apresentar / alerta | Consolidação e comparação permitidas |
|---|---|---|---|
| Técnico · sucesso | Resposta íntegra, legível e compatível com o contrato | Exibir resultado com as demais dimensões | Conferir itens, completude e elegibilidade antes de consolidar |
| Técnico · falha | Erro interno, corpo incoerente, incompatibilidade de contrato | Identificar etapa e permitir repetição com mesma combinação | Só componentes independentes. Bloquear total afetado |
| Técnico · indisponibilidade | Timeout, serviço ou tabela inacessível | Indicar dependência e retomada | Guardar entradas e resultados independentes, sem substituição por zero |
| Técnico · entrada inválida | Campo, relação ou data rejeitada | Pedir correção no campo identificável | Bloquear componente dependente |
| Completude · completo dentro da cobertura declarada | Todos os componentes previstos no perímetro descrito têm resultado, inaplicabilidade justificada ou zero demonstrado | Mostrar perímetro e totais | Consolidar e comparar somente no mesmo perímetro |
| Completude · parcial | Um ou mais itens/rubricas sem resultado | Exibir “subtotal dos itens calculados”, faltantes e alcance | Comparar apenas componentes correspondentes, bloquear ranking global |
| Completude · não calculado | Nenhum valor que responda à pergunta | Mostrar motivo e próximo dado necessário | Sem total ou comparação numérica |
| Natureza · calculado com parâmetros confirmados | Valores e regras aplicáveis identificados para o fato | Exibir fontes, data e memória | Permite comparação condicionada às demais dimensões |
| Natureza · estimado | Média, aproximação documental ou projeção substitui dado real | Evidenciar premissa e sensibilidade | Consolidar como estimativa |
| Natureza · cenário hipotético | Contrafactual, taxa ou opção simulada | Mostrar hipótese substituível | Comparar cenários condicionais na mesma base econômica |
| Natureza · combinação de dados confirmados e estimados | Ex.: IBS legal, CBS experimental, histórico declarado | Discriminar por rubrica | Total herda a incerteza, sem apresentar como fato |
| Validação · verificado tecnicamente | Ensaio ou suíte da combinação reproduz o contrato | Identificar versão, teste e período | Sustenta compatibilidade técnica do recorte |
| Validação · pendente de validação fiscal | Falta confronto independente sobre a obrigação da empresa | Tornar a pendência visível | Simulação exploratória, bloquear recomendação conclusiva |
| Validação · validado por referência independente | Fonte recuperável ou profissional confrontou **o mesmo recorte**, com entradas, tolerância e vigência | Registrar critério, resultado, data e responsável | Somente escopo efetivamente confrontado |
| Validação · divergente | Fontes ou combinações dão saídas materialmente incompatíveis | Expor divergência e excluir o caso afetado | Sem incorporação ao total integral ou recomendação |
| Validação · fora da cobertura confirmada | Tratamento/DF-e/período fora dos casos qualificados | Identificar exclusão | Subtotal independente apenas |
| Elegibilidade · elegível | Condições e opção verificadas para empresa e semestre | Exibir base da constatação | Comparar se as demais dimensões permitirem |
| Elegibilidade · não elegível | Impedimento conhecido ou escolha fora da janela para o período | Informar condição e data | Não oferecer como alternativa praticável |
| Elegibilidade · elegibilidade não confirmada | Informação societária, recibo, cancelamento etc. ausente | Mostrar condicionante e como resolver | Só contrafactual explicitamente identificado |
| Elegibilidade · fora da cobertura do sistema | Produto ainda não consegue avaliar esse enquadramento | Nomear o caso e o limite | Bloquear conclusão sobre possibilidade de opção |

[DECISÃO] Manter evidências técnicas cumulativas mesmo quando o estado fiscal atual for “divergente” ou “pendente”. Um HTTP 200 com dois itens, dos quais apenas um calculado, pode ter sucesso de transporte e completude parcial. Sucesso de transporte sozinho não promove o estado do componente. Uma venda com parâmetro hipotético pode estar completa apenas **dentro daquele cenário**. Um resultado `CALCULADO` do motor para 820001 conserva o retorno original e recebe exclusão na consolidação do MVP.

| Conteúdo numérico | Representação |
|---|---|
| Zero calculado ou vedação expressa | 0 + fundamento, escopo e período. Se a rubrica não incide, preferir “não aplicável” e motivo |
| Dado não informado ou taxa não determinada | Valor ausente + dado/regra faltante. Pode haver fórmula simbólica |
| Não implementado ou indisponível | Valor ausente + estado técnico ou motivo de cobertura |
| Valor parcial | Subtotal rotulado, denominador de cobertura quando conhecido e rubricas pendentes |
| Saldo credor | Valor e natureza do saldo. Mostrar a recolher e a recuperar em colunas distintas |

[DECISÃO] Uma afirmação de vantagem tributária pressupõe comparação de obrigações de mesmo escopo, elegibilidade e períodos, sem parcelas materiais desconhecidas e com qualidade de evidência declarada. Recomendar vantagem econômica exige também preço, volume, CMV, encargos, custos administrativos e condições comerciais/financeiras comparáveis. Qualquer divergência material ou cobertura parcial bloqueia conclusão geral.

## Manifesto e combinações

Cada execução guarda motor, commit, versão informada e SHA-256 do JAR, versão/hash da base, revisão/hash da tabela, NT e leiaute, vigências legais e fontes, versões de catálogo, premissas e regras próprias, data do fato e do processamento, entradas, cenário, arredondamento, resultados por item, exceções e decisão de consolidação. O manifesto aponta para artefatos recuperáveis. Para cenários sem chamada a motor, registrar esse fato. Preferir exportação ao usuário e referências mínimas sem persistir dados financeiros anônimos. [Inventário](evidencias/00a/inventario.json) · [Ensaio 00B](evidencias/00b/reference.json)

| Qualificação | Evidência mínima | Aplicação ao projeto |
|---|---|---|
| Tecnicamente executável | Inicialização, hashes e ensaio reproduzido | Ambas as combinações do ensaio 00B, somente nos itens observados |
| Compatível com a suíte | Relatório de testes da combinação exata, contagens e falhas | MS/V0058 passou 155 testes na 00A. MS/V0059 não atingiu esse critério |
| Com cobertura fiscal delimitada | Regime, operação, competência, lei, exclusões e resultado esperado registrados, divergências isoladas | Varejo 03/2027 tem metodologia delimitada e checagens de item. Permanecem abertas a homologação empresarial e a CBS final |
| Validada para determinado período | Referência oficial independente ou revisão profissional do mesmo caso, tolerâncias satisfeitas e artefatos preservados | Nenhuma combinação homologada para apuração empresarial de 03/2027 nesta fase |
| Não qualificada | Falta de artefato, alteração sem reensaio ou conflito no recorte | 820001 para conclusão empresarial e combinação com nova base/JAR ainda não testada |

Uma atualização abre nova qualificação. Conservar versão original, rodar compatibilidade e casos independentes antes de promover. O recorte de uso e a combinação técnica devem ser nomeados juntos. [Limitações](KNOWN_LIMITATIONS.md)
