# Dados de uma simulação e registro para reprodução

[CÓDIGO] A memória da 04 registra o preço e o volume comum, entradas normalizadas, fontes e aceites, duas séries fiscais, bases econômicas comparadas, contas separadas de IBS e CBS, cliente e opção. Campos monetários preservam decimais como texto no JSON. O valor nulo representa ausência de determinação. O comando local revalida a entrada e confronta toda a saída, exceto o instante do processamento. [Exemplo sintético](evidencias/04/middle.json) · [Comandos de reprodução](PHASE_04.md)

[CÓDIGO][EXECUTADO] O registro empresarial da 03 inclui campos normalizados, origem, meses, hipóteses aceitas, parâmetros resolvidos, rubricas analíticas e exibidas, estados, horário UTC e identificadores de software. O comando `manage.py replay_traditional` usa esse registro para recompor o formulário e comparar o conteúdo, exceto o horário da nova execução. [JSON sintético capturado no navegador](evidencias/03/c01.json) · [Procedimento](PHASE_03.md)

[CÓDIGO] O C03 guarda em memória do pedido a entrada técnica, a aceitação da hipótese, a fonte da base e das taxas, a data de processamento, os hashes, versões, resposta, memórias e arredondamento. `None` representa ausência de resultado e `Decimal('0.00')` representa zero conhecido. O detalhe expandível permite copiar o replay do cálculo bem-sucedido. As capturas de teste com dados sintéticos têm retenção separada. [Resultado real](evidencias/02/c03.json)

[DECISÃO] Contratos internos propostos em 19/11/2026. A unidade que o gestor compara é uma empresa em uma competência sob um cenário definido. O item e o documento conservam bases, estados e arredondamentos próprios. Estas estruturas orientam chamadas entre módulos e testes, sem criar uma API pública ou determinar tabelas de banco. [Matriz de responsabilidades](TAX_RESPONSIBILITIES.md)

## Convenções comuns

Identificadores e códigos são strings, inclusive quando têm zeros iniciais. Competência é `YYYY-MM`, data civil `YYYY-MM-DD` e instante ISO 8601 com deslocamento. Um valor carrega `state`, `value`, `unit`, `origin` e, quando couber, `source_ref`, `assumption_ref`, período e motivo. A origem identifica declaração do usuário, fonte oficial, retorno do motor, derivação, premissa ou informação indisponível. Manter o dado enviado, o normalizado e a ligação entre eles.

| Estado do valor | Exemplo de representação | Regra no cálculo |
|---|---|---|
| Conhecido, inclusive zero | `known / "0.00" / BRL`, com fato ou vedação demonstrada | Entra na conta em sua unidade e competência |
| Ausente | `missing / null / BRL`, falta o evento de apropriação | Solicitar o dado e suspender o líquido |
| Não aplicável | `not_applicable / null`, Fator R para esta revenda | Fundamentar a exclusão do perímetro |
| Estimado | `estimated / "100000.00" / BRL`, média aceita pelo usuário | Propagar natureza e registrar como substituir o valor |
| Não calculado | `not_calculated / null`, item fora da cobertura | Preservar código, motivo e identificação do item |
| Indisponível | `unavailable / null`, timeout do serviço necessário | Preservar os demais resultados e permitir nova tentativa |

Valores monetários em BRL e percentuais trafegam como **strings decimais** com ponto, sem agrupador ou notação exponencial. `"8.825"` em `percent` equivale a `"0.08825"` em `fraction`. Percentual incidente, parcela da repartição e variação em pontos percentuais têm tipos distintos. UI aceita convenção pt-BR explícita, valida antes de normalizar. Quantidade de itens é inteiro, quantidade comercial pode ser decimal com unidade física. Rejeitar escala incompatível, valor infinito, NaN, excesso de dígitos, sinal indevido e chave duplicada. Para o MVP, entrada monetária do formulário em centavos, até 15 dígitos inteiros como limite técnico, nunca como limite de elegibilidade.

