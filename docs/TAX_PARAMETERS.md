# Catálogo versionado de parâmetros tributários

[CÓDIGO] A edição comparativa `comparison-04-01` usa a repartição de `sn-03-02` e acrescenta o IBS por ente, a situação da CBS nominal aplicável, a redução transitória em pontos percentuais e as datas excepcionais. As hipóteses do caso 00B têm arquivo e digest próprios. A memória registra os quatro hashes de catálogos e premissas e a identidade do software. [Edição](../parameters/data/comparison-04-01.json) · [Premissas](../parameters/comparison_assumptions.json) · [Replay](PHASE_04.md)

[CÓDIGO] A edição `sn-03-02` cobre a seleção das faixas vizinhas para triagem e a apuração da quarta faixa do Anexo I. A edição `sn-03-01` conserva a quarta faixa para replay. O código fixa os hashes dos arquivos e das premissas. [Dados oficiais](../parameters/data/sn-03-02.json) · [Hipóteses](../parameters/assumptions.json) · [Seleção e reprodução](PHASE_03.md)

[DECISÃO] Uma consulta recebe fato, data, território, regime, operação/atividade, classificação e versão do cenário. Só há resolução automática quando existe um valor aplicável com origem e condições compatíveis. Lacuna, sobreposição contraditória, unidade incompatível e classificação insuficiente devem produzir estados distintos.

| Campo conceitual | Conteúdo necessário para uso e replay |
|---|---|
| Identidade e objeto | ID estável, revisão imutável, tributo, regime, tipo de parâmetro (taxa, parcela em reais, repartição, limite, calendário, indicador ou fórmula), nome e descrição |
| Valor e unidade | Decimal exato, escala, moeda, percentual ou fração, ponto percentual, quantidade/unidade física. Guardar ausência com motivo. Definir sinal e estágio de arredondamento |
| Tipo de alíquota | **Nominal** da tabela/operação, **efetiva** após cálculo, **de referência** do ente, **reduzida** por dispositivo, **derivada** de outras entradas, **projetada** para uma trajetória ou **hipotética** para ensaio. Tipo e grau de certeza são eixos distintos |
| Base e chaves | Definição da base e exclusões, atividade/anexo/faixa e inclusividade dos limites, NCM/NBS, CST/cClassTrib, natureza, modelo de DF-e e condições do contribuinte/adquirente |
| Território e tempo | País, UF, município, origem/destino e critério do local. Data do ato, publicação, primeiro/último dia de efeito, competência e data de consulta. Conservar versões conhecidas à época e correções posteriores |
| Proveniência | Origem (órgão, usuário, motor, derivação, premissa), ID de fonte, dispositivo/linha, link, versão, data de extração, hash se houver arquivo e IDs dos parâmetros de que depende |
| Qualificação | Fundamentação, exceções, status jurídico, evidência técnica, escopo da validação independente, limitações e responsável pela revisão |
| Substituição | Se permitida, guardar valor oficial de origem e valor substituto separadamente, motivo, rótulo e versão da premissa. A substituição cria resultado hipotético |
| Histórico da seleção | Critério de escolha, versões das regras e premissas, chaves da consulta e valores efetivamente usados. Retificação cria nova revisão preservando o replay anterior |

### Entradas de março/2027

