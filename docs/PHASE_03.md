# Fase 03 · Apuração rápida do Simples tradicional

## Abertura em 20/11/2026

[DECISÃO] O titular autorizou implementar e testar somente a estimativa empresarial tradicional. O ponto de partida é C01, uma loja madura com receita homogênea de revenda interna de canetas em Florianópolis em março de 2027. [EXECUTADO] `git status --short --branch` indicou árvore limpa e `git log -5 --oneline --decorate` apontou `main` e `origin/main` em `dcedd7576e6f3a96cab4278bedb2bf61dd43de7b`.

[DOCUMENTADO] Dependências da entrega local incluem Python/Django já fixados, a janela e a memória da 00B, a tabela legal de 2027–28, os contratos da 00C e o formulário privado da 02. Plano de execução:

1. Conferir a legislação e as fronteiras do caso contra as fontes da 00B.
2. Fixar uma edição do catálogo, separar premissas e implementar histórico, triagem, apuração e memória decimal em Python.
3. Entregar formulário e refinamento por POST, com validação no servidor e resultado copiável.
4. Confrontar com C01/C08–C14/C17/C21, executar regressão, navegador em duas larguras e integração já disponível. Registrar evidências sintéticas e atualizar a documentação.

[DECISÃO] Os riscos principais são escolher a janela antiga, confundir receita anual com RBT12, aceitar mudança de edição no refinamento ou atribuir ao PGDAS um ajuste de centavos inferido. O aceite técnico requer cálculo e bloqueios visíveis no navegador sem motor, revisão reproduzível, cinco estados, resíduos e testes de regressão. A revisão profissional e a autorização para a 04 continuam independentes.

## Conferência tributária antes da implementação

[OFICIAL] Corte de pesquisa em 20/11/2026. A Res. 190 foi publicada em 10/08/2026 e seu art. 9º dá efeitos às alterações a partir de 01/01/2027. Na Res. 140, os arts. 2º e 16 passam a reconhecer no mês do faturamento documentado a receita auferida. Os arts. 21–22 deslocam a janela e aplicam a regra geral a partir do 14º mês. Para março, o último mês somado é janeiro. Fevereiro/2027 pode integrar a receita acumulada no ano. O art. 45-A especifica centavos, arredondamento pelo primeiro algarismo descartado e mínimo positivo. O art. 45-B trata de extinções de IBS/CBS. [Res. 190 no sistema Normas](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/152832) · [Atualização operacional do PGDAS-D](https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/novembro/programa-gerador-do-documento-de-arrecadacao-do-simples-nacional-pgdas-d-e-atualizado-para-atender-a-reforma-tributaria-a-partir-de-novembro-de-2026)

[OFICIAL] A LC 123 disciplina limites da empresa, segregação e cálculo da efetiva. O Anexo XVIII da LC 214 fornece a tabela do comércio para 2027–28. Na quarta faixa, os seis pesos abaixo somam exatamente 100%. Na triagem, o limite geral é R$ 4,8 milhões e o sublimite é R$ 3,6 milhões. O excesso de até 20% inclusive produz, em regra, efeito no ano seguinte. Acima de 20%, a regra da empresa madura considera o mês seguinte à ultrapassagem. O ano de abertura exige fronteira proporcional e admite efeito retroativo. A tela bloqueia a simplificação quando encontra excesso. A memória identifica o ano, a grandeza, o excesso e quando os dados permitem datar o efeito. [LC 123, arts. 3º, 13-A, 18 e 20](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) · [Anexo XVIII, tabela 1](https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-anexo-pl.pdf)

[DOCUMENTADO] A conferência manteve a janela e os valores da 00B. Houve uma precisão de referência no caderno de regras. A Res. 190, art. 8º, revoga os arts. 10, 11, 13 e 14 da Res. 140 em 2027. A triagem usa os arts. 9º e 12 e reserva o cálculo especial do art. 24. O sublimite de 2026 abrange ICMS e ISS e tem fonte própria. A Res. 195 trata do documento do MEI e a Res. 194, do calendário de opção. A consulta ao histórico da 140 e aos comunicados da Receita até o corte não identificou alteração material do C01. Revisar os atos ao chegar à competência. [Res. 140 e histórico](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278) · [Fontes e vigências](TAX_SOURCES.md)

## Jornada e implementação

