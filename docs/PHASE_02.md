# Fase 02 · operação C03 pelo navegador

## Abertura em 20/11/2026

[DECISÃO] O titular autorizou a primeira operação de revenda com o regular. Ponto de partida conferido com `git status --short --branch` e `git rev-parse HEAD origin/main`: árvore limpa, ambas as referências em `71065ef5f73274a1771243359d4dffa19b89ebd1`.

| Aspecto | Registro de abertura |
|---|---|
| Objetivo | Levar a confirmação da hipótese de CBS até o retorno real do regular e a memória no navegador. |
| Dependências | Django da 01, Requests previsto na 00C, Java 21, JAR 1.6.1 e SQLite V0059 com hashes do inventário, navegador local. Compose depende do daemon Linux. |
| Plano | Conferir artefatos e dependências, iniciar serviço offline privado, qualificar canário, implementar formulário e adaptador, testar respostas históricas e reais, desligar e restaurar o motor, registrar replay e interface. |
| Riscos | Base divergente, HTTP 200 parcial, tempo de leitura superior ao orçamento, confusão entre hipótese e alíquota definitiva. Limitar concorrência, verificar estados e expor escopo por item. |
| Conclusão | C03 exato (incluindo memória), ensaio separado de tpDoc 55, C15, C16 e C20, testes offline e reais separados, navegador a 320 px e desktop com teclado, falha visível e ambiente documentado. Registrar eventual bloqueio Docker e pendência de homologação fiscal. |

## Resultado e integridade

[EXECUTADO] Em 20/11/2026, o POST da operação devolveu HTTP 200 com `CALCULO_SIMULADO`, aviso `x-warning-dados-simulados: 6` e versões `1.6.1` e `V0059`. O corpo completo do C03, incluindo as três memórias textuais, os zeros e as escalas, coincide com `cases[0].body` da 00B. A variação com `"tpDoc": 55` (inteiro no nível da operação) teve o mesmo corpo. As entradas, cabeçalhos tributários e respostas estão nas [capturas original](evidencias/02/c03.json), [com modelo 55](evidencias/02/c03-tpdoc55.json) e [Linux/amd64](evidencias/02/c03-linux.json).

| Campo do C03 | Retorno em reais |
|---|---:|
| CBS sob a hipótese explícita de 10% | 10,00 |
| IBS estadual | 0,05 |
| IBS municipal | 0,05 |
| Total de IBS do motor | 0,10 |
| Soma decimal dos totais de IBS e CBS | **10,10** |

A base documental é R$ 100,00. O preço final pago pelo cliente está ausente da entrada. A soma usa somente os dois totais oficiais devolvidos. Os componentes do IBS já estão incluídos no total de IBS.

[EXECUTADO] `git -C scratch/regular rev-parse HEAD` e `Get-FileHash scratch/regular/target/api-regime-geral.jar,scratch/regular/calculadora/db/calculadora-pro.db` na estação Windows identificaram o conjunto abaixo. Os dois hashes coincidem com o inventário e a captura da fase anterior. O adaptador relê os bytes dos arquivos utilizados antes do intercâmbio. O banco do perfil offline abre em `mode=ro`. [Inventário 00A](evidencias/00a/inventario.json) · [Referência 00B](evidencias/00b/reference.json)

| Artefato | Identificação |
|---|---|
| ReceitaFederal/calculadora-rtc-regime-regular | `150cccbe414d4a5edea703e4f7a424af5aa222c7`, versão 1.6.1 |
| api-regime-geral.jar | SHA-256 `3f7baa20442301e2ba6733fc274263a8756a7e21b3ed4e4020b0f1ecf51f9d61` |
| calculadora-pro.db | V0059, data declarada 30/09/2026, SHA-256 `4160a29e4f1a6a2c4f2d5d5527b64af2a84fb4ea2915693b70104865db533293` |
| Ambiente nativo | CPython 3.14.10, Django 5.2.19, Temurin 21.0.13+9, OpenSSL 3.5.4 do Git para Windows |

