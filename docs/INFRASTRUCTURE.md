# Execução interna e caderno de experimentos

**19/11/2026 · Fase 00A.** Os dois motores foram compilados, testados e executados separadamente no Windows. Cada JAR precisa de Java 21, caminho de trabalho previsível e base SQLite compatível. O Simples depende dos dados publicados com o regular. Uma instância do serviço regular em execução não foi necessária para o Simples responder. [Regular](evidencias/00a/regular.json) · [Simples](evidencias/00a/simples.json)

## Ambiente e dependências

| Item | Ambiente observado |
|---|---|
| Host | Windows 10 x64 build 19045, Ryzen 9 5900X, 12 núcleos / 24 processadores lógicos, 32 GiB de RAM física. Execução nativa em máquina de trabalho, processos medidos um por vez. |
| Build | Git 2.51.1.windows.1, Eclipse Temurin JDK 21.0.13+9 x64, Maven Wrapper 3.2.0 com Maven 3.9.5. O ZIP portátil do JDK foi conferido contra SHA-256 publicado pela API Adoptium: `a4dbaa05fca4bd89d84584e58c459bd732efebb1722af80ab13c6516832004f9`. JDK e cache Maven em `scratch/`. |
| Motores | Spring Boot 3.5.16, web MVC/Tomcat, Spring Data JPA/Hibernate, sqlite-jdbc, Caffeine, Bean Validation, Springdoc 2.8.9, Actuator/Micrometer. Flyway Maven 11.7.2 durante a geração. No regular, JEXL avalia expressões do banco. JUnit/Surefire e JaCoCo no build. |
| Rede e ferramentas | GitHub e Maven Central necessários para obter fontes e dependências em instalação limpa. Download do JDK via Adoptium. Sandbox bloqueou a saída inicial para esses hosts. A obtenção foi feita com acesso autorizado. Python 3.14.0 e biblioteca padrão apenas como cliente de ensaio e leitor SQLite. |
| Artefatos | Os JARs medem 92,36 MiB (regular) e 85,78 MiB (Simples). Cada cópia da V0059 ocupa 5,23 MiB. Para dimensionar a imagem, somar JVM, bibliotecas nativas/temporários e reserva operacional. Fontes, cache de build e relatórios só são necessários na investigação/build. |

Os POMs, os scripts de wrapper e seus destinos de download, o workflow do Simples, o perfil offline, os callbacks e a organização do SQL foram inspecionados antes do uso. A aplicação abre `calculadora/db/calculadora-pro.db` com SQLite `mode=ro`. O regular usa as portas padrão 8080/9101, o Simples 8082/9103 (HTTP/gestão). Cache e pool de conexões são internos à JVM. [POM regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/pom.xml) · [Perfil regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/resources/application-offline.yml) · [POM Simples](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/pom.xml) · [Perfil Simples](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/resources/application-offline.yml)

## Reproduzir a montagem

Os blocos abaixo pressupõem uma área nova ou clones nas revisões indicadas, JDK 21 selecionado em `JAVA_HOME` e o diretório atual na raiz do projeto. O ensaio original usou `git clone --depth 1` em `main` e registrou os SHAs e tags de HEAD. Para recuperação futura, use as tags abaixo e confira os SHAs completos no inventário. Os clones originais continuam em `scratch/regular` e `scratch/simples`.

```powershell
git clone --depth 1 --branch 1.6.1 https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git scratch/regular
git clone --depth 1 --branch 0.0.6 https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional.git scratch/simples
git -C scratch/regular rev-parse HEAD
git -C scratch/simples rev-parse HEAD
$lab = (Resolve-Path scratch).Path
$env:MAVEN_USER_HOME = "$lab/maven"
$env:MAVEN_SKIP_RC = "1"
$repoArg = "-Dmaven.repo.local=$lab/maven/repository"
Set-Location "$lab/regular"
New-Item -ItemType Directory -Force calculadora/db | Out-Null
.\mvnw.cmd -B -ntp $repoArg flyway:migrate "-Dflyway.configFiles=flyway/flyway-pro.conf"
New-Item -ItemType Directory -Force ../simples/calculadora/db | Out-Null
Copy-Item calculadora/db/calculadora-pro.db ../simples/calculadora/db/calculadora-pro.db
.\mvnw.cmd -B -ntp $repoArg package
```

