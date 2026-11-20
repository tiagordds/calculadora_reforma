# Fase 01 · Da cópia do repositório à primeira página

**Em 19/11/2026, a Fase 01 aguarda autorização específica do titular.** Sua entrega será uma página local em português, acessível pelo navegador, que explica o perfil de revenda planejado e onde a calculadora ficará disponível. A página terá teste HTTP e instruções reproduzíveis. O desenvolvimento fiscal começa na 02.

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

## Sequência autorizável

1. Ler `AGENTS.md`, [produto](PRODUCT_SPEC.md), [decisões](DECISIONS.md) e [roadmap](ROADMAP.md). Conferir estado local, registrar objetivo, dependências, riscos e aceites da **01**. Usar a cópia de trabalho com a 00C; se a revisão só existir localmente, conservá-la ao mudar de branch.
2. Em diretório novo, a forma de obter as revisões disponíveis é `git clone https://github.com/tiagordds/calculadora_reforma.git`. Entrar na raiz, verificar `git status --short --branch` e `git log -3 --oneline`. Em checkout existente pular a clonagem. Conferir `python --version` ou `py -3.14 --version` antes de criar o ambiente. Em Linux usar `python3.14 --version`.
3. Criar e selecionar o ambiente isolado conforme o SO. Na primeira autoria, escrever os dois arquivos de dependências com os pins diretos acima. Instalar, inspecionar `python -m pip freeze` e resolver transitivas e marcadores nos dois SOs. Não copiar um freeze global. Para as instalações seguintes usar os arquivos versionados resultantes.
4. Criar `manage.py` e pacote `config` mínimos a partir das convenções geradas por Django. Se usar `python -m django startproject config .`, retirar configurações automáticas de admin/sessões, URL de admin, chave embutida e arquivos de esqueleto sem uso antes de prosseguir. Criar o pequeno pacote `web` com os arquivos da tabela, em vez de gerar modelos. Configurar middleware, templates, estáticos, hosts e chave.
5. Implementar a página e o teste. A seção sobre a calculadora informa o que estará disponível, sem CTA que aponte a uma rota inexistente e sem campos ou resultados fiscais fictícios.
6. Executar os comandos de verificação abaixo, abrir o navegador, conferir largura de celular, teclado, folha estática e ausência de dependência dos motores. Repetir em ambiente limpo a partir da cópia do repositório, usando as versões congeladas. Documentar o SO realmente exercitado.
7. Rever o diff e a lista de arquivos, documentar a execução e fechar a fatia no roadmap. Registrar divergências de instalação e SO. Solicitar autorização própria para a 02.

### Windows PowerShell

Comandos previstos para a raiz do projeto, **na futura 01**. `.venv` será local ao checkout. Usar o executável do ambiente evita alterar políticas de ativação do PowerShell.

```powershell
py -3.14 --version
py -3.14 -m venv .venv
$phasePython = '.\.venv\Scripts\python.exe'
& $phasePython -m pip install -r requirements-dev.txt
& $phasePython -m pip check
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = '1'
$env:DJANGO_ALLOWED_HOSTS = '127.0.0.1,localhost,testserver'
& $phasePython -m django --version
& $phasePython manage.py check
& $phasePython -m pytest -q
& $phasePython manage.py runserver 127.0.0.1:8000
```

### Linux

```sh
python3.14 --version
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DJANGO_DEBUG=1
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,testserver
python -m django --version
python manage.py check
python -m pytest -q
python manage.py runserver 127.0.0.1:8000
```

Abrir `http://127.0.0.1:8000/` em navegador local. Em outro terminal, `curl.exe -I http://127.0.0.1:8000/` (Windows) ou `curl -I http://127.0.0.1:8000/` (Linux) deve retornar 200 para HEAD. Encerrar o servidor com Ctrl+C. O conteúdo e o CSS são verificados por GET no navegador. A geração da chave acima apenas a coloca no ambiente do processo local. Para uso posterior na mesma sessão, manter a mesma chave.

## Testes e aceite da 01

| Verificação | Estímulo e retorno esperado |
|---|---|
| Instalação | Em venv limpo instalar os arquivos versionados, conferir versões e `pip check` sem conflitos. Documentar Windows e Linux separadamente, inclusive lacuna se algum não foi exercitado |
| Configuração | `manage.py check` sem erros. Com chave ausente, falha de configuração identificável. Com debug omitido, desligado. `manage.py findstatic web/site.css` encontra o arquivo do app |
| Cliente HTTP, sem JVM nem banco em disco | GET e HEAD em `/`, status 200, UTF-8, título e `lang` esperados, descrição do recorte e link interno válido. POST em `/` não inicia operação (405 com CSRF válido). Caminho inexistente retorna 404. Ausência de valores que aparentem cálculo |
| Navegador | CSS local carregado, título e texto legíveis a 320 px, sem rolagem horizontal, ação navegável por teclado e foco visível. Rodar com JavaScript desativado. Registrar SO/navegador, URL local, entrada e resultado |
| Repositório | `git diff --check` e `git status --short`. Apenas arquivos previstos, nenhum segredo, binário/clone, banco, cache ou venv no histórico. README permite repetir do zero |

[DECISÃO] Aceitar a fundação quando instalação, inicialização, página, testes e documentação forem demonstrados, indicando evidência por ambiente e eventuais pendências de compatibilidade. Docker é ensaio da 02, com prova operacional exigida antes da consolidação/produção. Disponibilidade de PGDAS de março/2027, taxa regular da CBS e profissional responsável condicionam habilitação fiscal posterior. A 01 não inclui cálculo, adaptadores, containers definitivos, modelos de usuário/empresa, dados salvos, CI remoto nem deploy. [Bloqueios e etapas](ROADMAP.md)
