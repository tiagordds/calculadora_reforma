# Plataforma de simulação e planejamento tributário

Projeto independente para ajudar empresas brasileiras a estimar sua carga tributária e comparar cenários com premissas, vigências e memória de cálculo visíveis. O ponto de entrada previsto é uma simulação pelo navegador, sem cadastro, com processamento no servidor.

Este repositório contém a especificação e a investigação da Fase 00A. O primeiro software executado aqui pertence aos projetos oficiais da Receita Federal. Os comandos da investigação, as condições de reprodução e os limites de uso dos resultados estão no relatório de infraestrutura.

| Para consultar | Documento |
|---|---|
| Visão, usuários e requisitos | [Especificação do produto](docs/PRODUCT_SPEC.md) |
| Etapas, estado e critérios de aceite | [Roadmap](docs/ROADMAP.md) |
| O que cada motor calcula e o que exige do chamador | [Motores oficiais](docs/OFFICIAL_ENGINES.md) |
| Contratos HTTP e exemplos | [Integração](docs/API_INTEGRATION.md) |
| Ambiente, experimentos e reprodução | [Infraestrutura](docs/INFRASTRUCTURE.md) |
| Incertezas e condições de lançamento | [Riscos e questões](docs/RISKS_AND_OPEN_QUESTIONS.md) |
| Escolhas do projeto e instruções de trabalho | [Decisões](docs/DECISIONS.md) · [AGENTS.md](AGENTS.md) |

Os clones, ferramentas, logs e binários locais em `scratch/` são ignorados pelo Git. A [sonda HTTP experimental](scratch/00a/probe.py) e as capturas que acompanham os documentos permitem conferir o ensaio com dados sintéticos. Os projetos oficiais e suas fixtures são da Receita Federal do Brasil, sob as licenças indicadas no relatório.
