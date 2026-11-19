# Roadmap

**Posição em 19/11/2026.** Inicialização documental e investigação técnica 00A encerradas. A próxima decisão do responsável pelo projeto é autorizar a 00B. O caso 820001 e a origem das alíquotas de 2027 seguem abertos. Há informações suficientes para iniciar o trabalho de matriz quando autorizado.

| Fase | Entrega e critério de conclusão | Estado |
|---|---|---|
| 00A · Motores oficiais | Identificar revisões e contratos, executar operações e erros por motor, registrar cobertura, serviço interno, testes, limitações e questões para a matriz. | Concluída no escopo investigativo |
| 00B · Matriz, metodologia e riscos | Atribuir responsabilidades por tributo, nível de processamento, vigência e origem. Delimitar lacunas empresariais, créditos, fontes e metodologia de comparação. | Aguarda autorização |
| 00C · Arquitetura, produto e planejamento | Escolher recorte verificável do MVP, jornada, arquitetura mínima e casos de referência. Validar hipóteses de produto e mercado. | Planejada |
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

A primeira hipótese de trabalho para a 00B é delimitar um perfil de atividade em que se possa reconciliar o valor do documento com a apuração mensal, declarando as informações adicionais e a origem das alíquotas. A ordem das fases de implementação deve ser revista se esse recorte não tiver referência independente.
