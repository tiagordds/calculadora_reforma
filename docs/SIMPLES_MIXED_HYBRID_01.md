# C09 · Comparação mensal das atividades mistas

## Abertura em 27/11/2026

[DECISÃO] O Prompt 13 autoriza o ensaio técnico interno de março de 2027 para a EPP madura de Florianópolis que revende canetas e desenvolve software sob encomenda. O objetivo é comparar obrigações empresariais ao mesmo preço e volume por atividade. A implantação pública e a homologação dependem de decisões próprias.

[EXECUTADO] Antes da implementação, `git status --short --branch` mostrou a árvore limpa em main. `git log -4 --oneline --decorate`, `git rev-parse HEAD main origin/main` e `git ls-remote origin refs/heads/main` apontaram a revisão `ee5210305e53977af7e8302dbbdbf14ce0a8b852`. `git remote -v` identificou o repositório tiagordds/calculadora_reforma no GitHub.

[DECISÃO] Primeiro conferir as regras e as edições fixadas do C01, C08 e C09. Depois reutilizar a apuração empresarial do C09 em cada trajetória, os cálculos regulares por atividade e as contas por tributo. Integrar formulário, memória e replay. Encerrar com referências aritméticas independentes, regressão, integrações e Chrome nos ambientes disponíveis.

[DECISÃO] Os riscos são copiar a faixa entre trajetórias, inferir exclusões de ICMS ou ISS, duplicar créditos compartilhados, perder informação parcial e alterar o replay histórico. O aceite exige as quatro combinações III/V, contas empresariais separadas, exemplos completos e parciais reproduzíveis, preservação das memórias anteriores e identificação do alcance de cada teste.

## Conferência normativa para março de 2027

