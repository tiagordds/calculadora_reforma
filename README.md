# Plataforma de simulação e planejamento tributário

Projeto independente para ajudar empresas brasileiras a estimar sua carga tributária e comparar cenários com premissas, vigências e memória de cálculo visíveis. O ponto de entrada previsto é uma simulação pelo navegador, sem cadastro, com processamento no servidor.

Este repositório contém a especificação, a investigação dos motores da Receita Federal (00A) e a metodologia de apuração empresarial (00B). O exemplo de março/2027 acompanha uma revenda de Florianópolis desde os cálculos por item até o DAS e a comparação com IBS/CBS no regime regular.

| Para consultar | Documento |
|---|---|
| Visão, usuários e requisitos | [Especificação do produto](docs/PRODUCT_SPEC.md) |
| Etapas, estado e critérios de aceite | [Roadmap](docs/ROADMAP.md) |
| O que cada motor calcula e o que exige do chamador | [Motores oficiais](docs/OFFICIAL_ENGINES.md) |
| Contratos HTTP e exemplos | [Integração](docs/API_INTEGRATION.md) |
| Ambiente, experimentos e reprodução | [Infraestrutura](docs/INFRASTRUCTURE.md) |
| O que cabe ao motor e o que cabe à empresa | [Matriz tributária](docs/TAX_RESPONSIBILITIES.md) · [Metodologia](docs/TAX_RULES.md) |
| Cálculo de março/2027, sensibilidade e evidências | [Memória de referência](docs/CALCULATION_REFERENCE.md) · [Ensaio por item](docs/evidencias/00b/FONTES_TECNICAS.md) |
| Legislação e valores por vigência | [Fontes](docs/TAX_SOURCES.md) · [Parâmetros](docs/TAX_PARAMETERS.md) |
| Estimativa rápida, estados e validação | [Premissas](docs/ASSUMPTIONS.md) · [Estados](docs/RESULT_STATUS.md) · [Casos de teste](docs/TEST_SCENARIOS.md) · [Limitações](docs/KNOWN_LIMITATIONS.md) |
| Incertezas e condições de lançamento | [Riscos e questões](docs/RISKS_AND_OPEN_QUESTIONS.md) |
| Escolhas do projeto e instruções de trabalho | [Decisões](docs/DECISIONS.md) · [AGENTS.md](AGENTS.md) |

Os clones, ferramentas, logs e binários locais em `scratch/` são ignorados pelo Git. A [sonda HTTP experimental](scratch/00a/probe.py) e as capturas que acompanham os documentos permitem conferir o ensaio com dados sintéticos. Os projetos oficiais e suas fixtures são da Receita Federal do Brasil, sob as licenças indicadas no relatório.
