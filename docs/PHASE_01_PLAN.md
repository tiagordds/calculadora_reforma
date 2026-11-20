# Fase 01 · Da cópia do repositório à primeira página

## Abertura · 20/11/2026

[DECISÃO] O titular autorizou exclusivamente a Fase 01. O objetivo é abrir no navegador uma página Django local em português que apresente o perfil de revenda. A execução depende do checkout da 00C, de Python, pip e acesso às distribuições. Seguir o roteiro abaixo para fixar versões, implementar a página, testar e repetir a instalação em cópia limpa.

[EXECUTADO] `git status --short --branch` mostrou a árvore limpa em `main...origin/main`. Em `git log -5 --oneline --decorate`, HEAD e origin/main apontavam para `a9f9bb2`, após `bb39b72` e `99fc807`. O Python inicial do Windows é 3.14.0. Riscos de execução incluem disponibilidade dos patches, diferenças entre sistemas e confusão entre resposta HTTP e apresentação no navegador. O aceite exige instalação reproduzida, página com CSS e âncora funcionais, verificações da tabela de aceite e registro dos limites por ambiente.

## Pré-requisitos e versões de partida

[DECISÃO] Usar CPython **3.14.10**, Django **5.2.19 LTS**, pytest **9.2.0** e pytest-django **4.14.0**, com `venv` e `pip`. As duas últimas dependências servem aos testes. Rever correções de segurança das mesmas séries na abertura da 01 e registrar qualquer mudança e a combinação final. O Windows atual tem 3.14.0. Preparar o patch recomendado em instalação de usuário ou ambiente isolado, sem depender de alteração global no sistema. Linux requer Python da mesma série com `venv` disponível. Verificação documental de compatibilidade e medição local estão na [arquitetura](ARCHITECTURE.md) e na [infraestrutura](INFRASTRUCTURE.md).

Dependências para iniciar a execução: autorização da 01, cópia de trabalho contendo os documentos da 00C, Git, Python compatível, diretório gravável e acesso ao índice de pacotes ou a wheels previamente verificadas. JVM, bases fiscais, daemon Docker, cadastro, chaves de serviço e conta de hospedagem ficam fora do caminho crítico.

## Arquivos a entregar

| Arquivo | Função e critério de revisão |
|---|---|
| `manage.py`, `config/__init__.py`, `config/settings.py`, `config/urls.py`, `config/wsgi.py` | Projeto Django com settings únicos e rota nomeada `home` em `/`. Resolver caminhos com `pathlib`. WSGI inicializa a mesma configuração usada nos testes |
| `web/__init__.py`, `web/views.py`, `web/templates/web/home.html`, `web/static/web/site.css` | Um app de apresentação com uma view GET/HEAD, template e uma folha de estilo local. Título principal “Simulação tributária”, descrição do recorte e link funcional “Conhecer a calculadora” para seção da própria página, indicando que o cálculo estará disponível em etapa posterior |
| `requirements.txt`, `requirements-dev.txt` | Runtime separado de testes. Dev inclui `-r requirements.txt`. Fixar versões exatas das dependências diretas e transitivas resolvidas para os dois sistemas. Manter marcadores de plataforma quando uma dependência for específica, como `colorama` ou `tzdata`. Verificar a instalação limpa antes de registrar o conjunto |
| `pytest.ini`, `tests/test_home.py` | `DJANGO_SETTINGS_MODULE = config.settings`, descoberta de `test_*.py`. Testes com a fixture `client`, sem autorização de acesso a banco |
| `.env.example`, `.gitignore` e `README.md` | Exemplo só com nomes e valores inofensivos, instruções de configuração pelo shell. Ignorar `.venv/`, `.env`, caches Python/Pytest e bancos locais. Preservar regras existentes de `scratch/` e evidências rastreadas |
| Documentação existente | Registrar objetivo/aceite na abertura, versões efetivas, resultados e limitações por SO. Atualizar roadmap e changelog ao concluir |

### Configuração mínima

