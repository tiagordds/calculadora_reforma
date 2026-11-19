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