[OFICIAL] A LC 123, arts. 13 e 18, e a LC 214, art. 41, vinculam a opção pelo regime regular de IBS e CBS à empresa. O art. 18 da LC 123 e os arts. 21, 22, 22-A, 25 e 26 da Res. 140 determinam o uso da faixa empresarial e a segregação das bases mensais. A redação da Res. 190 aplicável ao período desloca a janela da empresa madura para os doze meses antecedentes ao mês anterior ao PA. Para março, ambas as trajetórias usam fevereiro/2026 a janeiro/2027. A escrituração por competência e a conciliação da transição de caixa em dezembro de 2026 são condições de entrada. [LC 123](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) · [LC 214 atualizada pela LC 227](https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-normaatualizada-pl.html) · [Res. 140](https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278) · [Res. 190](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/152832) · [Perguntas e respostas do Simples](https://www8.receita.fazenda.gov.br/SimplesNacional/arquivos/manual/PerguntaoSN.pdf)

[OFICIAL][EXECUTADO] Conferência de 27/11/2026. A Res. 196, arts. 2º a 8º, qualifica as alterações da 190 e publica as tabelas de 2027–28. Na edição de 24/11 do DOU, seção 1, as páginas 39, 40 e 42 trazem I, III e V. A faixa 4 comercial retira pesos de CBS e IBS de 15,33% e 0,17%. Para o serviço, os pesos são 16,41% e 0,19% no III e 18,94% e 0,21% no V. Na faixa 5 do III, aplicar o teto de ISS e a redistribuição antes da remoção. A conferência dos textos locais e de `Get-FileHash scratch/services01/p38.pdf,scratch/services01/p39.pdf,scratch/services01/p40.pdf,scratch/services01/p42.pdf` recuperou os quatro hashes do C08. A consulta HTML direta ao DOU retornou 502. Os PDFs oficiais já preservados e a publicação do Ministério da Fazenda identificam a edição consultada. [Páginas oficiais e hashes completos](SIMPLES_SERVICES_HYBRID_01.md) · [Publicação da Fazenda](https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/novembro/comite-gestor-do-simples-nacional-publica-novas-regras-para-o-simples-nacional-e-para-a-transicao-da-reforma-tributaria)

[OFICIAL] O primeiro semestre da empresa madura usa a janela excepcional de 01/09 a 30/10/2026 e o cancelamento de 03/11 a 20/12/2026, conforme Res. 186 alterada pela 194. Um novo pedido em março/2027 produz efeitos em julho. A Res. 196 altera o calendário ordinário de cancelamento, já incorporado à edição 04-02. O art. 41, § 5º, da LC 214 trata do impedimento de saída por ressarcimento no ano corrente ou anterior. A comparação completa exige situação vigente declarada, referência temporal compatível e ausência declarada da vedação. A confirmação independente requer consulta ao Portal. [Calendário do CGIBS](https://cgibs.gov.br/embora-os-periodos-sejam-parecidos-tratam-de-escolhas-diferentes-por-isso-e-importante-entender-cada-situacao) · [LC 214 compilada](https://planalto.gov.br/ccivil_03/leis/lcp/lcp214compilado.htm)

[OFICIAL] A LC 214, arts. 11 e 12, determina o local e a composição das bases. Para a caneta vale a entrega local. Para o serviço deste contrato, conferir o domicílio aplicável do adquirente privado, além do estabelecimento prestador para ISS, conforme LC 116, arts. 3º e 4º e item 1.04. Excluir IBS e CBS próprios e identificar o ICMS ou o ISS incidente e as demais exclusões transitórias efetivamente contidas no preço. Os arts. 344 e 347 da LC 214 sustentam o IBS de 0,05% estadual e 0,05% municipal e a transição da CBS. Em 27/11, o AVS 1/2026 constava em tramitação. O catálogo conserva a taxa de CBS em aberto. [LC 116](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm) · [LC 214, texto atualizado](https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-normaatualizada-pl.html) · [Situação da matéria no Senado](https://www25.senado.leg.br/web/atividade/materias/-/materia/176221)

[OFICIAL][CÓDIGO] Os arts. 44–49 da LC 214 orientam apuração mensal, consolidação empresarial e apropriação por tributo. O documento, tratamento do fornecedor, destinação e competência em que os requisitos foram atendidos acompanham cada aquisição. A opção muda o tratamento das operações nas duas atividades. A segregação preserva o ISS do serviço e o ICMS comercial no DAS remanescente. A conferência do recorte não identificou diferença material nas edições `sn-retail-2027-01` (base `sn-03-02`), `sn-services-01` e `comparison-04-02`. A memória grava os quatro hashes. A nova revisão identifica a coordenação mista. [Catálogo comercial](../parameters/data/sn-retail-2027-01.json) · [Serviços](../parameters/data/sn-services-01.json) · [Opção e taxas](../parameters/data/comparison-04-02.json)

## Da entrada à obrigação mensal

[CÓDIGO] Na jornada tradicional, **Comparar usando estes dados** preserva as duas receitas, o perfil e os doze meses informados. Na comparação, o usuário preenche o histórico híbrido próprio ou confirma expressamente a igualdade das duas receitas e de todos os componentes da folha em cada mês. A origem de cada mês pode ser informada, estimada ou sintética. Cada série registra os campos em aberto. A soma mensal das receitas alimenta a RBT12 e, neste mercado interno, a RBT12r. A FS12 soma remuneração, pró-labore, CPP e FGTS empresariais elegíveis. O C09 compara a folha com 28% da RBT12r antes de arredondar e aplica os casos legais de denominador ou folha zero. A faixa do I e a faixa do III/V são determinadas em cada trajetória. [Apuração mista existente](../simulation/mixed.py) · [Coordenação comparativa](../simulation/mixed_comparison.py)

[CÓDIGO] Para preço final P, exclusões X e soma das taxas regulares t em fração, a revenda homogênea usa B = (P − X)/(1 + t), com ICMS e demais exclusões identificados separadamente. A receita fiscal H é P − t × B. No serviço, B = H − ISS − outras exclusões. O ISS pode vir das prestações ou, por escolha expressa, da hipótese ISS = s × H, com s da partilha híbrida após o teto. Quando H é informada, a coordenação confronta o preço com a receita e os débitos ao centavo. Se faltar CBS e a base estiver documentada, o IBS do serviço continua calculável. A memória registra a origem das exclusões, a taxa aceita, a receita fiscal, a base e os débitos de cada grupo. [Revenda](../tax/regular.py) · [Serviço](../tax/service_regular.py)

[CÓDIGO] Sobre H de cada atividade, o DAS remanescente soma as rubricas após retirar IBS e CBS. As contas empresariais recebem a soma dos débitos comerciais e de serviços do mesmo tributo, com um único lançamento por aquisição. O formulário admite adicionar documentos nas três destinações, exige referência local distinta e registra o crédito potencial, apurado e apropriado conforme o evento. O crédito compartilhado entra inteiro uma vez. A apropriação de março, os saldos anteriores, ajustes e estornos determinam o disponível. O uso é o menor entre disponível e débito do próprio tributo. O excedente fica na respectiva conta. A empresa pode declarar expressamente ausência de apropriações do mês. Sem declaração ou documentos suficientes, a obrigação dependente fica em aberto. Folha e percentuais de faturamento não alimentam as contas de crédito. [Contas e eventos](../tax/credits.py) · [Entrada e validação](../web/mixed_comparison.py)

[CÓDIGO] A obrigação híbrida soma o DAS remanescente analítico e os dois débitos líquidos de créditos, antes de outras extinções. A diferença é híbrido menos tradicional. Preço, volume, composição e condições comerciais são comuns por construção e exigem confirmação para comparar. A conta deve abranger os movimentos relevantes de cada tributo. Pedido intempestivo, cobertura incompleta ou ausência de confirmação eliminam a diferença global. Guia, pagamento, custo do crédito para o cliente, margem e caixa exigem conciliações próprias.

## Memórias de referência

[HIPÓTESE] No exemplo, a empresa abriu em janeiro/2023. Vende 6.000 canetas por R$ 60.000 e presta quatro serviços por R$ 40.000 em ambas as trajetórias. Os primeiros onze meses de cada histórico têm R$ 60 mil de comércio e R$ 40 mil de serviço. Em janeiro/2027, o híbrido informa R$ 50 mil e R$ 40 mil, e o tradicional mantém R$ 60 mil e R$ 40 mil. As séries da folha somam R$ 335.999,99 cada. A CBS de 10% é hipótese expressamente aceita, após a transição. As exclusões e o documento são sintéticos. A opção de 15/10/2026 é declarada vigente, sem ressarcimento ou outros movimentos de conta.

| Cálculo de março | Revenda | Software sob encomenda |
|---|---:|---:|
| Tradicional · faixa 4 sobre RBT12 de R$ 1,2 milhão | I · 8,825% × 60.000 = 5.295,00 | V · 19,075% × 40.000 = 7.630,00 |
| Exclusões na base regular | ICMS 4.950,00 + outras 0,00 | ISS das prestações 1.463,00 + outras 2,00 |
| Base de IBS/CBS | (60.000 − 4.950) / 1,101 = 50.000,00 | (40.000 − 1.465) / 1,101 = 35.000,00 |
| CBS regular | 5.000,00 | 3.500,00 |
| IBS estadual + municipal | 25,00 + 25,00 | 17,50 + 17,50 |
| Receita fiscal híbrida | 54.950,00 | 36.465,00 |
| Efetiva remanescente sobre RBT12 de R$ 1,19 milhão | (0,107 − 22.500/1.190.000) × 0,845 | (0,16 − 35.640/1.190.000) × 0,834 |
| DAS remanescente | 4.090,37 | 3.955,07 |

[EXECUTADO] O Fator R tradicional é 27,999999166…%, com serviço no V. A menor receita histórica híbrida eleva o fator a 28,235293277…%, com serviço no III. A receita fiscal híbrida de março soma R$ 91.415,00. O DAS remanescente empresarial de R$ 8.045,44 reparte-se em IRPJ R$ 455,93, CSLL R$ 335,40, CPP R$ 4.091,24, ICMS R$ 1.621,63 e ISS R$ 1.541,24. Neste caso os resíduos de exibição das rubricas são +R$ 0,01 na revenda e −R$ 0,01 no serviço. O resíduo consolidado é zero. A política usa Decimal de 34 dígitos e metade para cima. [Memória V/III](evidencias/mistas-hibrido01/fronteira-v-iii.json)

| Entrada modificada | Tradicional | Híbrido após créditos | Diferença ou componente preservado |
|---|---:|---:|---|
| [V/III, crédito zero](evidencias/mistas-hibrido01/fronteira-v-iii.json) | 12.925,00 | 16.630,44 | +3.705,44 |
| [Folha tradicional de R$ 336.000, III/III](evidencias/mistas-hibrido01/ambos-iii.json) | 10.507,00 | 16.630,44 | +6.123,44 |
| [Crédito de CBS desconhecido](evidencias/mistas-hibrido01/credito-cbs-pendente.json) | 12.925,00 | Em aberto | DAS 8.045,44, CBS bruta 8.500,00 e IBS líquido 85,00 |
| [ISS excluível desconhecido](evidencias/mistas-hibrido01/iss-pendente.json) | 12.925,00 | Em aberto | Comércio com DAS 4.090,37 e débitos regulares de 5.050,00 |
| [Preço comercial em aberto](evidencias/mistas-hibrido01/preco-comercial-pendente.json) | Em aberto | Em aberto | Serviço com DAS tradicional 7.630,00, remanescente 3.955,07 e débitos regulares de 3.535,00 |

[DOCUMENTADO] Para homologação, confrontar os dois grupos com PGDAS-D e contas assistidas de março/2027, verificar classificação do contrato de software, incidência e exclusões nos DF-e, apropriações por evento, opção efetiva e resíduos por tributo. A NFS-e tem correlação preliminar. O motor 1.6.1/V0059 tem canário documental de mercadoria. O ensaio do C09 é agregado. Uma publicação, outro período ou perfil e os regimes de lucro dependem de nova autorização.

## Reprodução local

[DOCUMENTADO] Com o ambiente Python e a chave efêmera do README, abra o Django e use **Estimar o DAS de atividades mistas → Comparar usando estes dados**. **Explorar exemplo com históricos diferentes** preenche as entradas sintéticas do primeiro caso. A seção **Memória de cálculo, premissas e fontes** contém o JSON completo. O replay valida o formulário e as referências dos documentos, resolve as edições fixadas, recalcula e exige igualdade integral com o registro. Na raiz do projeto, estes comandos reproduzem os cinco arquivos nos dois sistemas.

```text
python manage.py replay_mixed_comparison docs/evidencias/mistas-hibrido01/fronteira-v-iii.json
python manage.py replay_mixed_comparison docs/evidencias/mistas-hibrido01/ambos-iii.json
python manage.py replay_mixed_comparison docs/evidencias/mistas-hibrido01/credito-cbs-pendente.json
python manage.py replay_mixed_comparison docs/evidencias/mistas-hibrido01/iss-pendente.json
python manage.py replay_mixed_comparison docs/evidencias/mistas-hibrido01/preco-comercial-pendente.json
```

[CÓDIGO] A identidade `mixed-hybrid-01` inclui os hashes dos módulos de C09 tradicional e C08 híbrido e dos novos módulos de cálculo e de entrada. O SHA-256 normaliza as quebras de linha entre sistemas. Os comandos anteriores de replay e os snapshots de C01, C03, C08 e C09 tradicional continuam identificados por suas revisões de emissão. [Inicialização e execução do motor](../README.md) · [Comando do comparador misto](../web/management/commands/replay_mixed_comparison.py)

## Campanha interna de 27/11/2026

[EXECUTADO] CPython 3.14.10, Django 5.2.19 e dados sintéticos. As cinco exportações finais registram o SHA-256 de software `f7d2455b08aa4bd8d91a154a6006865aa2ab7731bdb11e4615a0b812ed1eeebe`. Todos os comandos de verificação da tabela retornaram 0.

| Verificação | Comando e entrada | Resultado |
|---|---|---|
| Software Windows | `python manage.py check`, `python -m pip check` e `python -m pytest -q` com a porta 18080 sem serviço | Zero problemas de sistema e dependências. 370 testes aprovados, dos quais 47 do novo comparador. Quatro integrações desmarcadas. |
| Software Linux | `docker compose -p c09-misto13 up --build -d --wait web` e, em container separado, `docker run --rm --network none -e DJANGO_SECRET_KEY c09-misto13-web python -m pytest -q -p no:cacheprovider` | 370 aprovados e quatro desmarcados sem acesso ao serviço fiscal. O replay das cinco memórias faz parte da suíte. |
| Motor real Windows | Lançador privado do README com Java 21 e V0059. `python -m pytest -q -m engine_integration --record-engine=scratch/mixed-hybrid01/replay` | Quatro aprovados. C03 com e sem tipo 55, resposta parcial C15 e exigência de certificado de cliente. O hash canônico do C03, removido apenas o instante, reproduziu `c5aca5f12b6191f8eb53d731d246be3137cd10cd22a071a9badee2257cfe7b66` da 05. |
| Motor real Linux | `docker compose -p c09-misto13 exec -T web python -m pytest -q -p no:cacheprovider -m engine_integration` | Quatro integrações aprovadas com a JVM na rede privada. |
| Interface sem JavaScript | Python do ambiente de navegador do projeto, `tests/browser/check_mixed_comparison.py http://127.0.0.1:8019 docs/evidencias/mistas-hibrido01`. Repetição com servidor Linux em `http://127.0.0.1:8003` e destino `scratch/mixed-hybrid01/compose` | Chrome 158.0.8127.37 no Windows, 320 e 1366 px em cada servidor. Transferência da apuração tradicional, edição de receita e folha, inclusão e correção de lacunas, foco pelo teclado e memória sem rolagem horizontal da página. Cinco JSON idênticos byte a byte entre servidores. |
| Replay histórico | `replay_traditional` no C01 da 05, `replay_services` nos dois C08 tradicionais, `replay_service_comparison` nos dois C08 híbridos, `replay_mixed` nos dois C09 tradicionais e `replay_comparison` nos três cenários de cada edição 04/05 | Treze memórias reproduzidas na árvore atual. O C01 da 03 e as três memórias da 04 também passaram nos checkouts de emissão em `scratch/services-hybrid/phase03` e `phase04`. |

[EXECUTADO] A sondagem inicial encontrou o Docker Desktop desligado. Após `docker desktop start`, o build, o teste sem rede, as integrações e a interface em Compose concluíram. A revisão do formulário identificou que a confirmação documental de uma aquisição com prefixo precisava de verificação do valor original do checkbox. A campanha final inclui a rejeição de texto inesperado nesse campo e de datas que impedem calcular o semestre. Os serviços de ensaio foram encerrados após os testes. [Testes de cálculo e contrato web](../tests/test_mixed_comparison.py) · [Percurso em Chrome](../tests/browser/check_mixed_comparison.py)

## Arquivos da entrega

| Área | Criados | Alterados |
|---|---|---|
| Cálculo, entrada e replay | `simulation/mixed_comparison.py`, `web/mixed_comparison.py`, `web/management/commands/replay_mixed_comparison.py` | `web/management/commands/replay_service_comparison.py` permite reutilizar a leitura limitada e a verificação integral do JSON |
| Jornada Django | `web/templates/web/mixed_comparison.html`, `web/templates/web/mixed_company.html` | `config/urls.py`, `web/middleware.py`, `web/templates/web/mixed.html` |
| Testes e evidências | `tests/test_mixed_comparison.py`, `tests/browser/check_mixed_comparison.py`, cinco JSON em `docs/evidencias/mistas-hibrido01/` | `.dockerignore` inclui as novas memórias na imagem de ensaio |
| Documentação | Este relatório | `README.md` e, em `docs/`, `PRODUCT_SPEC.md`, `ROADMAP.md`, `DECISIONS.md`, `TAX_PARAMETERS.md`, `TEST_SCENARIOS.md` e `KNOWN_LIMITATIONS.md` |

[EXECUTADO] Ao encerramento, `git rev-parse HEAD main origin/main` e `git ls-remote origin refs/heads/main` retornaram a revisão de abertura. `git status --porcelain=v1 -uall` listou 12 arquivos rastreados alterados e 13 novos, todos na árvore de trabalho. A conferência com `git diff --exit-code ee52103` dos adaptadores, parâmetros, regras e memórias históricas selecionadas retornou 0. O estado entregue é local, anterior ao commit.