[CÓDIGO] Abra a apuração tradicional na página inicial. Para o C01, selecione março de 2027, abertura em janeiro de 2023, revenda de caneta, loja e entrega em Florianópolis e todas as condições do perfil. Informe média de R$ 100.000 e aceite a estimativa do histórico. Informe R$ 100.000 de receita de março. A situação empresarial e os acumulados anuais podem ficar desconhecidos para uma estimativa condicional. O botão **Estimar com a média** mostra o resultado. Em **Informar ou refinar os 12 meses reais**, preencha a série e pressione **Calcular com histórico real**. Zero declara um mês sem vendas. Em branco, o mês permanece desconhecido.

| Componente | Responsabilidade executada |
|---|---|
| [Formulário](../web/traditional_form.py), [view](../web/traditional_view.py) e [template](../web/templates/web/traditional.html) | Validar identificadores, unicidade, mês, escala, formato, edição e valores no servidor. Reapresentar o POST com as entradas e o resultado em HTML. Aplicar CSRF, limite de 64 KiB, resposta privada sem cache e bloqueio de query string na rota. Sem cadastro, sessão financeira ou chamadas externas. |
| [Serviço](../simulation/traditional.py) e [histórico](../simulation/history.py) | Separar histórico, receita do PA, acumulado jan–mar/2027 e total de 2026. Conferir coerência dos totais fornecidos. A soma parcial conhecida permite detectar uma ultrapassagem mesmo sem o total anual. O acumulado desconhecido permanece ausente. Verificar perfil, competência, maturidade, opção e impedimentos. Registrar origem e faltantes. |
| [Catálogo](../parameters/catalog.py) e [edição ativa](../parameters/data/sn-03-02.json) | Edição por pedido, valores decimais em texto, limites inferior exclusivo e superior inclusivo, unidades, vigências, fontes, região e condição da revenda. Identificar cada valor pela edição, intervalo, número de faixa e nome do campo ou tributo. Conferir SHA-256 sobre UTF-8 com fim de linha LF, duplicidade, continuidade de vigência, fronteiras, unidades e soma dos pesos. Uma falha impede o total. |
| [Edição anterior](../parameters/data/sn-03-01.json) e [premissas](../parameters/assumptions.json) | A primeira edição contém a faixa 4. A segunda inclui nominal, dedução e fronteiras das faixas 3 e 5 para triagem. Os demais meses e faixas ficam bloqueados na web. O refinamento aceita somente a edição servida e ativa. Uma troca exige reabrir a página. O replay local aceita a revisão arquivada explícita. A repartição histórica de PIS/Cofins fica fora das duas edições. |
| [Núcleo decimal](../tax/traditional.py) | Janela móvel, escolha de faixa, limiares de excesso, base, alíquota efetiva, seis parcelas, resíduo e projeção. A multiplicação monetária antecede a divisão para preservar empates de centavo. Precisão de 34 dígitos nas divisões. |
| [Replay](../web/management/commands/replay_traditional.py) | A memória expandível permite selecionar e copiar o JSON. O comando local revalida os dados, restaura a revisão indicada e compara todos os campos salvo o horário da nova execução. O hash de software identifica os arquivos de cálculo, coordenação, seleção e normalização. |

[DECISÃO] Uma entrada anual é repartida em 12 valores de centavos. Os eventuais centavos indivisíveis entram nos primeiros meses em ordem cronológica, preservando o total informado para selecionar a faixa. Se o usuário também autorizar estimar março, usa-se a média arredondada ao centavo. A memória identifica a hipótese aplicada a cada base. A extrapolação anual multiplica por 12 o DAS mensal exibido sob as condições descritas no resultado.

## C01 e refinamento

[EXECUTADO] A entrada sintética acima retornou RBT12 de R$ 1.200.000,00. Com nominal de 10,70% e dedução de R$ 22.500,00, a efetiva foi de **8,825%**. Sobre março, o DAS bruto foi **R$ 8.825,00** e a extrapolação anual **R$ 105.900,00**. A referência independente da implementação é a memória da 00B e sua captura sintética. [Resultado copiável](evidencias/03/c01.json) · [Memória de referência](CALCULATION_REFERENCE.md) · [Captura anterior](evidencias/00b/reference.json)

| Tributo | Parte do DAS | Efetiva sobre a receita | Parcela analítica (R$) | Exibida (R$) |
|---|---:|---:|---:|---:|
| IRPJ | 5,50% | 0,485375% | 485,375 | 485,38 |
| CSLL | 3,50% | 0,308875% | 308,875 | 308,88 |
| CPP | 42,00% | 3,7065% | 3.706,50 | 3.706,50 |
| ICMS | 33,50% | 2,956375% | 2.956,375 | 2.956,38 |
| CBS | 15,33% | 1,3528725% | 1.352,8725 | 1.352,87 |
| IBS | 0,17% | 0,0150025% | 15,0025 | 15,00 |