Usar `Decimal` a partir do texto e conservar escala original e intermediários. Fixar versão da política decimal, precisão (proposta inicial de 34 dígitos significativos para divisões próprias), contexto de empate e ponto da quantização por regra. Testar fronteiras e estabilidade do centavo contra cálculo de maior precisão. Para o DF-e conservar taxa efetiva original e quatro casas quando exigido pelo leiaute. Para o DAS aplicar o estágio e o critério legal do art. 45-A, inclusive o mínimo positivo, conservar resíduo e distinguir valor analítico de guia. Guardar quantização do fornecedor na fronteira e saída original. [Arredondamento por contrato](API_INTEGRATION.md) · [Repartição e centavos](CALCULATION_REFERENCE.md)

## Campos que atravessam as fronteiras

O símbolo `?` significa opcional ou dependente de contexto. Campo desconhecido conserva o motivo. Preenchimento obrigatório depende da pergunta e do nível de resultado.

| Estrutura | Campos, tipos e unidades | Origem, validação e dependências |
|---|---|---|
| Pedido e dados econômicos | `format_version, period, activity, sales.amount, sales.unit, sales.basis, sales.frequency, requested_scenarios[]`. Opcionais `history[], purchases[], credits[], costs?, final_volume?, assumptions[]` | Usuário declara preço com tributos ou receita fiscal e se é média, mês efetivo ou total anual. Converter anual em média apenas se aceito. Não somar total anual a mês. Sem significado econômico pedir correção |
| Perfil e atividade | `opened_month?, establishments, origin_city?, destination_city?, activity_id?, description, revenue_groups[], eligibility_facts[]`. Cada fato tem estado, período de efeito e origem | Triagem por descrição, atividade, local, operação e natureza. CNPJ e identificação pessoal dispensáveis. Abertura ou opção desconhecida deixa condição visível. Elegibilidade só confirmada com referências compatíveis |
| Competência e históricas | `period, revenue_history[{month, amount, basis, origin}], payroll_history?[{month, paid_payroll, charges, origin}]` em BRL | Série da empresa e da trajetória. Exigir meses únicos, continuidade e janela legal. Estimar lacuna só por escolha registrada. Folha, pró-labore e encargos com data de pagamento entram apenas em perfil futuro que deles dependa |
| Operação e item | `operation_id, event_at, document_type, territory, regime, items[{item_id, description, activity_id?, ncm?, nbs?, cst?, class_code, quantity?, unit?, base, exclusions?, rates}]` | Gerar IDs locais estáveis, conferir unicidade, pertinência e número esperado de itens. Validar códigos por vigência, data no PA e base com origem. Item incompatível deixa falha localizada |
| Cenário | `scenario_id, regime, election_period, economic_basis, scope_id, assumption_refs[], release_id` | Serviço fixa preço/volume e distribuição, informa semestre e condições. Novo contrafactual preserva dados de partida e identifica substituições |
| Premissa | `id, revision, field, value, unit, reason, source, period, accepted, replaces?, affected_components[]` | Cenário ou usuário. Registrar seleção explícita e substituir no ramo correto. Sem aceite não preencher CBS, créditos ou série histórica por conveniência |
| Parâmetro e fonte | `id, revision, kind, value, unit, tax, regime, territory, scope, valid_from, valid_to?, conditions, source_ref, validation`. Fonte: `id, authority, title, locator, provision, published_on, retrieved_on, edition, digest?` | Catálogo a seguir. Parâmetros derivados apontam para IDs/revisões usados e método. Ausência de prova deixa grau de validação individual |
| Item e tributo | `operation_id, item_id, tax, base, gross_due, rates_used[], source_state, notices[], error_code?, result_state, trace_refs[]` | Adaptador guarda código de origem, cabeçalhos e ponteiros de erro. Serviço exige um retorno por item, trata duplicidade, ausência ou resposta incoerente como falha de contrato |
| Crédito | `event_id, owner, tax, document_ref, stage, amount, event_date, recognition_period?, extinction_ref?, rule_ref` | Dono = empresa ou adquirente. Estágios potencial/apurado/apropriado/compensado, também estorno e ajuste referenciados. Identidade impede duplicar evento no replay. Só crédito próprio apropriado entra na respectiva conta |
| Apuração mensal | `period, scenario_id, fiscal_revenue, rbt12, bracket, effective_rate, das_parts[], retained_das?, accounts[], known_subtotal, total, expected_scope, missing[], states` | Domínio reconcilia DAS e duas contas, cada uma com saldo inicial, débito, créditos, ajustes, extinções, a recolher e saldo final. Depende de cobertura, bases e eventos; nunca somar destaque documental ao DAS |
| Consolidado e comparação | `scenario_results[], basis, period_or_range, common_scope, differences[], excluded[], states, next_inputs[]` | Planejamento confronta mesma unidade, preço, volume, período e perímetro. Ausência de qualquer parcela material suspende diferença global. Benefício comercial e margem/caixa têm medidas próprias |
| Passo de memória e manifesto | `step_id, rule_ref, input_refs[], intermediate, unit, rounding, output_ref, source_refs[]`; `release_id, code_commit, catalog_rev, assumptions_rev, rules_rev, engines[], tables[], sources[], used_at` | Cada valor mostrado liga ao passo, cada passo a entradas/versões. Registrar motor dispensado, além dos efetivamente usados. Campos concretos do manifesto de motor na [integração](API_INTEGRATION.md) |

