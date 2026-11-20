# Premissas e calculadora rápida

[DECISÃO] Na 03, a média mensal ou o valor anual alimentam a série estimada mediante aceite. O valor anual é distribuído pelos doze meses em centavos, preservando sua soma. Usar a média como receita do próprio março exige outro aceite. O refinamento utiliza a série real completa e reaproveita os demais campos. [Implementação e limites](PHASE_03.md)

[DECISÃO] A primeira pergunta pode ser “Quanto você costuma vender por mês, já com os impostos no preço?”. Em seguida, pedir o que a empresa vende ou presta e o período. Solicitar o local de entrega/prestação quando o resultado depender de destino. A faixa estimada de comércio e a parcela do DAS podem ser apresentadas antes de perguntar sobre compras. [Memória](CALCULATION_REFERENCE.md)

| Informação | Classificação para a entrada rápida | Origem, derivação e efeito |
|---|---|---|
| Valor e significado do faturamento | Obrigatória para quantificar | Usuário em R$/mês. Distinguir média, receita fiscal e preço final |
| Atividade e mix | Obrigatória para escolher percurso, segregação indispensável em atividades mistas | Usuário descreve o que vende. Um único anexo pode ser hipótese identificada. Pedir receita por grupo em reais |
| Competência | Obrigatória, seleção inicial sugerível | Mês/ano visíveis e alteráveis. Catálogo determina automaticamente a edição aplicável quando identificada |
| Município/UF de destino | Indispensável somente quando muda regime, tributo, benefício ou item | Usuário informa local da venda ou entrega. UF/IBGE determinável a partir do município e fonte externa |
| Regime atual, abertura, sócios e opção semestral | Indispensáveis para elegibilidade e início de atividade | Perguntas simples e, para precisão, situação/recibo. Elegibilidade jurídica depende de mais que faturamento |
| Histórico mensal | Opcional na triagem, indispensável para faixa exata | Estimável por receita constante se empresa madura e hipótese explícita. Para março/27 incluir fev/26 |
| Folha, pró-labore, FGTS/CPP pagos | Indispensáveis para Fator R, Anexo IV, margem ou folha | Usuário, histórico e comprovantes. Derivar FS12 e Fator R |
| Compras, fornecedores, destinação e eventos | Opcionais para DAS, indispensáveis para tributo líquido regular comprovado | Crédito apenas estimável por cenários até reconciliar documentos e fatos |
| Perfil dos clientes | Opcional para tributo próprio, indispensável para efeito comercial | Perguntar se vende a consumidor final ou empresa e se esta recupera imposto, com opção “não sei” |
| Margem, estoque, custos, conformidade e datas de caixa | Opcionais para comparar tributos, indispensáveis para calcular lucro/caixa | Usuário. Margem projetada pode ser hipótese rotulada |
| NCM/NBS, CST, cClassTrib, benefícios e alíquotas | Dependentes de fonte externa e fatos, deriváveis em recorte unívoco | Primeiro pedir descrição, uso ou documento. Catálogo valida códigos. Nunca atribuir tratamento apenas pela atividade genérica |
| RBT12, anexo/faixa, PD, alíquotas efetivas e obrigações | Deriváveis quando as entradas bastam | Aplicação guarda fontes, hipótese e histórico. O usuário pode começar sem conhecer esses termos |

| Informação ausente | Impacto no cálculo | Tratamento permitido | Premissa aplicável | Quando solicitar ao usuário | Limitação apresentada |
|---|---|---|---|---|---|
| Histórico completo em empresa madura | Faixa e alíquota podem mudar | Estimar ou receber série real | 12 × média na janela correta, se adotada | Ao refinar ou perto de mudança de faixa | “Estimamos o mesmo valor de vendas para cada mês do histórico” |
| Data de abertura | Muda anualização e primeira faixa | Solicitar mês de início ou ramificar | Cenários de idade declarada | Após indicação de início recente | “O mês de abertura muda a faixa aplicável” |
| Mix ou descrição da atividade | Muda anexo e segregação | Cenários por grupo | Toda a receita num grupo somente se escolhida | Antes do DAS misto | “Quanto veio de vendas e quanto de serviços?” |
| Folha histórica em atividade com Fator R | Anexo III ou V | Calcular os dois ramos se os demais dados bastarem | Acima/abaixo do limiar, sem probabilidade | Para identificar o ramo | “Sua folha pode mudar o anexo usado” |
| Opção ou situação impeditiva | Alternativa pode estar indisponível | Simulação condicional | Escolha válida apenas na hipótese | Antes de atribuir resultado à empresa | “O resultado depende da sua opção em vigor” |
| Produto, tratamento ou município | Muda ICMS, benefício, classificação e base | Parcela identificada, descrição e local | Perfil sintético se selecionado | Para calcular item | “Ainda falta identificar o tratamento desta venda” |
| Composição do preço / ICMS excluível | Falta base regular inequívoca | Fórmula, documentos ou cenário | X informado separadamente do tributo apurado | Antes de total híbrido numérico | “Quais valores já estão incluídos no preço?” |
| Taxa aplicável de CBS | Impede débito definitivo | Variável ou taxa de cenário | Hipotética, substituível | Só ao explorar cenário | “A taxa usada nesta projeção pode mudar” |
| Compras, regime de fornecedor ou evento legal de crédito | Falta líquido e seu mês | Mostrar bruto, extremos calculados ou deixar aberto | Zero só se assumido num extremo ou comprovado | Ao pedir impacto líquido | “Ainda não sabemos quanto das compras gera crédito neste mês” |
| Regime do cliente | Incerteza comercial | Preservar tributo próprio | B2B e B2C como cenários | Quando comparar custo do cliente | “O crédito que seu cliente pode usar depende da situação dele” |
| Margem/custos/estoque ou datas | Impede lucro e caixa | Mostrar tributos e saldos conhecidos | Sem lucro implícito | Ao pedir resultado econômico | “Para estimar o lucro faltam custos e despesas” |
| Item não implementado, erro ou 820001 | Falta cobertura material | Parcela independente e quantidade/valor afetado, se conhecido | Sem substituição silenciosa | Pedir correção só em erro sanável | “Esta operação ficou fora do total calculado” |

[DECISÃO] Mostrar diretamente valores determinados dentro do recorte. Exibir como estimativa resultados derivados de média. Oferecer faixa apenas quando os dois extremos tiverem cálculo e premissas reproduzíveis. Um resultado parcial mostra os grupos abrangidos e o que falta. Um resultado indisponível explica a informação ou regra necessária. Preservar a entrada entre refinamentos. Cada premissa tem versão, origem, data, unidade, período, motivo e efeito no resultado. [Estados](RESULT_STATUS.md)
