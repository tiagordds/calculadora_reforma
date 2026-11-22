# Fase 05 · Consolidação do MVP interno

**Concluída tecnicamente para ensaio local com dados sintéticos.** As três jornadas da revenda de março/2027 passaram na regressão e no navegador. A Fase 06 segue bloqueada. A [matriz de prontidão](#matriz-de-prontidão) identifica as condições de cada estágio.

## Abertura em 21/11/2026

[DECISÃO] O titular autorizou a consolidação interna das três jornadas no recorte da 04. Objetivo: conferir integração, semântica, segurança, capacidade e recuperação com dados sintéticos. Dependências: revisão c9a330a, capturas e artefatos preservados, Python fixado, Java 21, Chrome e Compose locais. Antes das alterações, git status --short --branch mostrou main limpa; git rev-parse HEAD origin/main e git ls-remote origin refs/heads/main coincidiram em c9a330a33201e7a3d4074aa46084ac2679b237b3.

[DECISÃO] Plano: reproduzir a base em outro checkout, auditar formulários, estados e memória, corrigir desvios com regressão, exercitar navegador e falha/restauração do motor, medir carga local e preparar confronto por caso e decisão de prontidão. Riscos: confundir guia com obrigação, hipótese com direito, checkout local com backup externo e automação com observação humana. Aceite técnico exige regressão offline e real separadas, jornadas integradas, medições controladas, recuperação demonstrada e registro de bloqueios materiais. PGDAS do período, contas assistidas, revisor, participantes autorizados e host independente são dependências externas. A autorização termina na 05.

## Resultado das três jornadas

| Jornada | Resultado sintético conferido | Limite preservado |
|---|---|---|
| C03 por item | Caneta de base R$ 100,00. CBS de R$ 10,00 e IBS de R$ 0,05 por ente. Corpo idêntico à captura da 00B. | A CBS de 10% exige aceite. A indisponibilidade da JVM afeta o item. |
| C01 tradicional | RBT12 de R$ 1,2 milhão, efetiva de 8,825% e DAS bruto de R$ 8.825,00. Ao reduzir o primeiro dos doze meses reais para R$ 80 mil, o histórico cai a R$ 1,18 milhão e o DAS a R$ 8.793,22. | Origem e janela do histórico visíveis. Resíduo de R$ 0,01 entre soma das rubricas e global do exemplo. A guia requer conciliação. |
| Comparação mensal | Para as mesmas vendas de R$ 100 mil, obrigação híbrida após créditos de R$ 15.717,31, R$ 14.202,31 ou R$ 12.687,31, conforme a sensibilidade. | O crédito ausente conserva o bruto conhecido e deixa aberta a diferença após créditos. Opção, potencial do adquirente e extinções têm verificações próprias. |

[CÓDIGO][EXECUTADO] O atalho de exemplo aceitava um campo CSRF repetido com token válido. Passou a rejeitar o pedido antes do cálculo. O resumo de erros duplicava identificadores e mostrava nomes internos. Agora o link rotulado leva ao campo, que tem uma única mensagem associada. A home identifica o DAS bruto, o comparador identifica a origem do histórico e a taxa escolhida, e a apresentação de lote parcial nomeia o subtotal de IBS. A quebra de palavras na introdução corrigiu o estouro observado na ampliação a 200%.

[CÓDIGO][EXECUTADO] Com venda sintética de R$ 0,01, a obrigação híbrida exata chegava a cerca de R$ 0,00159 e aparecia como R$ 0,00. A tela passou a distinguir valor inferior a um centavo, zero exato e dado em aberto. Quando há resíduo, explicita a diferença entre as parcelas exibidas e a soma calculada antes de arredondar. O teste de regressão confere o valor positivo, o negativo e a ausência.

## Campanhas e evidências

| Ambiente | Regressão offline | Motor real | Prova adicional |
|---|---:|---:|---|
| Windows nativo, checkout limpo da 04 | 170 aprovados | 4 aprovados | Venv novo, JAR/base restaurados, replays e canário. |
| Windows nativo, árvore da 05 | 174 aprovados | 4 aprovados, repetidos após restauração | Chrome em 1366/320 px, histórico real, parcial, correção e 503. |
| Linux x86_64 em Compose, 05 | 174 aprovados | 4 aprovados, repetidos após restauração | Backend e JVM em containers, Chrome no Windows. Replays cruzados e regressão em container sem rede externa. |
| Linux em distribuição WSL de uso geral | Não executado | Não executado | Somente a distribuição interna do Docker Desktop estava instalada. |
| Linux nativo em host independente | Não executado | Não executado | Sem máquina disponibilizada. |

- [Matriz fiscal C01–C21 e dossiê de créditos com procedimento de confronto](evidencias/05/CONFRONTO.md)
- [Auditoria de acessibilidade e roteiro de observação para gestor e contador](evidencias/05/EXPERIENCIA.md)
- [Segurança, avisos do motor, inventário, capacidade e recuperação](evidencias/05/OPERACAO.md)
- [Manifesto do software e memórias reproduzidas](evidencias/05/manifesto.json) · [Dependências, licenças e hashes](evidencias/05/inventario.json)
- [Medições no Windows](evidencias/05/windows.jsonl) · [Medições no Compose](evidencias/05/compose.jsonl)

[EXECUTADO] Foram 3.600 requisições medidas, com 3.500 sucessos e 100 recusas de admissão esperadas, todas no C03 a quatro clientes. Houve zero falhas inesperadas de conteúdo ou status. As metas locais de p95 de 500 ms nos agregados e 2 s no item aquecido foram atendidas. O comparador respondeu com duas operações C03 em andamento e durante a parada completa da JVM. Medições limitadas à estação e ao processo web único de cada ambiente.

## Matriz de prontidão

| Dimensão | Estado | Evidência | Pendência, consequência e ação | Responsável ou etapa |
|---|---|---|---|---|
| Funcionamento técnico interno | Atendido | Três jornadas, refinamentos e retornos parciais conferidos. | Moderada: manter lista de perfis e verificar a cada revisão. | Engenharia |
| Qualidade e regressão do recorte | Atendido | 174 offline e 4 reais por ambiente, fronteiras e replays. | Alta se mudar motor ou regra. Repetir qualificação do componente. | Engenharia |
| Experiência e acessibilidade | Parcialmente atendido | Teclado, nomes, foco, erros, leitura móvel e caminhos sem JS no Chrome. | Alta para guias e créditos. Observar as duas personas e testar leitura assistida. | Produto e participantes autorizados |
| Segurança e privacidade | Parcialmente atendido | Validação no servidor, CSRF, escape, logs amostrados, isolamento, mTLS e limites efetivos. | Alta para promoção. Tratar avisos do Tomcat embutido, borda TLS, segredos e retenção no destino. | Engenharia e segurança antes de exposição |
| Desempenho interno | Atendido | 1, 2 e 4 clientes, medições por jornada e replay. | Alta se extrapolado. Dimensionar implantação e admissão no destino. | Infraestrutura em etapa autorizada |
| Reprodução e recuperação | Parcialmente atendido | Checkout limpo, código arquivado, hashes, parada e restauração. | Alta em perda da estação. Preservar cópia externa autorizada e restaurar em outro host. | Titular e infraestrutura |
| Compatibilidade operacional | Parcialmente atendido | Windows nativo e Compose Linux. | Moderada. Comprovar SO e rede no destino. Linux nativo independente pendente. | Engenharia e infraestrutura |
| Homologação fiscal | Não atendido | Matriz e dossiê prontos, aritmética confrontada com 00B. | Bloqueadora. Obter PGDAS, contas assistidas, documentos e parecer do PA. | Profissional tributário a designar |
| Licenças e distribuição | Parcialmente atendido | Fontes, pins, artefatos e avisos identificados. | Bloqueadora para distribuição. Conferir direitos e obrigações da mídia concreta. | Titular e assessoria jurídica |
| Autorização de publicação | Não atendido | Autorização alcança apenas a 05. | Bloqueadora. Delimitar público, finalidade, infraestrutura e aprovar expressamente. | Titular |

[DECISÃO] Estágio atingido: **MVP interno técnico**. Uma versão experimental restrita exige autorização e público, infraestrutura e privacidade definidos. Homologação exige contraprova e parecer do PA. Publicação controlada depende também de direitos, segurança, recuperação no destino e decisão do titular. Próximo passo recomendado: designar revisor tributário e responsável pela triagem do motor. O roteiro humano pode ser aplicado internamente quando houver participantes autorizados.

## Repetir as provas

### Revisão para versionamento em 22/11/2026

[DECISÃO] Conferir os 17 arquivos modificados e os dez novos do fechamento contra `c9a330a`, o manifesto e as capturas sintéticas. O aceite desta revisão requer que a suíte offline, a checagem Django e os replays funcionem com os arquivos da entrega, sem depender de dados privados ou temporários. O principal risco é aprovar um pacote que só possa ser conferido com o conteúdo de `scratch/` desta estação.

[DOCUMENTADO] As capturas sintéticas da 05 acompanham a entrega. O [C01](evidencias/05/c01.json) preserva a apuração tradicional. Os cenários de crédito [zero](evidencias/05/zero.json), [intermediário](evidencias/05/middle.json) e [alto](evidencias/05/high.json) preservam a comparação. O [C03 da 02](evidencias/02/c03.json) conserva a resposta por item. Os cinco hashes canônicos constam no [manifesto](evidencias/05/manifesto.json). Para conferir os hashes de código, testes e parâmetros em checkouts Windows, normalize CRLF para LF.

[DOCUMENTADO] No ambiente Python do projeto, a partir da raiz, com a chave Django efêmera configurada conforme o README, execute os replays offline:

```powershell
python manage.py replay_traditional docs/evidencias/05/c01.json
foreach ($case in 'zero','middle','high') { python manage.py replay_comparison "docs/evidencias/05/$case.json" }
python -m pytest -q tests/contract/test_results.py::test_c03_exact_wire_and_amounts tests/test_traditional.py::test_c12_shift_and_refine
```

[EXECUTADO] O inventário de entrada repetiu os 17 arquivos modificados e os dez novos do fechamento. A revisão acrescentou as quatro capturas empresariais que só estavam em `scratch/`, registrou sua reprodução e atualizou o roadmap. As entradas das quatro capturas coincidiram com os exemplos sintéticos arquivados nas fases 03 e 04. Os 31 arquivos selecionados são textos UTF-8. A inspeção da seleção e a busca por identificadores pessoais formatados, chaves privadas, tokens e credenciais em URLs não apontaram dados reais ou segredos. Os JSONL contêm medições agregadas.

[EXECUTADO] Em 22/11/2026, `git checkout-index --all --prefix=<diretório-novo>/` exportou o índice para um diretório vazio. No Windows, nessa cópia e com o venv do projeto, `python -m pytest -q` retornou **174 aprovados e quatro integrações desmarcadas** em 12,55 s. `python manage.py check` retornou zero problemas. Os quatro comandos de replay reproduziram integralmente o C01 e as três sensibilidades. O teste dirigido do refinamento confirmou R$ 8.793,22. No C03, entrada e corpo da 02 coincidiram com a referência da 00B e o adaptador apurou R$ 10,10 da captura. Os 12 arquivos de código e testes, os cinco parâmetros e as cinco memórias conferiram com os hashes registrados. A comparação com a base preservou as evidências até a 04, os adaptadores, os parâmetros e os módulos de cálculo e simulação. `git diff --check` e `git diff --cached --check c9a330a` retornaram 0. Para o motor ao vivo, a carga e a restauração, valem as campanhas de 21/11, com os limites da matriz de prontidão.

### Campanhas registradas em 21/11/2026

[DOCUMENTADO] Na raiz, prepare o ambiente e inicie o [motor privado conforme o README](../README.md#iniciar-o-motor-e-reproduzir-a-operação). A suíte padrão dispensa o Java. A seleção de integração requer o canário pronto. Em um terminal PowerShell:

```powershell
$phasePython = (Resolve-Path .venv/Scripts/python.exe).Path
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = '0'
& $phasePython -m pip check
& $phasePython manage.py check --deploy
& $phasePython -m pytest -q
& $phasePython -m pytest -q -m engine_integration
& $phasePython manage.py runserver 127.0.0.1:8055 --noreload --insecure
```

[DOCUMENTADO] Com o servidor ativo, em outro terminal, grave novas saídas em scratch. O navegador da estação usa Playwright 1.65.2 e canal chrome. Conserve a chave da sessão Compose durante a parada e a restauração.

```powershell
$browserPython = 'scratch/phase01/browser/Scripts/python.exe'
$phasePython = '.venv/Scripts/python.exe'
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
$target = 'scratch/phase05/repeticao'
& $browserPython tests/browser/check_traditional.py --origin http://127.0.0.1:8055 --output $target
& $browserPython tests/browser/check_comparison.py --origin http://127.0.0.1:8055 --output $target
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8055 --state online --output $target
& $browserPython tests/browser/check_accessibility.py --port 8055
& $phasePython manage.py replay_traditional "$target/c01.json"
foreach ($case in 'zero','middle','high') { & $phasePython manage.py replay_comparison "$target/$case.json" }
& $phasePython tests/performance/measure_local.py --port 8055 --output "$target/windows.jsonl"
docker compose -p calculadora-fase05 up -d --build --wait --wait-timeout 150
docker compose -p calculadora-fase05 exec -T web python -m pytest -q -p no:cacheprovider
docker compose -p calculadora-fase05 exec -T web python -m pytest -q -m engine_integration -p no:cacheprovider
& $phasePython tests/performance/measure_local.py --port 8003 --output "$target/compose.jsonl"
docker compose -p calculadora-fase05 stop regular
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8003 --state offline --output "$target/parada"
& $browserPython tests/browser/check_comparison.py --origin http://127.0.0.1:8003 --output "$target/parada"
docker compose -p calculadora-fase05 up -d --no-recreate --wait --wait-timeout 150
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8003 --state online --output "$target/restaurado"
docker compose -p calculadora-fase05 down
```

[DOCUMENTADO] Para restaurar a revisão versionada em diretórios novos, use o acervo da 00A e os comandos abaixo. Inicie o lançador no checkout com caminhos absolutos para Java e OpenSSL e a porta 18080 livre. O checkout da 04 reproduz as sensibilidades históricas. A captura original de C01 usa o código da 03. A reprodução da candidata 05 depende da árvore identificada no manifesto até decisão de versionamento.

```powershell
$lab = 'scratch/phase05/novo'
New-Item -ItemType Directory $lab
git bundle create "$lab/base.bundle" main
git clone "$lab/base.bundle" "$lab/checkout"
git -C "$lab/checkout" switch --detach c9a330a
$checkout = (Resolve-Path "$lab/checkout").Path
scratch/phase01/python/python.exe -m venv "$checkout/.venv"
$cleanPython = "$checkout/.venv/Scripts/python.exe"
& $cleanPython -m pip install -r "$checkout/requirements-dev.txt"
New-Item -ItemType Directory -Force "$checkout/scratch/regular/target","$checkout/scratch/regular/calculadora/db"
Copy-Item scratch/preservado-00a/api-regime-geral.jar "$checkout/scratch/regular/target/"
Copy-Item scratch/preservado-00a/calculadora-pro.db "$checkout/scratch/regular/calculadora/db/"
$env:DJANGO_SECRET_KEY = & $cleanPython -c "import secrets; print(secrets.token_urlsafe(50))"
Push-Location $checkout
& $cleanPython -c "from adapters.manifest import verify_artifacts; verify_artifacts()"
& $cleanPython -m pytest -q
foreach ($case in 'zero','middle','high') { & $cleanPython manage.py replay_comparison "docs/evidencias/04/$case.json" }
git worktree add --detach ../phase03 c515471
& $cleanPython ../phase03/manage.py replay_traditional ../phase03/docs/evidencias/03/c01.json
Pop-Location
```

[EXECUTADO] O manifesto usa SHA-256 dos módulos e templates modificados com quebras de linha normalizadas para LF. Para conferir cada memória, remover apenas a chave de horário de execução (`processed_at` ou `executed_at`) do objeto raiz e calcular SHA-256 de `json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")`. Os dados do inventário de parâmetros são hashes dos bytes da cópia examinada. No fechamento, índice Git limpo, 17 arquivos rastreados modificados e 10 novos. A comparação com c9a330a das evidências históricas, adaptadores, parâmetros, cálculo e simulação retornou 0.