No fluxo anônimo, marcar a opção como declarada quando o usuário informar recibo, data ou situação. A declaração pode sustentar a exploração condicional. Para marcar a elegibilidade como confirmada, a origem precisa identificar uma verificação independente da empresa, do período e das condições aplicáveis. Enquanto essa verificação estiver fora do fluxo, manter “elegibilidade não confirmada”. A evidência profissional de um exemplo sintético tampouco confirma a opção de um visitante.

### Exemplo de entrada e saída no limite do serviço

[HIPÓTESE] Exemplos reduzidos em JSON. No pedido, o gestor escolhe o perfil sintético da 00B, informa o preço das vendas e aceita a mesma série fiscal estimada como ponto de partida das duas trajetórias de março. Falta informar a opção e os eventos de crédito. Os identificadores são ilustrativos.

```json
{
  "format_version": 1,
  "period": "2027-03",
  "profile_ref": "reference-00b-retail",
  "opened_month": "2023-01",
  "destination_city": "4205407",
  "sales": {"amount": "100000.00", "unit": "BRL", "basis": "final_price", "frequency": "monthly", "origin": "user"},
  "assumptions": [{"id": "flat-fiscal-history", "accepted": true, "applies_to": ["traditional", "regular_option"], "from": "2026-02", "to": "2027-01", "monthly_amount": "100000.00", "unit": "BRL"}],
  "requested_scenarios": ["traditional", "regular_option"],
  "election_proof": {"state": "missing", "value": null},
  "own_credits": {"state": "missing", "value": null, "unit": "BRL"}
}
```

```json
{
  "period": "2027-03",
  "basis": "constant_final_price_and_volume",
  "traditional": {
    "rbt12": {"value": "1200000.00", "unit": "BRL", "state": "estimated"},
    "effective_rate": {"value": "8.825", "unit": "percent"},
    "gross_das": {"value": "8825.00", "unit": "BRL", "state": "estimated"},
    "scope": "gross_das_only",
    "states": {"technical": "success", "completeness": "complete_in_scope", "nature": "estimated", "validation": "fiscal_pending", "eligibility": "unconfirmed"}
  },
  "regular_option": {
    "retained_rate": {"value": "0.07457125", "unit": "fraction"},
    "own_tax_total": {"value": null, "unit": "BRL", "state": "not_calculated"},
    "missing": ["regular_cbs_rate", "documented_exclusions", "appropriated_credits_and_balances"],
    "states": {"technical": "success", "completeness": "partial", "nature": "hypothetical", "validation": "fiscal_pending", "eligibility": "unconfirmed"}
  },
  "comparison": {
    "scope": "monthly_own_tax", "difference": null, "reason": "incomplete_scope",
    "states": {"technical": "success", "completeness": "not_calculated", "nature": "hypothetical", "validation": "fiscal_pending", "eligibility": "unconfirmed"}
  },
  "engines_used": [],
  "trace_refs": ["flat-fiscal-history", "L214", "S140"]
}
```

## Consolidação das cinco dimensões

[DECISÃO] Aplicar em cada nó o vocabulário de [RESULT_STATUS](RESULT_STATUS.md). `technical` responde se a etapa executou, `completeness` mede o perímetro, `nature` qualifica insumos, `validation` indica evidência e `eligibility` situa a empresa no regime/semestre. Quando um item não decide o direito à opção, referenciar a elegibilidade do cenário e sua origem. O contrato guarda também evidências técnicas cumulativas sob um estado fiscal pendente.

