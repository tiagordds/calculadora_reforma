# Memória de referência · Florianópolis, março de 2027

[EXECUTADO] Em 24/11/2026, o segundo perfil investigado na 00B ganhou apuração empresarial própria. Com R$ 100.000 de receita no PA e RBT12r de R$ 1,2 milhão, a passagem de FS12 de R$ 335.999,99 para R$ 336.000,00 muda o DAS bruto de R$ 19.075,00 para R$ 13.030,00. [Contas e memórias dos dois lados do C08](SIMPLES_SERVICES_01.md)

**Resultado do caso sintético.** A revenda comum do Anexo I gera obrigação mensal estimada de **R$ 8.825,00** no regime único, antes da conciliação da guia. No híbrido, **7,457125%** incide sobre a receita do Simples daquele cenário. Ainda faltam a taxa aplicável definitiva da CBS regular e os documentos que fecham bases e créditos. A comparação principal conserva o preço pago pelo cliente. [Fontes S140, L214 e C27](TAX_SOURCES.md)

## Entradas e elegibilidade

| Dado | Valor e origem |
|---|---|
| Empresa e mercado | [HIPÓTESE] EPP aberta em 2023, uma loja em Florianópolis/SC (IBGE 4205407), sem filiais. Revenda interna, estoque nacional, entrega local, sem importação, industrialização, transferência ou retenção. |
| Mercadoria e operação | [HIPÓTESE] Caneta esferográfica comum para escritório, comprada para revenda. NCM 9608.10.00 conforme descrição do MDIC. Venda onerosa de mercadoria adquirida de terceiros no Estado, hipótese de CFOP 5.102, NF-e modelo 55, cAtivSN 01. Na ausência de regime especial aplicável, CST IBS/CBS 000 e cClassTrib 000001, tpRBSN 1. A tabela permite NF-e. Não se escolheu o produto por retornar sucesso. Revisar descrição, embalagem, benefício e RICMS/SC na vigência. [MER e F55](TAX_SOURCES.md) |
| Receita | [HIPÓTESE] Preço final de março R$ 100.000,00, sem frete adicional, devoluções, descontos ou receita diversa. Receita **fiscal** informada de R$ 100.000 por mês de mar/2026 a fev/2027 para ambos os históricos de partida. Acrescentou-se fev/2026 nos mesmos R$ 100.000, necessário para a janela de 2027. Não se fixa retroativamente o preço final desses meses em ambos os regimes. |
| Compras e folha | [HIPÓTESE] R$ 40.000 em compras pelo preço final do fornecedor regular local e R$ 10.000 de folha no mês. A compra tem destinação para revenda. Não há eventos de crédito reais. No caso-base, clientes consumidores finais, fornecedor e adquirente domésticos. |
| Condições legais | [HIPÓTESE] Empresa regularmente optante pelo Simples, sócios e participações permitidos, receitas globais dentro do limite, atividade admitida, sem débito impeditivo, exclusão, transposição de sublimite ou ressarcimento impeditivo. Na trajetória híbrida, escolha regular conjunta no Portal em 15/10/2026, válida para jan–jun/2027 e não cancelada. Na tradicional, continuidade no regime único. São contrafactuais na data de decisão, sem comprovação de uma empresa real. |
| Perímetro | [HIPÓTESE] Sem benefício, ST, antecipação, monofasia, importação, diferencial, venda com IS ou outro fato que gere tributo próprio externo no comércio descrito. Sem saldos anteriores, ajustes, split/recolhimento pelo comprador no exemplo aritmético. Retenções de terceiros, FGTS, salários e custo de conformidade são rubricas distintas. Sem estoque inicial/final, CMV e despesas completos, margem e caixa permanecem abertos. |

## Tradicional

[OFICIAL][EXECUTADO] RBT12 de março = 12 × R$ 100.000 = R$ 1.200.000 (fev/26–jan/27). Revenda no Anexo I, quarta faixa, de R$ 720.000,01 a R$ 1.800.000,00, nominal 10,70%, parcela a deduzir R$ 22.500. Alíquota efetiva = (1.200.000 × 0,107 − 22.500) / 1.200.000 = 0,08825. DAS bruto projetado = 100.000 × 0,08825 = **8.825,00**. Folha não altera o anexo. Repartição do Anexo XVIII da LC 214 na redação de 2027–2028. [L214 e S140](TAX_SOURCES.md) · [Verificação decimal](evidencias/00b/reference.json)