Para recuperar binários ausentes nesta estação, use as cópias homônimas de `scratch/preservado-00a/` e coloque-as nos dois caminhos da tabela de hashes acima indicados pelo comando. Em uma máquina sem o acervo, a recuperação a partir do código fixado está no [caderno de infraestrutura](INFRASTRUCTURE.md). Uma recompilação com outros bytes fica fora do conjunto admitido até nova qualificação. As imagens experimentais recebem JAR e base por montagem em tempo de execução.

## Caminho do pedido e falhas

[CÓDIGO] O navegador envia apenas o token CSRF e a confirmação `confirm_cbs=yes` a `/operacao/caneta/`. O Django verifica nomes, unicidade, conteúdo e tamanho e o serviço monta o C03. O adaptador lê a versão local e faz um POST por submissão. Ao iniciar cada JVM, o lançador verifica Java, hashes e canário completo antes de disponibilizar a identidade de cliente daquela instância. Uma porta HTTP de gestão fica desabilitada. [Adaptador](../adapters/regular.py) · [Transporte](../adapters/transport.py) · [Lançador](../adapters/launch.py)

[CÓDIGO] Até dois cálculos em voo por processo Django no ensaio de uma instância. Um terceiro recebe 429 antes de chamar o motor. Conexão de até 0,5 s e leitura inativa de 2 s. O limite de 1 MiB é aplicado ao corpo em streaming, inclusive sem Content-Length. O cliente exige resposta sem compressão, ignora proxies e credenciais do ambiente e desativa redirects e repetição de POST. Compara versões antes/depois, reconcilia itens únicos, classificação, base, alíquotas, valores, memória, total e avisos. Conserva códigos e ponteiros dos itens rejeitados. [Interpretação](../adapters/result.py)

[CÓDIGO][EXECUTADO] O orçamento de 5 s começa no middleware da operação. Há reserva de 150 ms para encerramento do leitor e renderização do HTML. Em leitura contínua lenta o processo Django encerra o **cliente Python** por prazo de parede e libera a vaga. A mesma JVM permanece ativa. A medição cobre chegada ao Django até o retorno HTML local. Agendamento do SO, chegada do corpo à camada WSGI, trânsito ao navegador e conclusão de um POST já recebido pelo Java não têm prazo rígido garantido por esse mecanismo. A admissão global precisa ser redimensionada se o servidor ganhar mais processos.