| Nível | Como propagar e apresentar |
|---|---|
| Componente tributário | Guardar dependências, estado nativo, fonte e ação. Uma taxa hipotética pode gerar um débito calculado e completo naquela hipótese. Exibir o rótulo junto ao valor |
| Item | Comparar rubricas requeridas com processadas. Divergência fiscal em componente obrigatório retira o valor da consolidação integral e preserva a memória do retorno. Inaplicabilidade fundamentada pode fechar a rubrica |
| Operação | Conferir identidade e contagem de todos os itens. Em HTTP 200 com um item bom e outro sem cálculo, exibir “1 de 2 itens” e subtotal. Falha estrutural que impeça associar os itens invalida a resposta inteira |
| Mês | Incluir ainda obrigações externas, créditos e saldos esperados. Um mês parcialmente apurado mantém débitos brutos conhecidos e líquido ausente. Uma falha do motor afeta só a rubrica dependente |
| Cenário | Somar meses apenas quando todos satisfazem o mesmo perímetro. Uma hipótese relevante permanece na natureza do total, fatos mistos mantêm identificação por parcela. Elegibilidade incerta mesmo em cenário numericamente completo. Divergência ou falta de validação em filho material impede promover o pai |
| Comparação | Interseção dos perímetros permite diferenças nomeadas por componente. Total global exige ambos completos e bases equivalentes. Classificar como exploração condicional se houver hipótese ou elegibilidade não confirmada. Alternativa inelegível não concorre. Recomendação fiscal requer evidência e revisão no próprio recorte |

## Catálogo versionado e resolução atômica

| Alternativa | Alteração e revisão | Consulta e integridade | Replay, crescimento e administração |
|---|---|---|---|
| JSON UTF-8 em Git | Pequenos diffs legíveis por tributo, fonte e edição. Revisor confere ato/dispositivo antes da promoção | Carregador valida campos, tipos, repartição, faixas e vigências. Índice em memória por chave, adequado ao recorte | Commit, arquivo e SHA-256 recuperáveis. Sem serviço nem painel. Revisar custo de carga quando crescer |
| Relacional como origem | Transações e restrições, mas exige edição controlada e histórico imutável próprio | SQL e índices atendem muitos territórios e períodos. Exige migrações e manutenção | Snapshot, backup e trilha de alteração para reconstruir a edição. Administração só se justifica com curadoria frequente multiusuário |
| Híbrido | JSON continua canônico. Build deriva índice ou banco somente leitura com hash de entrada e de saída | Bom para volume ou latência comprovados. Comparar resolução com a origem em cada build | Recuperar ambos e ferramenta geradora. Pode evoluir sem painel nem duas fontes editáveis |

[DECISÃO] Começar pelo JSON versionado. Uma edição em `reference/releases` referencia por hash os registros de `official` e, **separadamente**, os conjuntos de `assumptions`, fontes, qualificação por recorte e revisão das funções. Manter limites de faixa com inclusividade explícita, anexos e repartições agrupadas, tipo de alíquota, condições, território de origem/destino e vigência do fato. Novas correções têm nova revisão imutável e vínculo `supersedes`. Preservar também quando cada edição ficou disponível para distinguir conhecimento histórico de vigência jurídica. [Campos e exemplos reais](TAX_PARAMETERS.md)

1. Abrir um snapshot aprovado no início e verificar integridade. Fixá-lo em todos os ramos, meses e adaptadores. Um lote de referências pode conter várias vigências. A troca do manifesto ativo vale para o próximo pedido.
2. Filtrar por objeto, fato/data, regime, anexo/faixa, tributo, operação, classificação, território, unidade e condições. Validar intervalos no build e de novo ao usar. Só uma regra com precedência expressa e fundamentada pode especializar outra. Registrar as candidatas e o motivo da seleção.
3. Se local ou classificação puderem mudar a resposta, devolver `needs_territory` ou `needs_classification`. Sem candidato, `not_found`; taxa sem definição oficial, `pending_rule`. Valor publicado para outro ano e nominal da calculadora antiga não são substitutos.
4. Dois candidatos contraditórios ou vigências incompatíveis produzem `conflict`, bloqueiam promoção do recorte e impedem o total afetado. Pedir curadoria. Ordenação de arquivo ou data da última edição jamais decide a regra.
5. Uma hipótese autorizada pelo usuário gera ramo separado com unidade, condição, motivo e valor oficial de origem, se houver. Não passa pelo índice oficial. Em correção retroativa oferecer reprodução original ou novo cálculo retificado, registrando ambas as revisões. Se faltar artefato, explicitar qual reprodução ficou inviável.