## Híbrido ao mesmo preço final

[DOCUMENTADO] Para evitar confusão entre valor da venda e valor após compensação, sejam `P=100.000`, `c` a alíquota final aplicável da CBS em **fração**, `r=c+0,0005+0,0005`, `X` as demais exclusões legais do valor da operação (neste perfil, particularmente o ICMS incidente, a conciliar por documento). No cenário homogêneo, antes do arredondamento por item: `B=(P−X)/(1+r)`, pois `P=B+X+rB`. Débito bruto regular `D=rB`. Para o caso simples em que as únicas exclusões da receita do SN são os tributos regulares incidentes na venda, `H=P−D`. A base regular `B`, a receita fiscal do Simples `H` e o preço `P` são três grandezas diferentes. Validar a composição de cada documento antes do uso fiscal. [L214 art. 12, S140 arts. 2º e 22-A](TAX_SOURCES.md)

Para março os históricos de entrada coincidem. DAS remanescente = `H × 0,08825 × (1−0,1533−0,0017) = H × 0,07457125`. A multiplicação de **R$ 100.000 de receita fiscal** por essa taxa resultaria em R$ 7.457,125 antes de arredondar. Usá-la diretamente para **R$ 100.000 de preço final** no híbrido superestimaria a receita. Para compras de R$ 40.000 são necessárias a base própria do fornecedor, tributação de cada item e extinções/condições de apropriação. Definir `C_c` e `C_i` como créditos de CBS e IBS já apropriados e disponíveis neste PA. Para ausência expressa de outros saldos, definir `L_c=max(0,cB−C_c)`, `L_i=max(0,0,001B−C_i)`. O excedente positivo de cada crédito fica em saldo próprio.

### Reconciliação do mês

Valores em reais. Casas além do centavo são memória analítica exata antes do fechamento. Os pesos da segunda coluna são frações percentuais **da repartição do DAS**. O IBS do Simples tem uma parcela única nessa tabela.

| Componente | Simples tradicional | Simples híbrido | Fonte | Método | Componente responsável |
|---|---:|---:|---|---|---|
| Venda a preço final | 100.000 | 100.000 | Perfil | Hipótese fixa | Usuário/premissa |
| Receita mensal no SN | 100.000 | H | S140 | Deduzir IBS/CBS regular da venda no híbrido | Aplicação |
| RBT12 / alíquota global | 1.200.000 / 8,825% | 1.200.000 / 8,825% antes da dedução | S140, Anexo I | História e fórmula da faixa | Aplicação |
| IRPJ | 5,50% → 485,375 | H × 0,00485375 | L214 Anexo XVIII | Dentro do DAS | Aplicação |
| CSLL | 3,50% → 308,875 | H × 0,00308875 | Idem | Dentro do DAS | Aplicação |
| CPP | 42,00% → 3.706,50 | H × 0,037065 | Idem | Dentro do DAS | Aplicação |
| ICMS | 33,50% → 2.956,375 | H × 0,02956375 | Idem | Dentro do DAS, conferir X independentemente | Aplicação |
| CBS dentro do DAS | 15,33% → 1.352,8725 | 0, opção válida | S140 art. 22-A | Alíquota efetiva 1,3528725% | Aplicação |
| IBS dentro do DAS | 0,17% → 15,0025 | 0, opção válida | Idem | Alíquota efetiva 0,0150025% | Aplicação |
| DAS bruto | **8.825,00** | **0,07457125 × H** | S140 arts. 22, 22-A | Subtotal das linhas anteriores | Aplicação |
| IBS regular UF e município | Não aplicável | 0,0005 B em cada ente | L214 art. 344 | Destino SC/Florianópolis, tributação integral | Motor regular por item, aplicação no PA |
| CBS regular bruta | Não aplicável | cB | L214 arts. 14, 347, 349 | c ainda condicional | Motor regular por item |
| Compras / créditos próprios | 40.000 / vedados para IBS/CBS do regime único | 40.000 / potenciais desconhecidos, apropriados C_c e C_i | L214 arts. 47–48 | Vínculo ao DF-e e à competência | Fornecedor/empresa/aplicação |
| Tributos regulares líquidos a recolher | Não aplicável | L_c + L_i | L214 arts. 27, 42–48 | Duas contas, após apropriação, antes de outras extinções | Aplicação |
| PIS e Cofins ordinários | Sem parcela na tabela de 2027 | Idem | E132, L214 | Sem resíduos de períodos anteriores por hipótese | Aplicação |
| ISS, IPI, IS e outros externos | Sem fato gerador no perfil | Idem | S123, L214, IS27, MER | Revenda interna comum, sem serviços/industrialização | Enquadramento/revisão |
| **Tributos próprios do mês no perímetro** | **8.825,00** | **0,07457125 H + L_c + L_i** | Acima | Somar subtotais uma vez. Resultado híbrido condicional | Aplicação |
| Valor ao cliente / demais encargos | B2C sem crédito / folha informada, encargos externos não medidos | Idem | Perfil e S123 | Fora da carga própria apurada acima | Cliente/empresa |
| Projeção anual | **105.900,00** na hipótese constante | Soma dos 12 DAS remanescentes e 24 contas mensais de IBS e CBS, com transporte de saldos | Regras e histórico | Ver condições abaixo | Planejamento |