[EXECUTADO] A geração aplicou 59 migrações, com baseline, scripts de manutenção e callbacks oficiais. A primeira montagem Maven/Flyway reportou 28,998 s incluindo resolução de dependências. A base reportou `PRAGMA integrity_check → ok` e nenhuma linha em `PRAGMA foreign_key_check`. O nome da última migração e a data da versão do conteúdo ficam em `VERSAO_BASE_DADO`. O histórico técnico fica em `flyway_schema_history`. [SQL, saídas e hashes](evidencias/00a/inventario.json) · [Configuração Flyway](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/flyway/flyway-pro.conf)

**Controle V0058.** Gerar uma segunda base a partir das mesmas fontes, até a migração 58, em arquivo próprio. O JAR do Simples foi empacotado após a suíte bem-sucedida com essa base. Na inicialização HTTP dos dois serviços, o nome padrão selecionou V0059. Maven aceita `-o` após abastecer o cache.

```powershell
# A partir de scratch/regular, depois do bloco anterior
.\mvnw.cmd -B -ntp $repoArg flyway:migrate "-Dflyway.configFiles=flyway/flyway-pro.conf" "-Dflyway.target=58" "-Dflyway.url=jdbc:sqlite:file:../simples/calculadora/db/compat58-pro.db?foreign_keys=ON"
Set-Location "$lab/simples"
$testTmp = (New-Item -ItemType Directory -Force "$lab/junit-tmp").FullName
$env:JAVA_TOOL_OPTIONS = "-Djava.io.tmpdir=`"$testTmp`""
$localDbArg = "-Dapplication.db.download.url=http://127.0.0.1:1/"
.\mvnw.cmd -B -ntp $repoArg $localDbArg test
# O comando acima reproduz as duas falhas conhecidas da V0059
.\mvnw.cmd -B -ntp $repoArg $localDbArg "-Dapplication.db.filename=compat58-pro.db" package
```

Em Linux, usar `./mvnw` (ou `sh mvnw`), `mkdir -p`, `cp` e os mesmos argumentos Maven/JDBC nas mesmas pastas de trabalho. A execução desta investigação ocorreu no Windows.

### Testes existentes realmente executados

| Tentativa | Casos Surefire | Resultado e diagnóstico |
|---|---:|---|
| Regular 1.6.1 + V0059, `package` | 1.090 listados | 1.080 executados com sucesso, 10 pulados, zero falhas/erros. JAR gerado. |
| Simples 0.0.6 + V0059, `package`, parâmetros padrão | 155 | 66 erros. O contexto de integração não conseguiu resolver `application.db.download.url`, mesmo com o banco presente. |
| Simples + V0059, `-o package` e propriedade explícita de URL | 155 | Duas falhas de asserção e dois erros de limpeza de diretórios temporários JUnit no Windows restrito. |
| Simples + V0059, `-o test`, mesma URL, temporário controlado e permissão local | 155 | 153 passaram, 2 falhas, nenhum erro ambiental. `classificacoesSemTratamentoImplementado_conformeACargaVigente` e `naoImplementadoTambemEmNfse` divergem sobre 820001. |
| Simples + V0058, `-o package`, mesmo ambiente, arquivo alternativo | 155 | 155 passaram. JAR gerado mantendo o código original. |

Apenas a base e a sua seleção mudam entre os dois últimos conjuntos de testes. O fallback de download do Simples não foi necessário para servir dados. A primeira tentativa de sondagem HTTP concluiu o regular e parou antes do Simples porque seu JAR ainda não havia sido empacotado. A campanha registrada abaixo foi refeita integralmente após a solução do build. Os resultados de software e compatibilidade não constituem ensaio de UI ou validação fiscal. [Resultados de build](evidencias/00a/inventario.json) · [Detalhe de 820001](OFFICIAL_ENGINES.md)

## Reexecutar os testes HTTP locais

Na raiz, em um shell novo com Java 21 no PATH, usar Python 3.11+ e os JARs gerados nas respectivas pastas `target/`. O script inicia seus próprios processos em loopback, verifica portas, envia somente fixtures e encerra as JVMs. A saída padrão fica em `scratch/results`. Para usar um JDK portátil, indicar o caminho do executável.

```powershell
python scratch/00a/probe.py
```

No Windows, usar caminho absoluto de Java quando a pasta de trabalho do subprocesso mudar. O comando efetivamente executado para as capturas preservadas foi:

```powershell
$java = (Resolve-Path 'scratch/jdk/jdk-21.0.13+9/bin/java.exe').Path
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" scratch/00a/probe.py --java $java --output docs/evidencias/00a
```

O perfil offline foi iniciado com `-Xmx512m`, portas 18080/18082 (HTTP) e 19101/19103 (gestão), todas as interfaces dos serviços presas a `127.0.0.1`. A opção `--versao.url=http://127.0.0.1:1/unavailable` tornou indisponível o comparador e `--management.tracing.enabled=false` desativou o tracing. As sondagens rodaram no ambiente de rede restrita, separado do download. Versão, classificação, consulta de alíquota e cálculos aplicáveis responderam sem acesso bem-sucedido ao piloto. O comparador, acionado também na inicialização, faz retentativas. No regular o cliente remoto usa `RestTemplate` sem timeouts explícitos nesse serviço. No Simples o perfil configura conexão/leitura de 5/10 s. A prova cobre os caminhos exercitados, sem interceptação de pacotes. [Sonda e lista de chamadas](../scratch/00a/probe.py) · [Comparador regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/150cccbe414d4a5edea703e4f7a424af5aa222c7/src/main/java/br/gov/serpro/rtc/domain/service/offline/VersaoOfflineService.java) · [Comparador Simples](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/api/versao/service/VersaoOfflineService.java) · [Download condicional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/blob/c5b0f01c8351c3f0d0795cc617b29d233e9f98df/src/main/java/br/gov/serpro/rtc/config/db/DatabaseDownloadService.java)