| Parâmetro, escopo e base | Valor/unidade ou variável | Origem e natureza no corte de 19/11/2026 | Uso e substituição |
|---|---|---|---|
| IBS estadual e municipal, venda regular integral no destino | 0,05% UF + 0,05% município, base do art. 12 | [OFICIAL] L214 art. 344, 01/01/2027 a 31/12/2028. Observar parágrafo único nos diferenciados/específicos. Nominais transitórias | Fornecer separadamente ao MR. Campo ausente na V0059 não altera a lei. Outra taxa somente como cenário |
| CBS nominal padrão regular | c, fração final incidente na base do art. 12 | [OFICIAL] L214 arts. 14 e 347, redução de 0,1 ponto percentual em 2027–28, ressalva dos combustíveis. Referência sujeita ao art. 349. Cálculo TCU 11,3%, sem resolução final identificada no corte | Distinguir referência, valor já ajustado e nominal de incidência. Registrar se a redução já está incluída. Ensaio com 10,00% é [HIPÓTESE] |
| Alíquota reduzida ou base reduzida | Fração de redução da taxa ou da base conforme dispositivo | [OFICIAL] L214 e anexos + F55, produto/serviço, finalidade e beneficiário. Taxa efetiva da operação pode ser derivada pelo MR | Validar condições e vigência. Sem comprovação produzir alternativas condicionais ou suspender item |
| IS, posição na cadeia e unidade | Parâmetro ad valorem/específico previsto por item | [OFICIAL] L214 Livro II, Anexo XVII e IS27. Ato publicado com efeitos futuros. Caneta comum da referência fora da lista | Requalificar produto, evento e MP quando aplicável |
| Faixa 4, Anexo I do comércio | Acima de R$ 720 mil até R$ 1,8 milhão inclusive, nominal 10,70%, PD R$ 22.500 | [OFICIAL] L214 Anexo XVIII, 2027–28, e S140 anexos | Registro por faixa, período e anexo. Condições de início e excesso têm regra própria |
| Repartição Anexo I, faixa 4 | IRPJ 5,50%, CSLL 3,50%, CBS 15,33%, CPP 42%, ICMS 33,50%, IBS 0,17% do valor repartido | [OFICIAL] Mesma tabela 2027–28. Soma 100% | Insumos da divisão do DAS e da dedução do art. 22-A. Não são alíquotas nominais de venda |
| Efetivas do SN e DAS remanescente | 8,825% global, IBS 0,0150025%, CBS 1,3528725%, restante 7,457125% no exemplo | [DOCUMENTADO] Derivadas de histórico sintético e repartição legal no PA. PGDAS pode fornecer percentuais da empresa | Distinguir taxa original da transmitida no DF-e. Mudam com a empresa e o mês |
| RBT12, FS12, anexo, Fator R e sublimite | Receita/folha em R$, fator em fração, corte 0,28, limites em R$ | [OFICIAL] Fórmulas S123/S140. Valores pagos/auferidos e abertura vêm da empresa | MS fornece indício de atividade. Trocar série documental por média produz estimativa |
| Opção semestral | Datas de efeito, situação no Portal | [OFICIAL] S140/O186. Recibo, cancelamento e ressarcimento são fatos da empresa | Ausência permite contrafactual condicional |
| Classificação | NCM/NBS, CST, cClassTrib, tipo de receita, DF-e, vigências | [OFICIAL] F55/F91, [CÓDIGO] recorte SQLite identificado separadamente | Catálogo fornece indicadores, sem comprovar o objeto real. Bloquear incompatibilidades |
| Base regular e créditos | R$, exclusões, débitos, créditos por tributo e eventos datados | [OFICIAL] L214 arts. 12, 27, 47–57 e RC. Fatos dependem de usuário, documento ou sistema externo | Sem dados, variável ou hipótese explícita. Preço das compras é insuficiente |
| Projeção e hipótese comercial | Crescimento, preço, mix, custos, base elegível e timing, com unidade e período | [HIPÓTESE] Usuário ou cenário substituível. Uma projeção pode incorporar parâmetros oficiais futuros | Nenhum percentual implícito de setor. Crescimento ou crédito zero exigem premissa registrada |

[DECISÃO] Para fatos dependentes de implantação, como a condição do art. 48 da LC 214, registrar ato, data e alcance da implantação. Até a confirmação, o parâmetro segue não resolvido. [Fontes](TAX_SOURCES.md) · [Exemplo](CALCULATION_REFERENCE.md) · [Manifesto de replay](RESULT_STATUS.md)
