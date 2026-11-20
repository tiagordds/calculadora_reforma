# Integração HTTP com os motores oficiais

**Rascunho técnico de 19/11/2026.** Contratos das revisões regular 1.6.1 e Simples 0.0.6. As capturas HTTP abaixo usaram V0059. Os endereços são internos. Os caminhos nas tabelas são relativos a `/api`. As portas padrão do perfil offline são 8080 e 8082. O ensaio usou 18080 e 18082 em loopback. [Captura regular](evidencias/00a/regular.json) · [Captura Simples](evidencias/00a/simples.json)

## Regime regular

| Método e caminho relativo | Entrada | Resposta e evidência |
|---|---|---|
| POST `/calculadora/regime-geral` | Operação JSON, um ou mais itens | ROC com objetos e total quando íntegro. Lote misto rejeitado por inteiro com 422, título e detalhe de NCM incompatível. [CÓDIGO][EXECUTADO] |
| POST `/calculadora/observabilidade/regime-geral` | Mesma estrutura | Itens com `nObj`, `estadoItem`, `tribCalc` ou `erros[]`. Total dos itens calculados e simulados. Ausente se nenhum entrar no total. [EXECUTADO] |
| GET `/calculadora/observabilidade/erros?codigo=REG-011` | Código de catálogo | Descrição ou 404. O erro do lote aponta para esse recurso. [CÓDIGO] |
| GET `/calculadora/dados-abertos/classificacoes-tributarias/cbs-ibs/class-trib/{cClassTrib}?data=AAAA-MM-DD` | Código de seis dígitos e data | Tratamento, nomenclatura, redução, indicadores de crédito e documentos. Código 000001 consultado. [EXECUTADO] |
| GET `/calculadora/dados-abertos/situacoes-tributarias/cbs-ibs`, `/calculadora/dados-abertos/ncm`, `/calculadora/dados-abertos/nbs`, `/calculadora/dados-abertos/fundamentacoes-legais` | Data de referência e, para NCM ou NBS específico, o parâmetro homônimo | CST e classificações associadas, detalhe de nomenclatura ou fundamentos, conforme a rota. [CÓDIGO] |
| GET `/calculadora/dados-abertos/aliquota-uniao`, `aliquota-uf`, `aliquota-municipio` sob o mesmo prefixo | `data`, mais `codigoUf` ou `codigoMunicipio` conforme ente | Referência e/ou alíquota aplicável conforme cadastro. No RS a consulta retornou `{"aliquotaReferencia":0.1}` em 2026 e 404 em 2027. [CÓDIGO][EXECUTADO para UF] |
| POST `/calculadora/base-calculo/base-calculo-unificada` e `/calculadora/base-calculo/base-calculo-unificada-nfse` | NF-e/NFC-e: ano, documento, natureza e componentes. NFS-e: ano, opção do Simples, situação, valor do serviço e componentes aplicáveis | Primeira rota fornece `baseRG`, `baseIS`, `baseSN` e avisos. A de serviços fornece `baseRG`, `baseSN`, avisos e erros. Complementares à operação. [CÓDIGO] |
| GET `/calculadora/dados-abertos/versao` e `/versao/status` | Sem corpo | Primeira lê app, banco, data e ambiente local. A segunda compara com endpoint remoto. Com remoto indisponível, primeira 200, segunda 500. [EXECUTADO] |

[Controladores](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/tree/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/java/br/gov/serpro/rtc/api/controller) · [Exemplos oficiais de base, XML e cálculo](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/docs/exemplos.md)

