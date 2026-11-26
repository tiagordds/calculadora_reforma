# Primeiro serviço do Simples tradicional · C08

## Abertura em 24/11/2026

[DECISÃO] O Prompt 10 autorizou a expansão local para desenvolvimento sob encomenda em Florianópolis, PA março/2027, empresa madura, receita exclusiva e opção tradicional. O objetivo é apurar o Fator R e estimar o DAS bruto com sua repartição. Dependências: regras com efeitos no PA, memória da 00B, módulo decimal, histórico deslocado e proteção dos formulários da Fase 05.

[EXECUTADO] Antes das edições, `git status --short --branch` retornou apenas `## main...origin/main`. O histórico começou em `9b8b9cf` (05), `c9a330a` (04) e `c515471` (03). `git ls-remote origin refs/heads/main` confirmou a ponta `9b8b9cfb7466795236154aa17f7a7f46f0dcfc66`.

[DECISÃO] Plano: conferir legislação e correlação documental, fixar parâmetros por revisão, implementar cálculo e memória, ligar o formulário à página inicial, confrontar fronteiras e reexecutar as regressões e memórias da 05. Riscos: deslocar um mês, confundir folha paga com provisionada, arredondar o fator antes do corte, aplicar partilha histórica ou atribuir ISS sem conhecer retenção e sublimite. Aceite técnico: fronteira de um centavo reproduzida, lacunas identificadas, repartição rastreável, correção no mesmo formulário e evidências separadas de software, compatibilidade e homologação. A publicação e a Fase 06 dependem de outra autorização.

## Uso e cobertura

[CÓDIGO] Na página inicial, abra **Calcular o Fator R e o DAS de serviços**. O botão **Preencher com o exemplo de 28%** carrega os valores sintéticos para edição. Também é possível iniciar com os campos vazios. O formulário mantém os valores após o cálculo ou erro, aceita centavos, rejeita campos extras ou repetidos e aplica as proteções de POST, CSRF e cache das jornadas financeiras. Os dados ficam no pedido e na página do navegador. [Formulário e entrada Django](../web/services.py) · [Interface](../web/templates/web/services.html)

[DECISÃO] A estimativa exige opção tradicional vigente, receita doméstica exclusiva da atividade, serviço no estabelecimento em Florianópolis, cliente privado, receita por competência, ISS devido no município sem retenção, benefício ou valor fixo. O usuário declara o atendimento aos limites anuais, inclusive os proporcionais. A soma de receitas **já conhecidas** de cada ano pode contradizer essa declaração. A RBT12 não substitui a receita do ano civil. Nas faixas 1 a 5, o DAS só aparece após confirmação das condições. Acima de R$ 3,6 milhões de RBT12, preservam-se fator e faixa identificável. A sexta faixa requer tratamento adicional de ISS, IBS e sublimite. Permanecem fora da apuração o híbrido, início de atividade, receitas mistas, outros serviços, Anexo IV e regimes de lucro.

## Regra e vigência conferidas em 24/11/2026