Para emitir o DAS aplicam-se os centavos do art. 45-A. Se cada quota analítica tradicional for exibida com duas casas, os arredondamentos somam R$ 8.825,01. Conservar o resíduo de R$ 0,01 na memória. A distribuição operacional dos centavos e o total efetivamente consignado na guia exigem confronto com o PGDAS. O número de R$ 8.825,00 corresponde à aplicação da alíquota global à receita.

### Confronto dos motores por item

[EXECUTADO] Em 19/11/2026 usamos a mesma mercadoria e **R$ 100 de base de entrada em cada contrato** para isolar o cálculo documental. Essa escolha de laboratório não implica o mesmo preço final na comparação econômica. No regular 1.6.1/V0059 usamos CBS **10,00% hipotética** ajustável e IBS 0,05%/0,05% legal. Retorno HTTP 200, `CALCULO_SIMULADO`, CBS R$ 10,00 e IBS R$ 0,05 + R$ 0,05. No Simples 0.0.6/V0059, usamos os percentuais derivados da faixa ao nível de quatro casas do leiaute (0,0150% e 1,3529%). Retorno HTTP 200, `CALCULADO`, RBSN R$ 100,00, IBS R$ 0,02 e CBS R$ 1,35. Nenhum resultado inclui IRPJ, CSLL, ICMS e CPP mensais. Mil reproduções desse item SN dariam R$ 1.370 nos dois campos, enquanto a memória mensal exata soma R$ 1.367,875. Registrar a diferença entre granularidades, sem substituir o DAS pela soma documental. [Entradas, retornos e hashes](evidencias/00b/reference.json) · [Reprodução](evidencias/00b/FONTES_TECNICAS.md)

### Sensibilidade ao mesmo preço

[HIPÓTESE] Para tornar a escala das diferenças visível, **apenas no ensaio** tomar `c=0,10`, `X=2.700` como montante de exclusões informado para testar a fórmula e R$ 30.000 de base tributável identificada dentro das compras de R$ 40.000. Esses valores sintéticos precisam ser substituídos pelos dos documentos. A faixa representa escolhas explícitas do experimento, sem pretensão de média setorial ou previsão oficial. Resultam B ≈ R$ 88.374,21, H ≈ R$ 91.074,21, DAS remanescente ≈ R$ 6.791,52, CBS bruta ≈ R$ 8.837,42 e IBS bruto ≈ R$ 88,37. As contas usam precisão completa até a exibição. As duas parcelas de IBS a R$ 44,1871… cada podem apresentar diferença de um centavo ao serem arredondadas por item.