**Entrada do cálculo.** [CÓDIGO] Informar `id`, `versao` do payload, `dhFatoGerador` com fuso, `municipio` IBGE e `itens`. O legado `dataHoraEmissao` ainda foi aceito na fixture de 2026. A UF pode ser derivada do município. Cada item tem `numero`, `cst`, `cClassTrib`, NCM/NBS conforme nomenclatura e documento, e base ou insumos suficientes para derivá-la. Quantidade, unidade, componentes, desoneração, compra governamental e IS dependem do tratamento. O tipo de DF-e opcional muda a validação dos vínculos. Alíquotas nominais por item são exigidas a partir de 2027, com valores compatíveis com o tratamento. Preservar zeros iniciais dos códigos. [DTO da operação](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/java/br/gov/serpro/rtc/api/model/input/OperacaoInput.java) · [DTO do item](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/java/br/gov/serpro/rtc/api/model/input/ItemOperacaoInput.java)

**Exemplo executado.** Enviar o campo `input` de `cases.single_2027` ao POST de observabilidade. É o item NBS 122011200, CST 200, cClassTrib 200028 do exemplo da Receita. Data 10/03/2027, município 4314902, base 1200, alíquotas de cenário 8,8 / 0,05 / 0,05. Vieram `X-CALC-APP-VERSION: 1.6.1`, `X-CALC-DB-VERSION: V0059`, `x-warning-dados-simulados: 6`, estado simulado e valores monetários em **strings**. Com o lote completo, o quarto item recebeu `REG-011`, ponteiro `#/itens/3/ncm`. No mesmo HTTP 200 o total exibiu CBS 56,76, IBS 0,64 e IS 15,00. A falha do quarto item faz desse total um resultado parcial. [Entradas e retornos sem abreviação](evidencias/00a/regular.json)

## Simples Nacional

| Método e caminho relativo | Entrada | Resposta e evidência |
|---|---|---|
| POST `/calculadora/observabilidade/simples-nacional` | Operação e itens do Simples | `oper`, `objetos[]`, `total` quando aplicável. Cada item contém tributos/receita ou erros. [EXECUTADO] |
| GET `/calculadora/observabilidade/simples-nacional/erros?codigo=VSN-024` | Código VSN | Descrição do erro de domínio ou 404. [CÓDIGO] |
| GET `/calculadora/simples-nacional/atividades` | `data` obrigatória, `anexos`, `tpDoc` e `cClassTrib` opcionais | Lista com indicadores de disponibilidade, admissibilidade, anexos faltantes e modo do Fator R. Filtros podem sinalizar incompatibilidade sem retirar a linha. [CÓDIGO] |
| GET `/calculadora/simples-nacional/atividades/{codigo}` | Código de dois caracteres, data, filtros opcionais `tpDoc` e `cClassTrib` | Detalhe do catálogo. A atividade 01 retornou 404 em 2026. Em 2027 indicou anexo I e documentos 55/65. [EXECUTADO] |
| GET `/versao` e `/versao/status` | Sem corpo | Versão local e comparação com instalação online. Sem resposta remota o status devolveu 200 e indicadores falsos, sem versão remota. Isso deixa a atualização desconhecida. [EXECUTADO] |

[Controlador de cálculo](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/api/simplesnacional/controller/SimplesNacionalController.java) · [Controlador de atividades](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/api/atividadesimples/controller/AtividadeSimplesController.java)

**Entrada do cálculo.** [CÓDIGO][EXECUTADO] Exige `id`, `versao`, `data` ISO, `tpDoc`, `CRT` em maiúsculas e lista não vazia. `tpRegimeIBSCBS` e `tpEnteGov` são condicionais e globais. O caso de revenda usa número do item, `cAtivSN` compatível, `cClassTrib`, `baseCalculo`, `valorImpostoSeletivo` (inclusive zero conhecido), alíquotas efetivas em **pontos percentuais**. O contrato usa texto para valores e alíquotas. Sem atividade admissível pode haver receita e estado `NAO_CALCULADO`. Sem alíquotas exigidas há erro de item. A alíquota nominal do regular e a alíquota efetiva do Simples têm significados diferentes. [DTO](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/api/simplesnacional/model/input/ItemSimplesInput.java) · [Validações](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/api/simplesnacional/service/SimplesNacionalObservabilidadeService.java)

