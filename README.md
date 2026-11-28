# Plataforma de simulação e planejamento tributário

Projeto independente para ajudar empresas brasileiras a estimar sua carga tributária e comparar cenários com premissas, vigências e memória de cálculo visíveis. O ponto de entrada previsto é uma simulação pelo navegador, sem cadastro, com processamento no servidor.

A página inicial oferece três experiências para uma papelaria de Florianópolis em março de 2027. Em **Comparar Simples tradicional e híbrido**, informe o preço das mesmas vendas para ver quanto a loja deve no mês em cada modalidade. Você pode explorar três exemplos sintéticos ou informar históricos, exclusões, opção e créditos próprios. A tela mostra o que falta para calcular o líquido. A **calculadora tradicional** mantém a estimativa mensal e sua extrapolação anual condicionada. A **operação da caneta** consulta o motor oficial regular para um item. [Comparador, testes e replay](docs/PHASE_04.md) · [Calculadora tradicional](docs/PHASE_03.md) · [Operação por item](docs/PHASE_02.md)

## Executar localmente

Para estimar o DAS de um mesmo CNPJ com comércio e serviços, abra **Estimar o DAS de atividades mistas** na página inicial. O exemplo sintético permite alterar as receitas de março, as receitas históricas segregadas e a folha de cada mês. [C09, memórias e comandos de replay](docs/SIMPLES_MIXED_01.md)

No mesmo formulário, **Comparar usando estes dados** leva a empresa e o histórico tradicional ao comparador de março/2027. Informe o histórico híbrido, as exclusões e os créditos por tributo ou explore o exemplo de R$ 60 mil de comércio e R$ 40 mil de serviços. [Comparação mista, cinco memórias e reprodução](docs/SIMPLES_MIXED_HYBRID_01.md)

A quarta jornada é a de [serviços do Simples tradicional](http://127.0.0.1:8005/simples/servicos/). Para desenvolvimento de software sob encomenda em Florianópolis, o formulário aceita o histórico de receita e folha, apresenta o Fator R, o anexo e o DAS bruto com ISS. O exemplo de 28% pode ser editado para reproduzir a mudança de anexo por um centavo. [Recorte, fontes e reprodução do C08](docs/SIMPLES_SERVICES_01.md)

Use a raiz desta cópia, que contém `manage.py`. A Fase 05 consolidou o **MVP interno para ensaio sintético** em Windows e Compose. O relatório inclui a matriz de prontidão, as condições de revisão profissional e os comandos para repetir as jornadas. [Consolidação da Fase 05](docs/PHASE_05.md)

Para reproduzir as memórias arquivadas, use uma cópia separada na revisão correspondente. A Fase 04 está versionada em `c9a330a33201e7a3d4074aa46084ac2679b237b3` e a Fase 03 em `c5154719dd39ad3b52b3193f11689d34fdb5aace`. Para a **Fase 02**, execute `git clone https://github.com/tiagordds/calculadora_reforma.git`, entre no clone e execute `git switch --detach dcedd7576e6f3a96cab4278bedb2bf61dd43de7b`. O cálculo real de item exige também o JAR e a base qualificados conforme o relatório da 02.

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
$env:DJANGO_DEBUG = '0'
& $phasePython manage.py runserver 127.0.0.1:8005 --noreload --insecure
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
export DJANGO_DEBUG=0
python manage.py runserver 127.0.0.1:8005 --noreload --insecure
```

Abra o [comparador mensal](http://127.0.0.1:8005/simples/comparar/), a [calculadora tradicional](http://127.0.0.1:8005/simples/tradicional/) ou a [operação da caneta](http://127.0.0.1:8005/operacao/caneta/). Para encerrar o servidor iniciado no terminal, pressione Ctrl+C. Nas próximas sessões, reutilize o ambiente virtual e gere a chave antes de iniciar o processo.

`DJANGO_SECRET_KEY` é obrigatória. O exemplo usa debug desligado e `--insecure` para servir o CSS com o servidor de desenvolvimento. `DJANGO_ALLOWED_HOSTS` tem padrão `localhost,127.0.0.1`. O arquivo `.env.example` ilustra o ambiente do processo. A aplicação dispensa migrações. A página inicial, o formulário e a suíte padrão funcionam com o motor desligado.

### Iniciar o motor e reproduzir a operação

Em outro terminal, na mesma raiz, use os caminhos da instalação preservada no Windows. O lançador confere os dois SHA-256, prepara credenciais locais e só habilita o cálculo após o canário. No Linux com os mesmos artefatos, Java 21 e OpenSSL 3 no PATH, o equivalente é `.venv/bin/python -m adapters.launch`.

```powershell
.\.venv\Scripts\python.exe -m adapters.launch --java "scratch/jdk/jdk-21.0.13+9/bin/java.exe" --openssl "C:/Program Files/Git/usr/bin/openssl.exe"
```

Espere a mensagem **Motor pronto**. Abra a operação, marque a confirmação e pressione **Calcular a operação**. Para conferir o ambiente em um terceiro terminal PowerShell, na raiz, execute:

```powershell
$phasePython = '.\.venv\Scripts\python.exe'
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
& $phasePython -m pytest -q
& $phasePython -m pytest -q -m engine_integration --record-engine scratch/phase02/replay
```

A primeira suíte usa referências gravadas. A segunda exige a JVM e grava apenas os exemplos sintéticos no destino indicado. Para conferir a falha no navegador, encerre o lançador com Ctrl+C e envie a confirmação novamente. Reinicie o lançador para restaurar o serviço. O [relatório da fase](docs/PHASE_02.md) inclui a prova em Chrome, comandos do Compose e restauração dos binários.

O [registro da Fase 01](docs/PHASE_01_PLAN.md) reúne os testes de software, as verificações no navegador e o alcance da reprodução por sistema.

A partir da calculadora de serviços, **Comparar usando estes dados** leva o faturamento e o histórico ao [comparador C08](http://127.0.0.1:8005/simples/servicos/comparar/). O formulário admite históricos diferentes e mostra quanto da obrigação de março já pode ser calculado. [Exemplo, memória e replay](docs/SIMPLES_SERVICES_HYBRID_01.md)

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
