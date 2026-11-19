# Especificação do produto

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