| Situação das compras do mesmo fornecedor regular | CBS / IBS apropriados no PA | Híbrido no perímetro, antes da conciliação documental |
|---|---:|---:|
| Pouco crédito: nenhuma das aquisições reúne as condições até março, hipótese expressa | 0 / 0 | R$ 15.717,31 |
| Intermediário: documentos correspondentes a R$ 15.000 de base cumprem as condições em março | 1.500 / 15 | R$ 14.202,31 |
| Alto: todos os documentos dos R$ 30.000 de base cumprem as condições | 3.000 / 30 | R$ 12.687,31 |

[DOCUMENTADO] Se o fornecedor recolher IBS/CBS no Simples, substituir a taxa regular pelos valores transferíveis do seu regime e seus documentos. Se estiver desonerado ou vender sem direito a crédito, verificar a hipótese específica. Sem informar seu regime, o valor utilizável fica desconhecido. Com predominância B2C, o preço final determina o gasto do consumidor. Em B2B regular, o mesmo preço pode deixar custos de aquisição distintos após o crédito utilizável. Com predominância de clientes do Simples tradicional, não há crédito próprio ordinário de IBS/CBS desses compradores. Os três montantes acima medem tributo próprio, não medem atratividade comercial nem autorizam recomendar regime.

[HIPÓTESE] No exercício alternativo de receita pré-tributos fixa, o alvo tradicional desta operação é R$ 100.000 − 2.956,375 − 1.352,8725 − 15,0025 = **R$ 95.675,75**. No híbrido resolver preço que deixe esse alvo após os débitos brutos da venda e o ICMS embutido. Usar o preço encontrado para calcular H, B e créditos do cliente. Mantendo apenas para esse ensaio a CBS de 10%, X de R$ 2.700 e a mesma alíquota efetiva de ICMS, H = 95.675,75 / (1 − 0,02956375) e P = H + 0,101 × (H − 2.700) ≈ **R$ 108.275,39**. O mesmo alvo de receita leva a outro preço para o comprador. [Método econômico](TAX_RULES.md)

### Ano e segundo perfil

[HIPÓTESE] Os R$ 105.900 são projeção de 12 competências do tradicional com R$ 100 mil/mês e histórico fiscal constante inclusive nos meses adicionais anteriores necessários para janeiro/fevereiro, mesmo mix, anexo e partilha de 2027, sem eventos externos. No híbrido, projetar janeiro a dezembro com receita fiscal própria em cada mês, opção válida para cada semestre, histórico móvel, preço, composição e eventos de crédito de cada mês. Conservar as entradas históricas de março ao montar o calendário. Alterar o preço de março altera sua receita fiscal e pode alterar a faixa/alíquota de **maio em diante** pela janela defasada. Multiplicar a estimativa híbrida de março por doze não reproduz essa trajetória.

[HIPÓTESE] Segundo perfil proposto: desenvolvedora de programas sob encomenda, serviços no estabelecimento do optante, mercado interno em Florianópolis, sem licenciamento, exportação ou benefício. LC 116 item 1.04, NBS candidata **1.1502.20.00**, cAtivSN 09, operação integral candidata 000/000001. F91 Anexo VIII v1.02.00 traz correlações múltiplas, conferir contrato, local do fornecimento, retenção de ISS e destino. Atividade sujeita ao Fator R (LC 123 art. 18 §§ 5º-D e 5º-M). Com RBT12r de R$ 1.200.000, FS12 de R$ 336.000 produz exatamente 28% e Anexo III. R$ 335.999,99 fica abaixo e conduz ao V. Pedir folha **paga com encargos definidos**, pró-labore, histórico e receita segregada. Pessoal assalariado não gera destaque de IBS/CBS. Softwares, equipamentos e serviços adquiridos exigem documentos e destino empresarial. Na opção regular, IBS/CBS saem da partilha correspondente ao anexo determinado e ISS continua sujeito ao seu limite/redistribuição e às exceções. A migração posterior V0068 corrigiu as colunas de anexos da atividade 09. A confirmação pelo catálogo V0059 isolado é insuficiente. Validação documental e profissional deste segundo perfil pendente. [SRV, F91, S140](TAX_SOURCES.md) · [Cenários](TEST_SCENARIOS.md)
