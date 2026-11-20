# Plataforma de simulação e planejamento tributário

Projeto independente para ajudar empresas brasileiras a estimar sua carga tributária e comparar cenários com premissas, vigências e memória de cálculo visíveis. O ponto de entrada previsto é uma simulação pelo navegador, sem cadastro, com processamento no servidor.

Na Fase 01, a página inicial apresenta a revenda de canetas em Florianópolis em março/2027 e a comparação planejada para o Simples Nacional. Os cálculos serão disponibilizados nas próximas etapas. As investigações dos motores (00A), a metodologia (00B) e o planejamento (00C) permanecem nas referências abaixo.

## Executar localmente

Use a raiz de uma cópia que contenha `manage.py`. Para obter as revisões publicadas, use `git clone https://github.com/tiagordds/calculadora_reforma.git` e `cd calculadora_reforma`. Enquanto a Fase 01 estiver apenas na árvore de trabalho, use essa árvore ou uma cópia incluindo os arquivos novos da fase.

O ambiente de referência usa CPython 3.14.10, Django 5.2.19 LTS e, para testes, pytest 9.2.0 e pytest-django 4.14.0. O arquivo `requirements-dev.txt` inclui as dependências de execução. Para apenas abrir a aplicação, instale `requirements.txt` e pule o comando de testes.

### Windows PowerShell · executado

Com o Python Install Manager, extraia o interpretador uma vez na cópia local. Se já tiver o 3.14.10 instalado, confira com `py -3.14 --version` e use `py -3.14 -m venv .venv` no lugar dos comandos de extração e criação abaixo.

```powershell
py install --target=scratch/phase01/python 3.14.10
.\scratch\phase01\python\python.exe -m venv .venv
$phasePython = '.\.venv\Scripts\python.exe'
& $phasePython -m pip install -r requirements-dev.txt
& $phasePython -m pip check
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
& $phasePython manage.py check
& $phasePython -m pytest -q
$env:DJANGO_DEBUG = '1'
& $phasePython manage.py runserver 127.0.0.1:8000
```

### Linux · instruções documentadas

Use CPython 3.14.10 com suporte a `venv` e a base de fusos horários do sistema. Confira o patch antes de criar o ambiente.

```sh
python3.14 --version
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
python manage.py check
python -m pytest -q
export DJANGO_DEBUG=1
python manage.py runserver 127.0.0.1:8000
```

Abra [a página inicial local](http://127.0.0.1:8000/). Para encerrar o servidor iniciado no terminal, pressione Ctrl+C. Nas próximas sessões, reutilize o ambiente virtual e gere a chave antes de iniciar o processo.

`DJANGO_SECRET_KEY` é obrigatória. `DJANGO_DEBUG` aceita `0` (padrão) ou `1`. Os comandos usam `1` para servir o CSS no servidor de desenvolvimento em loopback. `DJANGO_ALLOWED_HOSTS` aceita nomes separados por vírgula e tem padrão `localhost,127.0.0.1`. O pytest-django permite `testserver` durante os testes. A configuração lê o ambiente do processo. O arquivo `.env.example` apenas ilustra as variáveis. SQLite opera em memória e a página dispensa migrações, Java, Docker e bases fiscais.

O [registro da Fase 01](docs/PHASE_01_PLAN.md) reúne os testes de software, as verificações no navegador e o alcance da reprodução por sistema.

## Referências do projeto

| Para consultar | Documento |
|---|---|
| Visão, usuários e requisitos | [Especificação do produto](docs/PRODUCT_SPEC.md) |
| Arquitetura, contratos, parâmetros e replay | [Arquitetura](docs/ARCHITECTURE.md) · [Modelo de dados](docs/DATA_MODEL.md) |
| Experiência, wireframes e tratamento de dados | [Experiência web](docs/WEB_EXPERIENCE.md) · [Segurança e privacidade](docs/SECURITY.md) |
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