### Medições observadas

| Medida local | Regular | Simples |
|---|---:|---:|
| Lançamento do processo até primeiro HTTP 200 da rota de versão local | 16,95 s | 15,15 s |
| Primeira chamada de cálculo do caso de referência, após consultas de catálogo | 287,22 ms | 91,64 ms |
| Mediana de 10 repetições do mesmo POST de um item, já aquecido | 32,81 ms | 32,96 ms |
| Mínimo–máximo nessas 10 amostras | 11,77–41,84 ms | 12,37–39,10 ms |
| Quatro POSTs de valores diferentes liberados por barreira, tempo individual | 8,79–37,96 ms | 12,41–40,04 ms |
| Respostas simultâneas HTTP 200 iguais ao corpo de sua referência serial | 4/4 | 4/4 |
| Memória residente após início / após a série, em MiB | 562,25 / 573,67 | 399,66 / 398,84 |
| Pico de memória residente reportado pelo SO durante o processo | 580,63 MiB | 475,35 MiB |
| CPU acumulada após início / após a série, em segundos de processador | 48,47 / 51,31 | 41,97 / 43,91 |

[EXECUTADO] Cliente Python, relógio monotônico, HTTP em loopback, leitura integral do corpo. Um processo por vez, sem Django, proxy, TLS ou usuários externos. “Início” inclui espera pela primeira leitura de versão e resolução de conexão. É uma inicialização medida por motor na campanha final. O cliente criou conexões para cada chamada. As amostras não medem vazão sustentada, p95 de produção, consumo em contêiner nem latência de simulação empresarial. A memória residente inclui a JVM fora do heap. O limite de heap usado no experimento é uma configuração, não um mínimo. [Amostras individuais do regular](evidencias/00a/regular.json) · [Amostras individuais do Simples](evidencias/00a/simples.json)

## Execução em contêiner e hospedagem