[DOCUMENTADO][EXECUTADO] Requests 2.34.2 requer Python ≥3.10. `python -m pip install -r requirements-dev.txt` e `python -m pip check` resolveram os pins nos dois ambientes. No Windows, `Invoke-RestMethod https://pypi.org/pypi/<pacote>/<versão>/json` retornou lista `vulnerabilities` vazia para Requests e os quatro pins transitivos. O aviso GHSA-gc5v-m9x4-r6x2 registra correção em 2.33.0. Consulta limitada aos avisos conhecidos em 20/11/2026. [Distribuição](https://pypi.org/project/requests/2.34.2/) · [Aviso do mantenedor](https://github.com/psf/requests/security/advisories/GHSA-gc5v-m9x4-r6x2) · [Semântica de timeout](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)

## Campanha em 20/11/2026

[EXECUTADO] Comandos a partir da raiz, `python` do ambiente da aplicação e chave de desenvolvimento efêmera nas suítes Django. A [instalação e partida nativas](../README.md#iniciar-o-motor-e-reproduzir-a-operação) incluem a geração da chave. Para repetir uma camada offline isolada, use `python -m pytest tests/unit -q`, `python -m pytest tests/contract -q` ou `python -m pytest tests/test_home.py -q`.

| Camada e comando | Entrada e resultado |
|---|---|
| Software e contratos · `python -m pytest -q -s` | 70 aprovados e quatro de integração desmarcados em cada SO de execução. Inclui os oito testes da 01, CSRF real, consentimento, recusa de campos extras e duplicados, escala, diferenças entre zero e ausência, escape de memória e proteção de respostas. |
| Prazo · `python -m pytest tests/unit/test_deadline.py -s` (também dentro da suíte completa) | Servidor de ensaio enviando bytes a cada 250 ms. O POST Django devolveu 503 em 4,871 s no Windows e 4,862 s no container. Leitura parada retornou 503 em 2,262 s e 2,390 s respectivamente. Saturação recusa nova operação. |
| Integração · `python -m pytest -q -m engine_integration --record-engine scratch/phase02/replay` | Quatro aprovados em cada ambiente, cobrindo original, modelo 55, lote misto e recusa TLS do cliente sem certificado. Para a captura versionada nativa foi usado o destino `docs/evidencias/02`. |
| C15 misto, adaptador fora do formulário | Quatro itens do lote histórico. Três simulados (incluindo zero conhecido), um rejeitado com REG-011 e ponteiro `#/itens/3/ncm`. O motor devolveu subtotal de CBS 56,76, IBS 0,64 e IS 15,00. O adaptador conserva o corpo e identifica completude parcial. [Lote real](evidencias/02/c15.json) |
| C16, exclusão offline | `tests/unit/test_operation.py` confronta as duas capturas 820001. V0058 sem total, V0059 tipo 9 e total de tributos zero. Submeter o tipo 91 e a classe ao fluxo web produz 400 antes do serviço. A fase não gera resultado empresarial. [Replay histórico](evidencias/00a/replay.json) |
| C20 e falha esperada na dependência | Com a JVM nativa parada, `python -m pytest -q -m engine_integration tests/integration/test_engine.py -k original` terminou com código 1 e “Motor indisponível”. O POST do Chrome devolveu 503 e nenhuma rubrica monetária de resultado. Após nova partida, canário e quatro testes reais aprovados. |
| C20, contrato | Hash alterado, base/versão/perfil divergentes, HTTP de erro, corpo inválido, tamanho excessivo, ID errado, item ausente/extra/duplicado, estado, memória ou total inconsistente impedem o cálculo afetado. [Contratos gravados e transporte](../tests/contract) |
| Carga local · `python scratch/02/measure.py` | Windows, JVM quente, 100 POSTs por perfil. Um usuário teve 100 sucessos, p50 0,326 s, p95 0,351 s e 3,05 sucessos/s. Com quatro usuários, 50 sucessos e 50 respostas 429, p50 0,321 s e p95 0,356 s entre os aceitos, 6,17 sucessos/s. Amostra desta estação, sem projeção de capacidade de produção. |

### Navegador real

[EXECUTADO] Chrome 157.0.8103.79, Playwright 1.65.2, em 1366 × 900 e 320 × 720. Em ambas as larguras, Tab, Espaço e Enter permitiram sair da home, confirmar e enviar o formulário sem JavaScript. O resultado recebeu foco. A memória e o JSON abriram por teclado, com largura do documento igual à viewport. Os pedidos registrados pelo navegador ficaram na origem Django. A repetição após desligar a JVM retornou 503. As capturas mostram somente dados sintéticos. [Sucesso desktop](evidencias/02/sucesso-1366.png) · [Sucesso 320 px](evidencias/02/sucesso-320.png) · [Indisponibilidade desktop](evidencias/02/indisponivel-1366.png) · [Indisponibilidade 320 px](evidencias/02/indisponivel-320.png)

Na estação preservada, com o servidor web ativo, execute os comandos abaixo em momentos distintos. O segundo pressupõe que o lançador do motor foi encerrado. O terceiro usa o Compose ativo. O script verifica o código de resposta esperado e termina com falha se o serviço estiver em outro estado.

```powershell
$browserPython = 'scratch/phase01/browser/Scripts/python.exe'
& $browserPython tests/browser/check_pen.py --state online --output scratch/phase02/browser
& $browserPython tests/browser/check_pen.py --state offline --output scratch/phase02/browser
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8003 --state online --output scratch/phase02/browser-linux
```

Em outra estação, instale Chrome e crie um venv de ensaio para `playwright==1.65.2`. O browser automatizado é o canal `chrome`. O Windows foi o host do navegador inclusive quando Django e Java rodaram nos containers.

[EXECUTADO] O primeiro E2E revelou 403 com token válido. O Chrome enviava origem nula no POST sob a política `no-referrer`. Com `same-origin`, o Chrome confirmou a origem e o Django manteve as verificações CSRF. Outra falha de teste, no formulário inteiramente vazio, foi corrigida indicando Content-Type explícito no cliente de teste. As campanhas acima são posteriores às correções.

## Compose Linux

[EXECUTADO] Inicialmente `docker info` falhou pela ausência do pipe `dockerDesktopLinuxEngine`. `wsl -l -v` indicou `docker-desktop` parado. `docker desktop start --timeout 45` retornou 0. `docker version` e `docker compose version` identificaram Docker Desktop 4.48.0, Engine 28.5.1 Linux/amd64 e Compose v2.40.2-desktop.1. As imagens-base foram resolvidas por `docker buildx imagetools inspect` e fixadas pelos digests dos índices OCI no [Dockerfile](../Dockerfile).

| Imagem-base do ensaio | Digest |
|---|---|
| python:3.14.10-slim-trixie | `sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f` |
| eclipse-temurin:21.0.13_9-jre-noble | `sha256:b4f9d2a0bc273417cf5219b7b832bbf0493ed500b7b57d5001d9f83374659060` |

```powershell
$env:DJANGO_SECRET_KEY = & .venv/Scripts/python -c "import secrets; print(secrets.token_urlsafe(50))"
docker compose up -d --build --wait --wait-timeout 120
docker compose exec -T web python -m pytest -q -s -p no:cacheprovider
docker compose exec -T web python -m pytest -q -m engine_integration --record-engine /tmp/phase02 -p no:cacheprovider
docker compose ps
```

[EXECUTADO] `docker inspect` confirmou `RW=false` nas montagens do JAR e da SQLite. `docker network inspect calculadora-fase02_fiscal --format '{{.Internal}}'` retornou `true`. O backend tem credencial em volume de leitura. A porta publicada do Django é `127.0.0.1:8003`. O serviço regular usa apenas a rede fiscal sem porta publicada. `docker cp calculadora-fase02-web-1:/tmp/phase02/c03.json docs/evidencias/02/c03-linux.json` preservou a captura. Entrada, corpo completo, versões, hashes e cabeçalhos tributários coincidiram com o Windows. Para encerrar o ensaio local em outro momento use `docker compose down` no mesmo ambiente. A reprodução nativa em Linux permanece pendente.

## Entrega e limites do aceite

| Arquivos | Alteração |
|---|---|
| `web/forms.py`, `web/middleware.py`, `web/templates/web/pen.html` | Novos. Consentimento, cabeçalhos, limite de corpo e página da operação. |
| `config/settings.py`, `config/urls.py`, `web/views.py`, `web/templates/web/home.html`, `web/static/web/site.css` | Integração com a página inicial existente, rota, tratamento de erro e apresentação responsiva. |
| `simulation/{__init__,example,service}.py`, `adapters/{__init__,manifest,launch,regular,transport,result}.py` | Novos. Entrada fixa, estados e replay, lançamento, transporte e interpretação. |
| `requirements.txt`, `pytest.ini`, `tests/test_home.py` | Pins de runtime herdados por requirements-dev, marcador de integração e atualização da ação da home. |
| `tests/conftest.py`, `tests/unit/test_{operation,deadline}.py`, `tests/contract/test_{results,transport}.py`, `tests/integration/test_engine.py`, `tests/browser/check_pen.py` | Suítes independentes e captura opcional de exemplos reais. |
| `.dockerignore`, `Dockerfile`, `compose.yaml`, `.gitignore`, `scratch/02/measure.py` | Ambiente privado de ensaio e medição sintética. |
| README, changelog e documentos de arquitetura, API, dados, decisões, experiência, estados, infraestrutura, riscos, roadmap, segurança e testes | Comandos, limites e evidências da fase. `docs/PHASE_02.md` reúne o aceite e `docs/evidencias/02/` conserva quatro JSON e quatro capturas. |

[DECISÃO] Critérios técnicos da Fase 02 satisfeitos para esta revenda, nos dois ambientes ensaiados. A base permite planejar a execução da 03 mediante autorização independente. Permanecem pendentes a revisão tributária profissional, a elegibilidade da empresa, as referências do período para o DAS e a política de histórico e centavos da futura apuração. O resultado desta fase é exploratório e local.

[EXECUTADO] `git ls-remote origin refs/heads/main` confirmou a publicação da 01 em `71065ef5f73274a1771243359d4dffa19b89ebd1`. A entrega da 02 está na árvore de trabalho de `main`, sem commit, push ou publicação de imagem. O formulário nativo usa a porta 8002 para preservar o serviço preexistente na 8000.