[EXECUTADO] A soma exibida é R$ 8.825,01. O resíduo de +R$ 0,01 fica identificado e sem redistribuição. A guia consignada e o líquido após extinções ficam indeterminados. No C17, o IBS/CBS de 1.000 itens de R$ 100 da referência soma R$ 1.370,00 após arredondamento documental. As parcelas empresariais desses dois tributos somam R$ 1.367,875 antes de arredondar e já integram o DAS.

[EXECUTADO] No C12, substituir apenas fevereiro/2026 por R$ 80 mil levou o histórico real de março a R$ 1,18 milhão e o DAS a **R$ 8.793,22**. Na janela interna de abril, fevereiro/2027 com R$ 150 mil entrou e fevereiro/2026 saiu, produzindo R$ 1,25 milhão. A interface bloqueou competência fora de março. [Captura do refinamento no desktop](evidencias/03/historico-real-1366.png) · [Captura a 320 px](evidencias/03/historico-real-320.png)

## Campanha técnica de 20/11/2026

[EXECUTADO] Windows 10 build 19045, CPython 3.14.10, Django 5.2.19 e pytest 9.2.0. Os 54 testes específicos fazem parte da suíte padrão de 124. Os quatro testes marcados de integração foram selecionados à parte e executados com o conjunto regular da 02. Resultado final por ambiente:

| Ambiente | Padrão | Integração real 02 | Falhos / ignorados | Verificação adicional |
|---|---:|---:|---:|---|
| Windows nativo | 124 aprovados | 4 aprovados | 0 / 0 | 54 testes específicos, navegador e replay da captura |
| Container Linux/amd64 em Docker Desktop | 124 aprovados | 4 aprovados | 0 / 0 | 54 específicos na imagem web com rede desativada e sem JVM, além do replay da memória capturada no Windows |
| Linux nativo | Sem execução | Sem execução | — | A estação dispõe do ambiente Linux do Docker Desktop via WSL2 |

[EXECUTADO] A suíte da 03 cobre as seis parcelas e efetivas (C01), bloqueio de serviços, mistos e empresa nova (C08, C09, C11), excesso até e acima de 20%, ano de abertura e efeito anterior ao PA (C10), zero, ausência, consentimento e janela móvel (C12/C14), fronteiras da quarta faixa (C21), art. 45-A e granularidade documental (C17). No C13, pedidos concorrentes ao serviço usam duas revisões, com o mesmo C01 e catálogos de fronteira distintos. Há testes de vigências adjacentes, lacuna, sobreposição, repartição incorreta, unidade incompatível, duplicidade, arquivo ausente e replay adulterado. Os testes do formulário cobrem CSRF ativo, campos duplicados, mês indevido, formato, escala, query string, tipo e tamanho de corpo. [Suíte da Fase 03](../tests/test_traditional.py)

### Reproduzir no Windows

[DOCUMENTADO][EXECUTADO] Na raiz da árvore com os arquivos desta fase, use o ambiente do [README](../README.md). A porta 8004 permitiu manter o processo web anterior na 8002. Para repetir a campanha padrão:

```powershell
$phasePython = '.\.venv\Scripts\python.exe'
$env:DJANGO_SECRET_KEY = & $phasePython -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = '0'
& $phasePython manage.py check
& $phasePython -m pip check
& $phasePython -m pytest tests/test_traditional.py -q
& $phasePython -m pytest -q
& $phasePython manage.py replay_traditional docs/evidencias/03/c01.json
& $phasePython manage.py runserver 127.0.0.1:8004 --noreload --insecure
```