[HIPÓTESE] Um contêiner por serviço com runtime Java 21, JAR, diretório de trabalho fixo e arquivo SQLite montado para leitura atende ao desenho observado. Disponibilizar diretório temporário gravável para JVM/driver. Preparar o banco fora do processo que atende requisições. O Simples admite baixar a base se ausente e houver URL configurada. Para reprodução, fornecer previamente a cópia verificada. Separar rede de aplicação e gestão, limitar lote e concorrência no chamador e verificar uma leitura funcional de versão/base para prontidão. Reservar memória nativa além de heap, manter processos aquecidos se a latência exigir e testar reinício com a edição de base anterior disponível.

[EXECUTADO] `docker version` identificou o cliente 28.5.1. A checagem com o contexto do usuário também não encontrou o pipe `dockerDesktopLinuxEngine`. Os clones principais não traziam Dockerfile. Não houve build de imagem, Compose, medição em Linux ou seleção de provedor. A qualificação de hospedagem exige ensaio de longa duração, limites de CPU/memória, comportamento das filas/pools, variabilidade, retentativas, privacidade dos logs e recuperação de uma cópia externa. O código de configuração permite métricas, Swagger e logs de depuração. Proteger portas e verificar o que é registrado antes de trafegar informações reais.

## Recuperar os componentes

[EXECUTADO] Preservamos, fora do histórico Git, os dois arquivos ZIP gerados por `git archive HEAD` nos commits fixados, os dois JARs e os dois bancos em `scratch/preservado-00a/`. Os clones, ZIP original do JDK e cache Maven também continuam no laboratório. O [inventário](evidencias/00a/inventario.json) contém tamanho e SHA-256 de cada arquivo preservado. No Windows, `Get-ChildItem scratch/preservado-00a -File | Get-FileHash -Algorithm SHA256` confere o conteúdo. Em Linux, usar `sha256sum scratch/preservado-00a/*`. Para replay, recuperar o JAR e banco corretos, conferir os hashes, posicionar sob a raiz do serviço e reexecutar a entrada preservada com o perfil documentado.

A cópia atual está em um único host. Uma regeneração por Flyway pode ter hash binário diferente por metadados de migração. Recompilar também pode alterar metadados de empacotamento. Para recuperar os bytes do ensaio, usar os arquivos preservados. Retenção durável, cópia externa e ensaio de restauração fora desta máquina ficam pendentes antes do uso de resultados persistidos.

### Ensaio de restauração local

[EXECUTADO] Em três inicializações adicionais, abrimos os JARs preservados com diretórios de trabalho separados, copiando a base arquivada para `calculadora/db/calculadora-pro.db` e verificando o hash da cópia. Usamos loopback nas portas 18200 e 19200. Com V0059, quatro corpos HTTP de sucesso foram integralmente reproduzidos (dois de cada motor). Com o mesmo JAR do Simples e V0058, a revenda de R$ 950,00 permaneceu idêntica. A NFS-e 820001 voltou a `NAO_IMPLEMENTADO`, com `VSN-027` e sem total. Nas seis chamadas o HTTP foi 200. Isso verifica a recuperação local dos recortes e a dependência da base com uma diferença observável. [Seis retornos](evidencias/00a/replay.json) · [Script de restauração](../scratch/00a/replay.py)

Para repetir com as cópias preservadas, executar na raiz `python scratch/00a/replay.py --java CAMINHO_ABSOLUTO_DO_JAVA`. O script lê as entradas arquivadas em `docs/evidencias/00a/` e grava o novo resultado em `scratch/results/replay.json`. Nesta execução foi usado `--output docs/evidencias/00a/replay.json` para conservar a captura.

## Diagnóstico de desenvolvimento na 00C

[EXECUTADO] 19/11/2026, PowerShell na raiz da cópia de trabalho Windows. Sondas de leitura; nenhum serviço foi iniciado. A existência do cliente Compose é verificável separadamente do daemon e de uma imagem executável.