## Onde fica o estado do refinamento

| Alternativa | Privacidade e acesso | Simplicidade, retenção e custo | Uso |
|---|---|---|---|
| Reenviar o formulário em POST a cada ajuste | Só a aba e a memória da requisição precisam dos números. O servidor revalida os campos e recompõe valores e estados derivados | Sem conta, ID buscável ou limpeza de registros financeiros. Fechar a aba perde a continuidade normal. Resposta privada `no-store` | Escolha do MVP. Botão “Limpar simulação” volta ao formulário vazio |
| Sessão de servidor com ID opaco aleatório em cookie | Vincular à sessão, proteger cookie, limpar ao expirar, impedir acesso cruzado | Mais armazenamento, expurgo e custo operacional. Se volume exceder o formulário, avaliar TTL proposto de 30 min de inatividade e máximo de 2 h | Adiada, sujeita a necessidade medida |
| Cookie assinado ou armazenamento persistente no navegador | Assinatura só assegura integridade. Dados financeiros permanecem no dispositivo e cookies podem viajar em toda requisição | Limite de tamanho, expiração e exposição em dispositivo compartilhado | Dispensados. Cookie técnico de CSRF só quando houver formulário |
| Identificador compartilhável, banco de histórico ou arquivo exportado | Link exige controle de acesso e retenção. Download explícito entrega o registro ao titular | Banco impõe operação permanente. Arquivo local pode ser guardado/apagado pelo usuário | Preferir download local futuro, sem URL de consulta a resultado |

Manifestos, fontes, testes sintéticos e parâmetros persistem no Git/acervo de artefatos conforme licença. A aplicação não precisa gravar movimentos do visitante nem serializar resultados em cookies ou logs. Política de tamanho, descarte, métricas e acesso em [Segurança](SECURITY.md).

## Registro exportável de reprodução

[DECISÃO] Propor arquivo JSON UTF-8 `format_version: 1`, gerado por pedido do usuário. A **memória legível** explica o caminho de cada parcela e seu fundamento. O **registro técnico** captura os dados para repeti-lo. A **evidência de homologação** é separada, sintética ou desidentificada, contém o confronto, tolerâncias, data e responsável.

| Chave obrigatória do registro | Conteúdo mínimo para reexecução |
|---|---|
| `format_version, executed_at, period, input` | Data/hora com fuso, dados declarados e normalizados, histórico por mês ou instrução exata de síntese, origem, unidades e fatos desconhecidos |
| `scenarios, assumptions, parameters, sources` | Base econômica, perímetro e opção, premissas aceitas e valores, valores de parâmetro efetivamente resolvidos com IDs/revisões, fundamento, recorte, vigência, hashes e substituições |
| `manifest` | Commit da aplicação, runtime e dependências fixados, versões de regras, premissas, catálogo, políticas decimais e cobertura. Por motor usado: commit, versão, hash JAR, base e hash, tabela, NT/leiaute, perfil de execução. Lista vazia quando dispensado |
| `operations, steps` | Entrada/saída técnica necessária por item, códigos e avisos, fórmulas/regras referenciadas, intermediários, arredondamentos, conciliação e resíduos. Excluir credenciais, URLs privadas e dados pessoais supérfluos |
| `results, states, limitations` | Mês, contas por tributo, saldos e extinções, comparação, cinco dimensões com alcance e motivos, dados ausentes e versão do formato de apresentação |

Para repetir, verificar versão do formato e integridade, recuperar as edições pelo manifesto, revalidar o pedido, executar na combinação original isolada e comparar valores, escalas, estados e faltantes. Se o JAR ou a edição se perdeu, a memória e os resultados registrados continuam consultáveis com a indicação “reprodução indisponível”, identificando a dependência. Uma execução com edição atual recebe outro manifesto. O arquivo pode conter informação empresarial e fica sob controle de quem fizer o download. [Recuperação de artefatos](INFRASTRUCTURE.md)
