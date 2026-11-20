# Roadmap

**Posição em 19/11/2026.** A investigação técnica 00A e a metodologia tributária 00B estão concluídas nos respectivos escopos. Há informação suficiente para planejar a arquitetura de um MVP de revenda interna, com cenários condicionais para o híbrido. A 00C aguarda autorização do titular.

| Fase | Entrega e critério de conclusão | Estado |
|---|---|---|
| 00A · Motores oficiais | Identificar revisões e contratos, executar operações e erros por motor, registrar cobertura, serviço interno, testes, limitações e questões para a matriz. | Concluída no escopo investigativo |
| 00B · Matriz, metodologia e riscos | Atribuir responsabilidades, reconciliar operação e empresa, delimitar créditos, fontes, comparação e riscos. | Concluída no escopo metodológico |
| 00C · Arquitetura, produto e planejamento | Escolher recorte verificável do MVP, jornada, arquitetura mínima e casos de referência. Validar hipóteses de produto e mercado. | Aguarda autorização |
| 01 · Fundação web | Django mínimo, página inicial funcional no navegador, ambiente reproduzível, testes e documentação. | Planejada |
| 02 · Primeira operação | Formulário, validação, adaptador interno, cálculo oficial, erros e resultado rastreável de um caso suportado. | Planejada |
| 03 · Simples rápido | Estimativa mensal e anual para perfis definidos, sem cadastro, com premissas, RBT12, anexos e memória. | Planejada |
| 04 · Tradicional e híbrido | Comparar opção de IBS/CBS regular com recolhimento tradicional em bases consistentes, incluindo demais parcelas, créditos e elegibilidade. | Planejada |
| 05 · Consolidação do MVP | Refinar cenário sem recadastro, demonstrar sensibilidade, validar cálculos e avaliar interface, segurança e desempenho. | Planejada |
| 06 · Primeira publicação | Escolher hospedagem, configurar domínio/HTTPS, rede privada, limites, monitoramento, atualização, privacidade e recuperação. Depende de validação profissional e autorização de publicação. | Planejada |
| 07 · Lucro Presumido | Acrescentar apuração e comparação verificadas para os perfis cobertos. | Planejada |
| 08 · Lucro Real | Acrescentar apuração e comparação verificadas com os insumos contábeis necessários. | Planejada |
| 09 · Planejamento avançado | Projetar até 2033 conforme vigências, simular sensibilidade, pontos de mudança, preços e impactos financeiros. | Planejada |
| 10 · Plataforma profissional | Autenticação, isolamento entre empresas, permissões, histórico, importação, relatórios e cenários avançados. | Planejada |
| 11 · Integrações e expansão | APIs externas e ERPs. Avaliar monetização, assinaturas, novos canais e PWA conforme necessidade. | Planejada |

## Aceite da 00A

| Critério da investigação | Evidência |
|---|---|
| Versões, objetivos, licenças, granularidade, cobertura e limites dos dois motores e triagem de DANFSe | [Relatório técnico](OFFICIAL_ENGINES.md) |
| Contratos, entradas indispensáveis, dados derivados, estados, alíquotas e créditos | [Integração](API_INTEGRATION.md) |
| Execução local e sem dependência remota de cálculo, classificações, operação válida e inválida, períodos e concorrência | [Regular](evidencias/00a/regular.json) · [Simples](evidencias/00a/simples.json) |
| Recursos, instalação, dependências, testes oficiais e recuperação de versões | [Infraestrutura](INFRASTRUCTURE.md) · [Inventário](evidencias/00a/inventario.json) · [Restauração de duas bases](evidencias/00a/replay.json) |
| Divergências, limitações de 2027, validação profissional e trabalhos para a matriz | [Pendências](RISKS_AND_OPEN_QUESTIONS.md) · [Decisões](DECISIONS.md) |

## Aceite da 00B

| Critério | Entrega e condição |
|---|---|
| Objetivo, plano, dependências e riscos da abertura | [Registro de abertura](evidencias/00b/PLANO.md) |
| Responsáveis, legislação, parâmetros de 2027 e apuração | [Matriz](TAX_RESPONSIBILITIES.md) · [Fontes](TAX_SOURCES.md) · [Catálogo](TAX_PARAMETERS.md) · [Regras](TAX_RULES.md) |
| Memória e confronto dos motores | [Revenda e segundo perfil de serviços](CALCULATION_REFERENCE.md) · [Experimento e fontes técnicas](evidencias/00b/FONTES_TECNICAS.md) |
| Estimativa rápida, estados e validação | [Premissas](ASSUMPTIONS.md) · [Estados e qualificação das combinações](RESULT_STATUS.md) · [Cenários de teste](TEST_SCENARIOS.md) |
| Divergência V0058/V0059, IS e bloqueios | [Exclusões](KNOWN_LIMITATIONS.md) · [Registro vigente de riscos](RISKS_AND_OPEN_QUESTIONS.md) |

### Decisões reservadas à 00C

1. Confirmar o primeiro recorte e o resultado que o usuário pode obter só com dados agregados. Definir quando solicitar descrição do item, opção, histórico ou compras.
2. Especificar as fronteiras entre entrada econômica, motor por operação, apuração empresarial, catálogo versionado e planejamento. Definir a semântica de estado e o formato mínimo exportável de replay.
3. Escolher casos prioritários para homologação, profissional responsável e referência do PGDAS/conta assistida para março de 2027. Decidir o que pode ficar restrito a simulação hipotética até haver fonte aplicável.
4. Definir atualização e qualificação de atos, notas, tabelas e combinações de JAR/base, orçamento de chamadas e comportamento em indisponibilidade.

A escolha de arquitetura, a implementação e a disponibilização pública permanecem etapas com autorizações próprias.