| Comando e entrada | Retorno observado |
|---|---|
| `python --version` e `py -0p` | Ambos 0. Python 3.14.0, instalação de usuário 64 bits da série 3.14 |
| `python -m pip show Django pytest pytest-django` | 0 pelo pacote encontrado: pytest 9.0.2 global. Aviso de Django e pytest-django ausentes. A 01 criará ambiente próprio |
| `git --version` | 0, 2.51.1.windows.1 |
| `Get-Command python,py,java,docker -ErrorAction SilentlyContinue` | Python, launcher e Docker localizados; Java ausente no PATH (retorno 1) |
| `& 'scratch/jdk/jdk-21.0.13+9/bin/java.exe' -version` | 0, Temurin 21.0.13+9 LTS preservado no laboratório |
| `docker context show` e `docker compose version` | 0 em ambos, contexto `desktop-linux`, Compose `v2.40.2-desktop.1` |
| `docker version` | 1. Cliente 28.5.1; pipe `dockerDesktopLinuxEngine` não encontrado. Sem seção Server. Docker/Compose em execução continuam pendentes |

[DECISÃO] Na 01 usar ambiente Python local e servidor em `127.0.0.1:8000`. O [plano de execução](PHASE_01_PLAN.md) especifica dependências, variáveis de ambiente, arquivo de exemplo, comandos e testes nos dois SOs. Na 02 usar Java 21 local com o par preservado se o daemon ainda estiver indisponível. Para o ensaio Compose, montar base em leitura, temporário gravável, imagem de runtime fixada por digest e web em rede privada com o regular; mapear apenas a web em loopback. A gestão e a porta do cálculo permanecem internas. Confirmar o acesso por nome de serviço e a restauração da edição anterior. Ensaiar a primeira integração em containers na 02; se houver impedimento ambiental, registrar a integração nativa separadamente. Exigir o ensaio Linux/Compose para o aceite operacional da 05 e antes de qualquer publicação.

### Metas a medir, a partir das observações da 00A

[HIPÓTESE] As medianas aquecidas de 32,81/32,96 ms vieram de 10 POSTs de um item, Windows em loopback, um processo Java por vez. Somar os dois picos individuais (580,63 + 475,35 MiB) dá cerca de 1,03 GiB apenas como ordem de grandeza da memória residente; essa soma não mede as duas JVMs simultâneas. Acrescentar web, SO, proxy, cache de páginas do sistema, temporários, observabilidade e folga. Iniciar cada JVM por cálculo acrescentaria os 15–17 s de inicialização observados. Manter aquecido apenas o motor exigido pelo perfil habilitado.

| Caminho ou recurso | Alvo de ensaio e método | Reação a falha |
|---|---|---|
| Página inicial | LCP p75 ≤ 2,5 s em navegador móvel simulado, cache frio, viewport e perfil de rede fixados no relatório | Medir peso do CSS/HTML e recursos bloqueantes |
| Cálculo agregado rápido | p95 ≤ 0,5 s do POST à resposta HTML no servidor. Zero POSTs fiscais. Medir tradicional e híbrido condicional com saída parcial | Isolar resolução de catálogo e custo de construir a memória |
| Cálculo com JVM pronta | p95 ≤ 2 s do POST web à resposta; prazo de parede de 5 s por pedido. Medir aquecido e primeiro canário separadamente | Informar indisponibilidade/saturação e preservar resultados independentes no prazo |
| Memória e CPU | Para primeiro ensaio Linux: RSS alvo até 768 MiB por JVM e 256 MiB para web de um worker. Medir serviço isolado, depois ambos simultâneos e sob repetição; registrar pico do conjunto, CPU, OOM e reinícios | Se exceder, ajustar heap/concorrência e repetir antes de dimensionar |
| Concorrência e volume | Um usuário, depois 4 usuários simultâneos; admissão inicial até 2 operações em voo por motor no total. No mínimo 100 requisições por perfil aquecido, registrar p50/p95, vazão, erros e amostra. 1 documento/cenário, até 2 cenários e 10 itens por entrada rápida; na 02 apenas um item | Recusar trabalho acima do orçamento antes do fan-out. Sem fila persistente. Saturação retorna resposta curta e recuperável |
| Falhas | Ensaiar um timeout, hash incorreto, lote parcial, concorrência entre casos distintos e reinício com comparador remoto inacessível. Medir tempo até resposta e retorno à prontidão | Nenhum zero substituto, cruzamento de usuário ou total indevido. Contar falhas por estágio |