**Exemplo executado.** A entrada abaixo corresponde ao teste oficial de CRT 1. O valor `versao` pertence ao payload. A versão do JAR vem no cabeçalho.

```json
{
  "id": "507f1f77bcf86cd799439011",
  "versao": "2.0.0",
  "data": "2027-03-15",
  "tpDoc": "55",
  "CRT": "1",
  "itens": [{
    "numero": 1, "cAtivSN": "01", "cClassTrib": "000001",
    "baseCalculo": "950.00", "valorImpostoSeletivo": "50.00",
    "pIBSSN": "1.25", "pCBSSN": "2.75"
  }]
}
```

[EXECUTADO] HTTP 200, app 0.0.6, base V0059. O retorno registrou receita e base de 950,00, `vIBSSNtot=11.88`, `vCBSSNtot=26.12`, `totalIs=50.00`, `totalTributos=88.00`. Os valores de IS e alíquotas já vieram na entrada. Remover as duas alíquotas gera `VSN-004` e `VSN-006`. Trocar a atividade por 99 preserva apenas receita no total. Enviar `tpEnteGov=7` retorna 422/`VSN-024`. Um segundo item com cClassTrib 999999 gera `VSN-021` sem invalidar o primeiro. [Capturas completas](evidencias/00a/simples.json)

## Contrato proposto com o futuro backend

[CÓDIGO][EXECUTADO] Ambos usam `BigDecimal`, precisão intermediária de oito casas e `HALF_EVEN`. Os serializadores monetários retornam duas casas. No Simples, os valores 11,875 e 26,125 do caso dourado aparecem como 11,88 e 26,12. Consumir a memória e os totais enviados pelo motor evita reaplicar arredondamentos a intermediários já formatados. [Precisão no regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/docs/adr/ADR003-estrategia-de-precisao-numerica.md) · [Precisão no Simples](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/docs/adr/ADR003-estrategia-de-precisao-numerica.md)

[DECISÃO] O navegador enviará dados ao Django. Um adaptador por motor traduzirá entradas para a API interna, tipará valores monetários como decimais e preservará o corpo e os avisos necessários para a memória de cálculo. Endpoints de referência e esquema OpenAPI configurado em `/api/api-docs` permitem testar o contrato por versão. A aplicação não deve depender das tabelas SQLite internas para calcular.

1. Validar a cobertura do cenário, origem dos parâmetros e versão esperada antes do envio. Usar destinos internos configurados. Limitar tamanho do lote, tempo de conexão/leitura e concorrência. Orçamentos numéricos dependerão dos testes da fatia vertical.
2. Conferir HTTP, cabeçalhos de versão e aviso, conjunto de itens, `estadoItem`, erros com código/ponteiro, existência de total e campos ausentes. Preservar distinção entre calculado, simulado, sem cálculo, sem implementação, entrada inconsistente e falha técnica. Manter resultados parciais identificados. Não traduzir ausência em zero.
3. Classificar 400/422 como erro de dados/escopo de acordo com o corpo. Diferenciar 404 de referência ausente, resposta incompleta, indisponibilidade, timeout e erro técnico. Mensagens ao usuário devem indicar o dado que pode corrigir ou informar qual cálculo ficou indisponível. Detalhes internos e URLs de falha ficam fora da apresentação. Nunca recorrer silenciosamente a uma fórmula substituta.
4. Associar o resultado a commit, hashes de JAR/base, período, payload, parâmetros, método de arredondamento e intermediários. Invalidar caches por versão e vigência. Gerar uma nova base offline e exercitar a suíte e as fixtures do par candidato antes de trocar instâncias. Para reverter, selecionar o conjunto anterior preservado e restaurar seu ambiente.
5. Guardar o registro de simulação anônima com o usuário quando possível. Limitar os logs operacionais a informações técnicas necessárias. O histórico profissional, a API externa e a exposição dos serviços oficiais não fazem parte da integração experimental.