| Opção | Valor e comportamento esperado |
|---|---|
| Ambiente | `DJANGO_SECRET_KEY` obrigatória e lida do ambiente. Ausência encerra inicialização com mensagem pelo nome da variável, sem revelar valor. `DJANGO_DEBUG` aceita valores explícitos `0`/`1`, padrão `0`. `DJANGO_ALLOWED_HOSTS` lista separada por vírgula com padrão `localhost,127.0.0.1`. Nos testes, permitir `testserver` no ambiente de teste |
| Idioma e relógio | `LANGUAGE_CODE="pt-br"`, `TIME_ZONE="America/Sao_Paulo"`, `USE_TZ=True`. HTML com `lang="pt-BR"` e viewport. Datas fiscais futuramente carregam competência explícita |
| Aplicativos e middleware | `web` e `django.contrib.staticfiles`. Templates Django com descoberta por app e autoescape padrão. SecurityMiddleware, CommonMiddleware, CsrfViewMiddleware e XFrameOptionsMiddleware. Sem admin, autenticação, sessões, mensagens ou app fiscal na 01 |
| Estáticos e roteamento | `STATIC_URL="/static/"`. Um GET em `/` renderiza a página. Link interno resolve para seção existente. CSS servido pelo desenvolvimento local com debug habilitado. Nenhum recurso externo é necessário para renderizar a página |
| Banco | SQLite `:memory:` como backend técnico local. Sem modelos, SQL de negócio, arquivos de banco ou migrações. A página e seus testes independem de tabelas |
| Segredos | `.env.example` documenta `DJANGO_SECRET_KEY=`, `DJANGO_DEBUG=0` e `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`. O projeto lê `os.environ`. Copiar um arquivo `.env` isoladamente não configura o processo. Comandos abaixo definem os valores na sessão |

## Roteiro definido na 00C

1. Ler `AGENTS.md`, [produto](PRODUCT_SPEC.md), [decisões](DECISIONS.md) e [roadmap](ROADMAP.md). Conferir estado local, registrar objetivo, dependências, riscos e aceites da **01**. Usar a cópia de trabalho com a 00C; se a revisão só existir localmente, conservá-la ao mudar de branch.
2. Em diretório novo, a forma de obter as revisões disponíveis é `git clone https://github.com/tiagordds/calculadora_reforma.git`. Entrar na raiz, verificar `git status --short --branch` e `git log -3 --oneline`. Em checkout existente pular a clonagem. Conferir `python --version` ou `py -3.14 --version` antes de criar o ambiente. Em Linux usar `python3.14 --version`.
3. Criar e selecionar o ambiente isolado conforme o SO. Na primeira autoria, escrever os dois arquivos de dependências com os pins diretos acima. Instalar, inspecionar `python -m pip freeze` e resolver transitivas e marcadores nos dois SOs. Não copiar um freeze global. Para as instalações seguintes usar os arquivos versionados resultantes.
4. Criar `manage.py` e pacote `config` mínimos a partir das convenções geradas por Django. Se usar `python -m django startproject config .`, retirar configurações automáticas de admin/sessões, URL de admin, chave embutida e arquivos de esqueleto sem uso antes de prosseguir. Criar o pequeno pacote `web` com os arquivos da tabela, em vez de gerar modelos. Configurar middleware, templates, estáticos, hosts e chave.
5. Implementar a página e o teste. A seção sobre a calculadora informa o que estará disponível, sem CTA que aponte a uma rota inexistente e sem campos ou resultados fiscais fictícios.
6. Executar os comandos de verificação abaixo, abrir o navegador, conferir largura de celular, teclado, folha estática e ausência de dependência dos motores. Repetir em ambiente limpo a partir da cópia do repositório, usando as versões congeladas. Documentar o SO realmente exercitado.
7. Rever o diff e a lista de arquivos, documentar a execução e fechar a fatia no roadmap. Registrar divergências de instalação e SO. Solicitar autorização própria para a 02.