| Fundamento | Aplicação em março de 2027 e limite da evidência |
|---|---|
| [OFICIAL] LC 123, art. 18, §§ 5º-D, IV, 5º-M e 24–26 | Elaboração do programa no estabelecimento do optante e natureza da receita justificam o teste III/V. [LC 123 consolidada](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) |
| [OFICIAL] Res. 140, arts. 21, 22, 25, 26 e 45-A, com redações aplicáveis das Res. 190 e 196 | Para a empresa no 14º mês ou posterior, somar fevereiro/2026 a janeiro/2027. A janela antecede o mês anterior ao PA. Somar receita de todos os estabelecimentos e folha elegível. No fator, a receita legal abrange também exportações, ausentes por premissa deste caso. [Res. 140](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/92278) · [Res. 190](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/152832) |
| [OFICIAL] LC 214, anexos XX e XXII, com as alterações da LC 227, e Res. 196, arts. 2º, 3º, 5º, 6º e 8º | O art. 6º da Res. 196 revoga a substituição de tabelas prevista no art. 6º da Res. 190. Foram lidos diretamente os novos quadros de 2027–28 no DOU. Na faixa 4 do III, a CBS representa **16,41%** do DAS. Os quadros fixam nominal, dedução e partilha de cada anexo. A LC 238 trata do MEI. [LC 214 compilada com redações](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm) · [DOU de 24/11, Anexo III, p. 40](https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=515&pagina=40&data=24/11/2026&captchafield=firstAccess) · [Anexo V, p. 42](https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=515&pagina=42&data=24/11/2026&captchafield=firstAccess) |
| [OFICIAL] LC 116, arts. 3º, 4º e 6º, lista 1.04 | O caso considera o estabelecimento prestador e o ISS ordinário no DAS. Retenção depende também do tomador e das regras municipais. A migração de Florianópolis para a NFS-e nacional preserva a necessidade de conferir as obrigações locais. [LC 116](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm) · [Orientação municipal](https://devportal.pmf.sc.gov.br/entidades/fazenda/index.php?noti=27349&pagina=notpagina) |
| [OFICIAL][EXECUTADO] NFS-e, Anexo VIII v1.02.00 de 26/10/2026 | Na aba “tabela geral”, a linha 27 inicia 01.04 com atividade 9, a linha 28 inclui a NBS 1.1502.20.00 para programa personalizado. `Get-FileHash scratch/00b/nbs.xlsx` reproduziu `12CC80BC92687856B47E961B98CDBAA3F8CAE568C099B3EF71994E73482AC7D0`. O portal, atualizado em 23/11, descreve a correlação como preliminar, sem regra de negócio baseada nela. Contrato e documento decidem a classificação da operação. A correção V0068 e a divergência de V0059 ficaram registradas na 00B. [Portal e notas 009/010](https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc) · [Evidência da 00B](evidencias/00b/FONTES_TECNICAS.md) |

[OFICIAL] FS12 agrega remunerações elegíveis pagas a pessoas físicas e declaradas, pró-labore pago, CPP e FGTS efetivamente recolhidos. O 13º entra na competência de incidência da contribuição. Excluir aluguéis e distribuição de lucros e evitar dupla contagem do pró-labore. Com ambas as bases positivas, comparar FS12 com 0,28 × RBT12r antes de apresentar a divisão decimal. Folha zero dá fator 0,01, mesmo com receita histórica zero. Folha positiva e RBT12r zero dão 0,28. Apenas para a alíquota efetiva, a RBT12 zero adota base de R$ 1,00. O manual histórico do PGDAS-D descreve o truncamento da razão a duas casas, compatível com o mesmo limiar. A memória preserva a razão analítica. [Res. 140, arts. 21 e 26](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/92278) · [Manual PGDAS-D 2018](https://www8.receita.fazenda.gov.br/SimplesNacional/Arquivos/manual/MANUAL_PGDAS-D_2018_V4.pdf)

[CÓDIGO] A edição `sn-services-01` fixa limites de faixa, nominal e dedução, parcelas em percentual do total, corte do fator, exceções de zero e teto de ISS. Na quinta faixa do III, quando a parcela proporcional de ISS ultrapassa 5% da receita, a diferença segue os pesos do quadro específico. A memória mostra bases, entradas mensais, componentes em aberto, fórmula aplicada, valores antes e depois do arredondamento e hashes de software e parâmetros. Zero informado participa da soma. A ausência de qualquer mês mantém aberto o respectivo total. [Catálogo](../parameters/data/sn-services-01.json) · [Cálculo](../tax/services.py) · [Coordenação](../simulation/services.py)

## C08 e referência aritmética

[HIPÓTESE] Para demonstrar o DAS nos dois lados, fixou-se receita de março em **R$ 100.000,00**. Na comparação, a empresa permanece no mesmo perfil e na faixa 4. São doze receitas de R$ 100 mil. Cada mês tem R$ 20 mil de remunerações, R$ 5 mil de pró-labore, R$ 2 mil de CPP e R$ 1 mil de FGTS. A variação de um centavo incide sobre a remuneração de janeiro/2027.

| FS12 | Fator R analítico | Anexo | Conta independente da alíquota efetiva | DAS bruto |
|---:|---:|---|---|---:|
| R$ 335.999,99 | 27,9999991666…% | V | (R$ 246.000 − R$ 17.100) / R$ 1.200.000 = 19,075% | R$ 19.075,00 |
| R$ 336.000,00 | 28% | III | (R$ 192.000 − R$ 35.640) / R$ 1.200.000 = 13,03% | R$ 13.030,00 |
| R$ 336.000,01 | 28,0000008333…% | III | Mesma faixa e base da igualdade | R$ 13.030,00 |

| Tributo | Peso no V | V, em reais | Peso no III | III, em reais |
|---|---:|---:|---:|---:|
| IRPJ | 21% | 4.005,75 | 4% | 521,20 |
| CSLL | 15% | 2.861,25 | 3,5% | 456,05 |
| CBS | 18,94% | 3.612,81 | 16,41% | 2.138,22 |
| CPP | 23,85% | 4.549,39 | 43,4% | 5.655,02 |
| ISS | 21% | 4.005,75 | 32,5% | 4.234,75 |
| IBS | 0,21% | 40,06 | 0,19% | 24,76 |

[DOCUMENTADO][EXECUTADO] Os valores esperados vêm da multiplicação do DAS bruto pelos pesos do DOU. Por exemplo, R$ 19.075 × 18,94% = R$ 3.612,805 de CBS, exibidos como R$ 3.612,81. No V, a soma das parcelas exibidas supera o bruto em R$ 0,01. No III, coincide. A diferença mensal **entre os cenários** é R$ 6.045,00. O confronto usou referências fixas independentes da implementação. As memórias extraídas do navegador permitem repetir o cálculo. [Teste C08](../tests/test_services.py) · [Memória Anexo V](evidencias/servicos01/c08-v.json) · [Memória Anexo III](evidencias/servicos01/c08-iii.json)

## Execução e limites

[EXECUTADO] Campanha de 24/11/2026, com chave Django temporária no ambiente e dados sintéticos. Nos comandos abaixo, `python` representa o interpretador do ambiente indicado no README. As únicas dependências adicionais do ensaio de interface estão no ambiente local de navegador da Fase 01.

| Verificação | Comando e entrada | Retorno |
|---|---|---|
| Software no Windows | `python manage.py check` e `python -m pytest -q`, suíte padrão | Zero problemas, 224 testes aprovados, quatro integrações reais desmarcadas. A primeira execução acusou um erro no caso de teste de excesso anual: o valor somava exatamente R$ 3,6 milhões. A entrada de excesso passou a ultrapassar o limite por um centavo. |
| Compatibilidade Linux | `docker build --target web -t calculadora-servicos01-local .` e `docker run --rm --network none -e DJANGO_SECRET_KEY calculadora-servicos01-local python -m pytest -q -p no:cacheprovider` | Imagem web local, 224 aprovados, quatro desmarcados, sem rede e sem JVM. |
| Interface em Chrome/Windows | `python tests/browser/check_services.py http://127.0.0.1:8017 docs/evidencias/servicos01` com servidor Django local | Saída 0. Em 320 e 1366 px, sem JavaScript, abriu a jornada pela home, preencheu o exemplo, corrigiu R$ 0,01, abriu a memória e retirou uma remuneração para obter resultado parcial. Conferiu foco, ausência de rolagem horizontal e preservação dos dados. |
| Replay C08 | `python manage.py replay_services docs/evidencias/servicos01/c08-iii.json` e repetição com `c08-v.json` | Memórias integrais da igualdade e de um centavo abaixo. Para repetir outra simulação, copie o JSON da memória para um arquivo local e passe esse arquivo ao comando. |
| Regressão da revenda | `python manage.py replay_traditional docs/evidencias/05/c01.json` e `python manage.py replay_comparison docs/evidencias/05/middle.json`, repetido para `zero.json` e `high.json` | Quatro memórias reproduzidas integralmente nas edições da 05. |
| C03 com motor real no Windows | Lançador fixado no README, depois `python -m pytest -q -m engine_integration --record-engine scratch/services01/replay` | Quatro testes reais aprovados. O JSON de C03 reproduziu o digest canônico da 05, `c5aca5f12b6191f8eb53d731d246be3137cd10cd22a071a9badee2257cfe7b66`. |

[DECISÃO] Aceite técnico para o C08 sintético. Para uso fiscal real, faltam PGDAS-D de março/2027 no mesmo cenário, conferência dos encargos pagos e da elegibilidade, documentação contratual, eventual retenção, segregação, conciliação de centavos e parecer profissional. Observar usuários e testar em host Linux independente seguem pendentes. Encerramento local antes da Fase 06.

[EXECUTADO] Uma conferência adicional com `python -` extraiu os seis pesos de cada faixa 1–5 das páginas 40 e 42 do DOU e comparou-os ao JSON da edição. Em seguida, usando `fractions.Fraction` sem importar o núcleo do projeto, confrontou os dois DAS e as doze parcelas antes do arredondamento. Retorno 0 para dez partilhas, dois totais e doze valores. O endereço do DOU em HTML retornou HTTP 403 durante a coleta. As páginas oficiais em PDF acima permitiram ler as tabelas. A primeira leitura automatizada perdeu o caractere ordinal no terminal Windows. A repetição com o ordinal Unicode preservado confirmou os valores.

## Arquivos e estado de entrega

| Área | Criados | Modificados |
|---|---|---|
| Cálculo e parâmetros | `parameters/data/sn-services-01.json`, `parameters/services.py`, `tax/services.py`, `simulation/services.py` | — |
| Jornada e reprodução | `web/services.py`, `web/templates/web/services.html`, `web/management/commands/replay_services.py` | `config/urls.py`, `web/middleware.py`, `web/templates/web/home.html` |
| Testes e capturas | `tests/test_services.py`, `tests/browser/check_services.py`, `docs/evidencias/servicos01/c08-iii.json`, `docs/evidencias/servicos01/c08-v.json` | — |
| Produto, regras e evidências | `docs/SIMPLES_SERVICES_01.md` | `README.md`, `CHANGELOG.md`, `docs/PRODUCT_SPEC.md`, `docs/ROADMAP.md`, `docs/DECISIONS.md`, `docs/CALCULATION_REFERENCE.md`, `docs/TAX_RULES.md`, `docs/TAX_SOURCES.md`, `docs/TAX_PARAMETERS.md`, `docs/TEST_SCENARIOS.md`, `docs/KNOWN_LIMITATIONS.md` |

[EXECUTADO] Ao encerrar, `git rev-parse HEAD origin/main` e `git ls-remote origin refs/heads/main` coincidiram em `9b8b9cf`. Árvore com 14 arquivos rastreados modificados e 12 novos, índice vazio de alterações. A checagem de links locais e `git diff --check` passaram.