Os resultados acima testam compatibilidade de software. O contrato para apuração mensal da empresa, a política de alíquotas para 2027 e a decisão fiscal sobre a NFS-e 820001 permanecem pendentes. [Riscos e pendências](RISKS_AND_OPEN_QUESTIONS.md)

## Política da 00C para os adaptadores internos

[DECISÃO] O parágrafo de encerramento da 00A acima descreve o estado de `99fc807`. Em `bb39b72`, a 00B delimitou a apuração e as origens de taxa, manteve a CBS regular condicional e excluiu NFS-e 820001 da comparação empresarial. A 00C traduz essas decisões em critérios de habilitação do adaptador. [Regras empresariais](TAX_RULES.md) · [Exclusões](KNOWN_LIMITATIONS.md)

**Primeiro cálculo web (02).** Escolha do regular 1.6.1/V0059, caso **C03**, operação de 15/03/2027 em Florianópolis. Uma caneta, NCM 96081000, 000/000001, base documental de R$ 100,00, IBS de 0,05% por ente e CBS hipotética de 10% aceita no modo de exemplo. Reusar o payload exato de `cases[0].input` e registrar os campos efetivamente enviados (inclusive o modelo de DF-e quando presente). O caso tem resposta observável, taxas decimais e cobertura técnica localizada, e dispensa RBT12 e DAS. Exigir o retorno por item `CALCULO_SIMULADO`, CBS R$ 10,00 e IBS R$ 0,05 por ente. Mostrar “base da operação”, distinguindo-a do montante pago pelo cliente. O caso C02 do Simples exige percentuais efetivos empresariais, o que adicionaria uma entrada à primeira integração. Nenhum dos dois testes homologa o regime empresarial. [Captura exata](evidencias/00b/reference.json) · [Qualificação do regular](INFRASTRUCTURE.md)