Os comandos de instalação, teste e inicialização para Windows PowerShell e Linux estão no [README](../README.md#executar-localmente).

## Testes e aceite da 01

| Verificação | Estímulo e retorno esperado |
|---|---|
| Instalação | Em venv limpo instalar os arquivos versionados, conferir versões e `pip check` sem conflitos. Documentar Windows e Linux separadamente, inclusive lacuna se algum não foi exercitado |
| Configuração | `manage.py check` sem erros. Com chave ausente, falha de configuração identificável. Com debug omitido, desligado. `manage.py findstatic web/site.css` encontra o arquivo do app |
| Cliente HTTP, sem JVM nem banco em disco | GET e HEAD em `/`, status 200, UTF-8, título e `lang` esperados, descrição do recorte e link interno válido. POST em `/` não inicia operação (405 com CSRF válido). Caminho inexistente retorna 404. Ausência de valores que aparentem cálculo |
| Navegador | CSS local carregado, título e texto legíveis a 320 px, sem rolagem horizontal, ação navegável por teclado e foco visível. Rodar com JavaScript desativado. Registrar SO/navegador, URL local, entrada e resultado |
| Repositório | `git diff --check` e `git status --short`. Apenas arquivos previstos, nenhum segredo, binário/clone, banco, cache ou venv no histórico. README permite repetir do zero |

[DECISÃO] Aceitar a fundação quando instalação, inicialização, página, testes e documentação forem demonstrados, indicando evidência por ambiente e eventuais pendências de compatibilidade. Docker é ensaio da 02, com prova operacional exigida antes da consolidação/produção. Disponibilidade de PGDAS de março/2027, taxa regular da CBS e profissional responsável condicionam habilitação fiscal posterior. A 01 não inclui cálculo, adaptadores, containers definitivos, modelos de usuário/empresa, dados salvos, CI remoto nem deploy. [Bloqueios e etapas](ROADMAP.md)

## Encerramento · 20/11/2026

[CÓDIGO] Árvore de trabalho sobre `a9f9bb2`. A rota nomeada `home` usa o template do app `web`, CSS local e a seção `#calculadora`. A configuração exige chave no ambiente, aceita apenas 0 ou 1 para debug, restringe hosts e usa os quatro middlewares previstos. O perfil apresentado é uma papelaria do Simples com revenda local em Florianópolis em março de 2027. [Configuração](../config/settings.py) · [Página](../web/templates/web/home.html) · [Testes](../tests/test_home.py)

[OFICIAL] Consulta em 20/11/2026. CPython 3.14.10 inclui correções de segurança. A listagem da série 3.14 em python.org e as versões estáveis disponíveis no PyPI nas séries 5.2, 9.2 e 4.14 mantinham os quatro pins da 00C. Os metadados do PyPI para as três versões diretas não listavam vulnerabilidades na consulta. [Distribuições Python](https://www.python.org/ftp/python/) · [Release do Python](https://www.python.org/downloads/release/python-31410/) · [Django](https://pypi.org/pypi/Django/5.2.19/json) · [pytest](https://pypi.org/pypi/pytest/9.2.0/json) · [pytest-django](https://pypi.org/pypi/pytest-django/4.14.0/json)

| Evidência no Windows x64, build 19045 | Entrada e resultado |
|---|---|
| [EXECUTADO] Interpretador e dependências | `py install --target=scratch/phase01/python 3.14.10` verificou a assinatura do índice e extraiu o runtime. O venv criado com esse executável retornou Python 3.14.10 em `python -VV` e pip 26.2.2 em `python -m pip --version`. `python -m pip freeze` confirmou os pins dos dois arquivos de dependências. |
| [EXECUTADO] Instalação apenas de execução | Em outro venv vazio em `scratch/phase01/runtime-only`, `python -m pip install --no-cache-dir -r requirements.txt` instalou somente Django 5.2.19, asgiref 3.13.0, sqlparse 0.6.1 e tzdata 2026.6. `python -m pip check` e `python manage.py check` retornaram 0. |
| [EXECUTADO] Reprodução da árvore de trabalho | A tentativa de clone direto do diretório local foi recusada pelo Git por divergência de proprietário. `git bundle create scratch/phase01/base.bundle main` e `git clone --quiet scratch/phase01/base.bundle scratch/phase01/checkout` reproduziram a base sem alterar a configuração de confiança. Sobre o clone em `a9f9bb2`, foram copiados os arquivos modificados e novos listados por `git ls-files --modified --others --exclude-standard`. No novo venv, `python -m pip list` mostrava apenas pip. `python -m pip install --no-cache-dir -r requirements-dev.txt` instalou os 11 pacotes fixados. `python -m pip check` retornou 0. |
| [EXECUTADO] Inicialização e isolamento | No clone, com chave efêmera e PATH limitado ao venv, `shutil.which` retornou `None` para java e docker. `python manage.py check` retornou 0 e `python -m pytest -q` passou nos oito testes. Com debug 1, `python manage.py runserver 127.0.0.1:8001 --noreload` serviu HTML e CSS por GET com 200. SQLite configurado como `:memory:`; os testes da página rodam com acesso ao banco bloqueado pelo pytest-django. |
| [EXECUTADO] Contrato de software | No checkout principal, `python -m pytest -q` também passou nos oito testes. GET e HEAD 200, corpo de HEAD vazio, título, idioma, conteúdo e âncora conferidos. POST sem token 403 e POST com token válido 405 com `Allow: GET, HEAD`. Rota inexistente 404. Chave ausente ou vazia impediu startup, debug omitido resultou em falso e os hosts padrão foram confirmados em novo processo. `python manage.py findstatic web/site.css` encontrou o CSS do app. |
| [EXECUTADO] Servidor e navegador | `python manage.py runserver 127.0.0.1:8000 --noreload` em loopback com debug 1. `curl.exe -I http://127.0.0.1:8000/` retornou 200. `scratch/phase01/browser/Scripts/python.exe scratch/phase01/check_browser.py` dirigiu o Google Chrome 157.0.8103.79 real em modo headless com Playwright 1.65.2 em venv de ensaio. Em 1366 × 900 e 320 × 720, com JavaScript da página desativado, o navegador carregou HTML e CSS locais (200), aplicou a cor do cartão e manteve a largura do documento igual à da área de leitura. Tab focou a ação com contorno de 3 px. Enter focou a seção com o título visível. As duas capturas de página inteira foram inspecionadas e estão no laboratório local em `scratch/phase01/home-1366.png` e `home-320.png`. |
| [EXECUTADO] Repositório | `git diff --check` retornou 0. `git status --short --branch --untracked-files=all` limitou as mudanças à aplicação, configuração, testes e documentação da 01. O diff de `a9f9bb2` para `docs/evidencias`, `scratch`, memória de referência e documentos de fontes, regras e parâmetros tributários ficou vazio. |

[EXECUTADO] Conferência dos metadados com `python -` no Windows. A entrada foram os pins dos dois requirements e os campos `Requires-Dist` das distribuições instaladas. Partindo de Django, pytest e pytest-django, a travessia avaliou as condições de plataforma para CPython 3.14 e conferiu cada restrição de versão. Retorno 0, com 11 pacotes para Windows e 9 para Linux. Somente tzdata (runtime) e colorama (testes) entram pelo marcador Windows.

[DOCUMENTADO] O WSL disponível listou apenas `docker-desktop`. A reprodução nativa em Linux, incluindo a disponibilidade do fuso no sistema, segue pendente. Para realizá-la, executar o bloco Linux do README em uma cópia limpa, verificar os oito testes e abrir a página e sua âncora com o CSS carregado. O ensaio em 320 px usou viewport do Chrome no Windows. Celular físico, leitor de tela e pesquisa com usuários têm evidência própria em etapas posteriores.

[DECISÃO] Critérios de software da Fase 01 atendidos no Windows. A lacuna Linux está identificada conforme a tabela de aceite. A base permite iniciar a 02 mediante autorização específica do titular e conferência do conjunto Java/JAR/base previsto para aquela fase.