[EXECUTADO] `manage.py check` retornou zero problemas e `pip check` informou dependências compatíveis. O replay devolveu “Memória reproduzida integralmente com a revisão sn-03-02.” Para a integração, com o lançador qualificado do [README](../README.md#iniciar-o-motor-e-reproduzir-a-operação), `python -m pytest -q -m engine_integration` aprovou os quatro testes. As dependências da aplicação e as revisões de motor continuaram as da 02.

### Navegador e prova sem motores

[EXECUTADO] Com o Django nativo na 8004, a JVM qualificada parada, nenhum processo Java listado por `Get-Process java` e Docker Desktop parado, Chrome 157.0.8103.79 completou a jornada em 1366 × 900 e 320 × 720. Cada largura gerou quatro POSTs na calculadora. Histórico estimado e refinamento retornaram 200. Valor com três casas decimais após a vírgula retornou 400 com possibilidade de correção. Serviço ficou fora da cobertura, com explicação e sem total. O teste verificou navegação por teclado, foco após envio, abertura da memória e ausência de rolagem horizontal. O formulário funciona com JavaScript desativado. A prova foi repetida no Chrome do Windows com o Django em Compose na porta 8003. [Roteiro automatizado](../tests/browser/check_traditional.py) · [Formulário desktop](evidencias/03/formulario-1366.png) · [Formulário móvel](evidencias/03/formulario-320.png) · [Resultado desktop](evidencias/03/c01-1366.png) · [Resultado móvel](evidencias/03/c01-320.png)

[EXECUTADO] Em terminal separado, o ambiente de navegador reutiliza Playwright 1.65.2 e o canal local do Chrome. O argumento de saída destina-se aos dados sintéticos do roteiro:

```powershell
$browserPython = '.\scratch\phase01\browser\Scripts\python.exe'
& $browserPython tests/browser/check_traditional.py --origin http://127.0.0.1:8004 --output scratch/phase03/browser
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8004 --state offline --output scratch/phase03/pen-offline
# Com o motor regular restaurado
& $browserPython tests/browser/check_pen.py --origin http://127.0.0.1:8004 --state online --output scratch/phase03/pen-online
```

[EXECUTADO] A operação anterior da caneta retornou 503 com o motor parado e 200 com o motor restaurado, em ambas as larguras. Durante o desenvolvimento, uma asserção encontrou texto de perfil desconhecido pouco específico. A primeira campanha em Chrome também exigiu acomodar as partes focáveis do seletor nativo de mês e corrigir o destino do POST para devolver o foco ao resultado depois do refinamento. Os testes passaram após as correções. A tabela móvel passou a agrupar as três medidas por tributo para evitar a quebra de dígitos nos centavos.

### Containers e alcance da reprodução

[EXECUTADO] Docker Engine 28.5.1 Linux/amd64, Compose v2.40.2-desktop.1 e CPython 3.14.10 na imagem. O nome de projeto separado preservou os containers anteriores. O contexto do build inclui as novas fontes e os JSON. As montagens dos artefatos fiscais seguem a configuração da 02. Com a mesma chave efêmera no ambiente do terminal, o procedimento é:

```powershell
docker compose -p calculadora-fase03 up -d --build --wait --wait-timeout 120
docker exec calculadora-fase03-web-1 python manage.py check
docker exec calculadora-fase03-web-1 python -m pip check
docker exec calculadora-fase03-web-1 python -m pytest -q -p no:cacheprovider
docker exec calculadora-fase03-web-1 python -m pytest -q -m engine_integration -p no:cacheprovider
docker run --rm --network none -e DJANGO_SECRET_KEY calculadora-fase03-web python -m pytest tests/test_traditional.py -q -p no:cacheprovider
docker cp docs/evidencias/03/c01.json calculadora-fase03-web-1:/tmp/c01-phase03.json
docker exec calculadora-fase03-web-1 python manage.py replay_traditional /tmp/c01-phase03.json
docker compose -p calculadora-fase03 down
```

[EXECUTADO] O replay entre sistemas aceitou a mesma revisão e os mesmos valores. O `pip` do container avisou que o usuário de execução não tinha permissão de escrita no cache e concluiu a verificação sem dependências quebradas.

## Aceite e pendências

[DECISÃO] A Fase 03 atingiu os critérios técnicos para o recorte local. O navegador calcula, refina e expõe as cinco dimensões. As referências numéricas, o isolamento de edições, o replay e as funções da 02 passaram nos ambientes acima. A única evidência financeira adicionada ao projeto é sintética. O usuário pode copiar a própria memória por decisão sua.

[DOCUMENTADO] Permanecem pendentes a guia independente do PGDAS para a competência, a conciliação operacional dos centavos, os dados de extinções, a verificação da elegibilidade de empresa real e a revisão tributária profissional. A campanha de navegador verifica a jornada técnica. Observação de empresários e execução em Linux nativo continuam abertas. O próximo marco possível é a autorização específica da Fase 04, com as premissas e referências previstas no [roadmap](ROADMAP.md). A publicação exige revisão e autorização próprias.