[EXECUTADO][CÓDIGO] Na captura da 00B para C03, `tpDoc` foi omitido no payload regular. A NF-e 55 pertence ao perfil da 00B. Para oferecer validação do vínculo documental no motor, executar uma variação identificada com `"tpDoc": 55` e conferir o resultado separadamente do replay original. [Campo opcional no contrato 1.6.1](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/java/br/gov/serpro/rtc/api/model/input/OperacaoInput.java#L64)

| Momento | Verificação e resposta do backend |
|---|---|
| Inicialização | Um processo de longa duração por motor necessário. Endereços `REGULAR_ENGINE_URL` e `SIMPLE_ENGINE_URL` de configuração interna, nunca de campos do usuário. Em nativo, http em loopback nas portas de ensaio 18080/18082; em Compose, serviços `regular:8080` e `simples:8082` na rede privada. Os ajustes de gestão não são portas públicas |
| Integridade | Antes de admitir cálculo, conferir SHA-256 do JAR e da cópia somente leitura do SQLite contra manifesto permitido, ambiente e versão local. Confirmar diretório de trabalho, base presente e temporário gravável. Base ausente/desconhecida deixa motor indisponível. Impedir download/updater e egress desnecessário |
| Vida e prontidão | Processo vivo indica apenas inicialização. Ler versão local e base pelos GETs descritos acima e executar canário sintético da combinação. Só então habilitar o recorte. Monitorar prontidão fora da requisição financeira e após reinício ou troca. Comparador remoto `/versao/status` é informativo; sua falha isolada não reprova o cálculo local qualificado |
| Montagem | Selecionar simulação agregada (0 POST), representativa (estimativa ponderada com equivalência demonstrada) ou documental. No Simples mapear atividade/CRT e taxas efetivas do PA; no regular, nominais conforme tratamento, fato e destino. Preservar códigos, unidade e escala do leiaute |
| Prazo e repetição | Valores propostos para ensaio: conexão até 0,5 s, leitura inativa até 2 s, orçamento de parede de 5 s para toda a requisição web. Consumir a resposta com limite de bytes e tempo restante, e impor teto de execução no servidor/borda. Zero retentativa automática de POST. Botão de repetição inicia outro pedido validado com a mesma versão se recuperável. Erro de dados exige correção |
| Resposta | Validar status HTTP, schema, cabeçalhos de versão/aviso quando previstos e consistência com o manifesto. Associar cada número de item exatamente uma vez, detectar extras, faltantes e duplicados. Preservar `estadoItem`, código/ponteiro e totais de origem. Computar cobertura em separado; um 200 com item rejeitado preserva o subtotal identificado |
| Falhas | 400/422 com campo reconhecido → correção. 404 de referência → lacuna. Conexão/timeout → indisponibilidade. JSON inválido, contrato desconhecido, IDs ambíguos ou edição inesperada → falha técnica, suspender o componente afetado. Sem cálculo substituto. Valores independentes permanecem disponíveis |
| Testes | Offline: replay de corpos preservados, cabeçalhos, falha e lote misto com transporte substituído. Integração explícita: iniciar par permitido, canário e POST real; comparar itens, versões, avisos e campos decimais. Uma suíte marcada como integração real deve falhar se invocada com dependência ausente. [Matriz por fase](TEST_SCENARIOS.md) |

### Seleção, atualização e retirada por recorte

[DECISÃO] A lista de combinações autorizadas usa a chave (motor, commit, versão informada, SHA-256 JAR, versão e SHA-256 SQLite, revisão/hash das tabelas, NT/leiaute, vigência, recorte e finalidade). Fixar ainda versão do catálogo, regras próprias e premissas. A finalidade diferencia teste técnico, ensaio interno, homologação e exposição aprovada. Uma combinação desconhecida não entra por proximidade de versão. Uma execução em andamento permanece presa à versão admitida; se a instância passar a servir outra, invalidar só os resultados que dela dependiam.

| Combinação preservada | Uso proposto e limite |
|---|---|
| Regular 1.6.1, commit `150cccbe`, V0059 | Executável, com suíte e C03 reproduzidos anteriormente. Selecionar para a prova web específica, com rechecagem de hashes e canário no ambiente-alvo |
| Simples 0.0.6, commit `c5b0f01c`, V0059 | Executável no C02 da 00B. Duas falhas conhecidas em 820001. Qualificar por caso. Excluir 820001 e IS controverso da comparação empresarial |
| Mesmo Simples e V0058 | Compatível com 155 testes originais. Usar como controle de regressão. A suíte não define vigência nem autoriza trocar a V0059 |
| Regular 1.7.2 e migrações posteriores inspecionadas na 00B | Evidência de leitura de código, fora da lista de execução habilitada. Nenhuma promoção por existir release novo |

IDs completos e hashes exatos devem vir do [inventário da 00A](evidencias/00a/inventario.json) e das [combinações do ensaio da 00B](evidencias/00b/reference.json). Os cinco estágios de qualificação (executável, compatível com suíte, cobertura fiscal delimitada, validada para o período e não qualificada) têm critérios independentes. [Estados](RESULT_STATUS.md)

Para mudar uma combinação, preparar candidato em instalação separada, verificar licença e origem, produzir manifesto, reexecutar suíte do fornecedor e corpus de casos e comparar diffs por rubrica/estado. Para novo recorte acrescentar referência independente, vigência e exclusões; para habilitação pública obter revisão fiscal e aceite. Se houver divergência, manter a captura, retirar a tupla afetada da cobertura e identificar replays que a invocam. Para reverter, selecionar a edição anterior aprovada, restaurar bytes pelos hashes, executar canário e reabrir o tráfego apenas para competências em que essa edição continue aplicável. Replay histórico isolado pode usar recorte já retirado, com seu status atual explícito. [Preservação e restauração](INFRASTRUCTURE.md)