Medir também um ciclo sustentado (proposta de 30 min) com cenários sintéticos alternados e períodos diferentes de aquecimento. Comparar corpos e estados a referências seriais antes de aceitar concorrência. Medições do navegador, servidor e motor usam relógios e amostras separados. Recalibrar metas na 05, registrando SO, CPU/memória, runtime, versões, dados, percentis e carga. [Limites do pedido](SECURITY.md)

Cache de resultados fiscais só se a medição mostrar necessidade. Preferir reutilizar catálogo público imutável por revisão. Qualquer chave de cálculo precisaria distinguir entradas normalizadas, fato/competência, território, condições, cenário, regras, parâmetros, premissas e par JAR/base. Manter dados/resultados privados fora de cache compartilhado. A primeira versão não precisa de filas, cache fiscal ou processamento assíncrono.

### Alternativas para a primeira hospedagem

[DOCUMENTADO][DECISÃO] Comparação conceitual em 19/11/2026. Não há orçamento monetário nem dimensionamento contratado. Para cotar na 06, usar região e moeda explícitas, horas das JVMs prontas, CPU/RAM medidas conjuntamente, tráfego, armazenamento versionado, backups, retenção de métricas, impostos e trabalho de operação.

| Modelo | Distribuição e disponibilidade | Operação, custo recorrente e recuperação |
|---|---|---|
| VPS Linux | Proxy TLS, web e containers privados em um host. Começar com um motor quando o recorte permitir. Falha do host afeta o conjunto | Custo de capacidade reservada mesmo em repouso. Equipe cuida de SO, certificados, alertas e recuperação. Restaurar manifesto e imagens em outra VM; snapshot sozinho não qualifica o replay. [Exemplo de snapshots de instância](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-instance-snapshots-in-amazon-lightsail.html) |
| Plataforma gerenciada de containers | Web com HTTPS gerenciado e motores acessíveis só pela rede privada/identidade de serviço. Verificar suporte a processos aquecidos, tempo máximo e espaço temporário | Instância mínima reduz partida fria e gera custo quando ociosa. Fixar artefatos fora de disco efêmero, medir latência entre serviços e custo mínimo de ambos ativos. [Instâncias mínimas no Cloud Run](https://docs.cloud.google.com/run/docs/configuring/min-instances) |
| Serviços gerenciados em cloud | Tarefas em sub-redes privadas, balanceador/TLS, repositório de artefatos e monitoramento. Banco gerenciado somente com escrita própria | Maior custo operacional inicial de configurar rede, identidade e políticas; pagar por tarefas, balanceador, logs, cópias e tráfego. Pode distribuir réplicas quando houver demanda. [Rede de tarefas no Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html) |

Recomendação para a prova interna: um host Linux controlado com serviços privados. Para a primeira oferta online, escolher entre VPS e containers gerenciados **após** o ensaio de carga/recuperação e a análise de quem consegue operar atualizações e incidentes. Monitorar disponibilidade da web, prontidão por motor, taxa de falhas, latência e memória, sem registrar a simulação. Definir objetivo de recuperação com o titular antes de contratar e medir uma restauração completa.

### Preservação fora da estação e restauração futura

A cópia da 00A em um host já permitiu replays locais. Para uso durável, inventariar bytes dos JARs, bases, fontes fixadas, SQL, tabelas/leiautes, runtime, regras próprias, premissas e manifesto com hash e licença/avisos por componente. Conferir separadamente os termos das nomenclaturas/dados e dos binários de terceiros. Se a redistribuição for vedada, documentar aquisição permitida e limites de recuperação. Em etapa autorizada, manter segunda cópia privada, versionada, com acesso mínimo, integridade conferida e política de preservação das revisões referenciadas. Sem dados de simulações anônimas nesses backups.

Para aceitar a recuperação, usar host limpo: obter manifesto e artefatos pelos IDs, conferir SHA-256 antes de iniciar, restaurar diretório/temporário, subir em rede isolada, conferir versão local e canário, repetir C03 e um caso de divergência em ambiente de teste, confrontar corpo/estados e registrar tempo e diferenças. Preservar bytes originais pois recompilar ou remigrar pode mudar metadados e hash. Em falha listar o artefato ausente e restringir o replay. Nenhum binário ou base foi transferido pela 00C. [Política de versões](API_INTEGRATION.md)
