# Atividades mistas no Simples tradicional · C09

## Abertura em 27/11/2026

[DECISÃO] O Prompt 12 autoriza a apuração interna de março/2027 para uma EPP madura de Florianópolis que revende canetas e desenvolve software sob encomenda no mesmo CNPJ. A entrega começa pelo histórico empresarial, segue pelas duas parcelas do DAS e termina no formulário Django, nos replays e na regressão. Depende das funções decimais do C01/C08, da janela histórica de 2027 e das tabelas oficiais. O Anexo I precisa de complemento de partilha para permitir refinamentos fora da quarta faixa.

[EXECUTADO] Antes das alterações, `git status --short --branch` retornou apenas `## main...origin/main`. A ponta local era `98fe96beb90c8817415c03c7bc27925139411fa1`, precedida por `c11a34e` e `9b8b9cf`.

[DECISÃO] Os riscos centrais são dividir a receita histórica ou a folha por atividade, tratar ausência como zero, ignorar excesso detectável em dados parciais e somar tributos já arredondados. O aceite técnico exige que a fronteira de um centavo só altere o serviço, que dados faltantes identifiquem precisamente a parcela em aberto, que ambas as memórias se reproduzam e que a regressão preserve os casos anteriores. A homologação exige demonstrativo do PGDAS-D do período e revisão profissional.

## Qualificação anterior à implementação

[OFICIAL] A LC 123, art. 18, §§ 1º a 4º, 5º-D, IV, 5º-M e 24–26, e a Res. CGSN 140, arts. 21, 22, 25 e 26, vinculam a faixa à receita empresarial e a incidência mensal à receita segregada. No mercado interno deste caso, RBT12 e RBT12r coincidem. Para empresa no 14º mês ou posterior, a redação da Res. 190 aplicável em 2027 desloca ambas as séries para fevereiro/2026 a janeiro/2027. Somar folha elegível paga e encargos efetivamente recolhidos da empresa. Aplicar o corte apenas ao serviço. [LC 123 consolidada](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm) · [Res. 140](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/92278) · [Res. 190](https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/152832) · [Perguntas e respostas oficiais](https://www8.receita.fazenda.gov.br/SimplesNacional/arquivos/manual/PerguntaoSN.pdf)

[OFICIAL] Para o PA, a LC 214/2025, anexos XVIII, XX e XXII, com as alterações da LC 227/2026, e a Res. 196/2026, art. 3º, trazem os quadros de 2027–28. Conferência em 27/11/2026 da edição de 24/11, seção 1, pp. 39, 40 e 42 (I, III e V). Os PDFs oficiais preservados em `scratch/services01/p{39,40,42}.pdf` têm SHA-256, respectivamente, `e12fb4bc15c7d9a6e530fcd278a64068857327110ab7e3682bd7386192828882`, `1dc26404ba81688659c8727d9cee936ad1c19ba2c06dc8f98b2bfdebac726c4b` e `b7988f231ad02ea4acbb1b09e91972c7540e5d9b61fa48ff444ddf6a3bd39878`. A faixa 4 comercial coincide com a edição do C01. O art. 45-A orienta os centavos. A ordem final da conciliação precisa do demonstrativo da competência. [LC 214](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm) · [Res. 196 no DOU](https://www.in.gov.br/web/dou/-/resolucao-cgsn-n-196-de-16-de-novembro-de-2026-745832719)

## Jornada e limites

[CÓDIGO] Na página inicial, abra **Estimar o DAS de atividades mistas**. Em **Preencher exemplo de comércio e serviços**, a folha está exatamente no limiar. Reduza a remuneração de janeiro/2027 em R$ 0,01 para reproduzir o outro cenário. É possível iniciar com campos vazios. O POST valida no servidor, mantém entradas após correção e identifica dados repetidos. O cálculo é local, sem persistência nem chamada a motor documental. [Formulário](../web/mixed.py) · [Tela de apuração](../web/templates/web/mixed.html)

[HIPÓTESE] O exemplo usa abertura em janeiro/2023, opção tradicional vigente, mercado interno, clientes privados e receitas fiscais por competência, com transição de caixa já conciliada. O comércio corresponde à caneta comum nacional adquirida de terceiros e revendida com entrega local por NF-e 55. O software é desenvolvido sob encomenda no estabelecimento, com ISS ordinário devido em Florianópolis. A empresa declara atendimento aos limites anuais. Continuam fora do recorte outros serviços e revendas, Anexo IV, início de atividade, retenções, benefícios, substituição, monofasia, excessos, sexta faixa, regimes de lucro, híbrido misto e integração documental.

[CÓDIGO] Cada um dos doze registros guarda comércio, serviços, folha por componente, origem do mês, campos faltantes e total empresarial derivado. O usuário distingue informado, estimado e sintético. Mês incompleto deixa RBT12 aberta. Ausência de folha mantém a parcela comercial quando a receita histórica e as demais condições são conhecidas. Uma atividade com receita de março ausente ou condição especial deixa em aberto sua parcela e o total. A receita conhecida também pode provar excesso do limite anual, mesmo quando a outra atividade está em aberto. A declaração dos limites cobre os meses do ano civil ausentes da janela. [Coordenação](../simulation/mixed.py)

[CÓDIGO] A edição derivada `sn-retail-2027-01` acrescenta os dados faltantes do Anexo I a `sn-03-02`. A partilha das faixas 3 e 5 coincide com a da faixa 4. Nas duas primeiras, CPP e ICMS têm pesos próprios. Para os serviços, `sn-services-01` fornece as faixas, a partilha e o teto de ISS, inclusive a redistribuição na quinta faixa do III. As funções existentes calculam o fator e a incidência por atividade. A memória contém os SHA-256 das três edições, a identidade do software e os valores analíticos. [Complemento comercial](../parameters/data/sn-retail-2027-01.json) · [Resolução da edição](../parameters/retail.py) · [Cálculo comercial](../tax/traditional.py) · [Cálculo de serviços](../tax/services.py)

## Duas memórias independentes de referência

[HIPÓTESE][DOCUMENTADO] Em cada mês de fevereiro/2026 a janeiro/2027, a receita soma R$ 60.000 de comércio e R$ 40.000 de serviços. Assim, RBT12 = 12 × R$ 100.000 = R$ 1.200.000. Março/2027 repete a proporção e fica fora dessa janela. A folha mensal da igualdade contém R$ 20.000 de remuneração, R$ 5.000 de pró-labore, R$ 2.000 de CPP e R$ 1.000 de FGTS. A FS12 soma R$ 336.000. Abaixo do limiar, a remuneração do último mês é R$ 19.999,99. O fator usa toda a folha e toda a receita empresarial.

| Conta manual da faixa 4 | FS12 de R$ 335.999,99 · I e V | FS12 de R$ 336.000,00 · I e III |
|---|---:|---:|
| Fator R, antes do corte | 335.999,99 / 1.200.000 = 27,9999991666…% | 336.000 / 1.200.000 = 28% |
| Efetiva comercial | (1.200.000 × 10,70% − 22.500) / 1.200.000 = 8,825% | 8,825% |
| DAS sobre R$ 60.000 de revenda | R$ 5.295,00 | R$ 5.295,00 |
| Efetiva do serviço | (1.200.000 × 20,50% − 17.100) / 1.200.000 = 19,075% | (1.200.000 × 16% − 35.640) / 1.200.000 = 13,03% |
| DAS sobre R$ 40.000 de serviços | R$ 7.630,00 | R$ 5.212,00 |
| **DAS bruto consolidado** | **R$ 12.925,00** | **R$ 10.507,00** |

[DOCUMENTADO] A mudança de enquadramento reduz apenas a parcela do serviço em R$ 40.000 × (19,075% − 13,03%) = **R$ 2.418,00**. As referências abaixo multiplicam cada DAS pelos pesos transcritos dos quadros oficiais. A coluna consolidada soma os valores de cada tributo antes de arredondar. Por exemplo, a CBS no I+V soma R$ 811,7235 da revenda e R$ 1.445,122 do serviço, exibindo R$ 2.256,85. ISS incide no serviço e ICMS na revenda.

| Tributo | Peso no I | Peso no V | Peso no III | I + V, em reais | I + III, em reais |
|---|---:|---:|---:|---:|---:|
| IRPJ | 5,50% | 21% | 4% | 1.893,53 | 499,71 |
| CSLL | 3,50% | 15% | 3,5% | 1.329,83 | 367,75 |
| CBS | 15,33% | 18,94% | 16,41% | 2.256,85 | 1.667,01 |
| CPP | 42% | 23,85% | 43,4% | 4.043,66 | 4.485,91 |
| ICMS | 33,50% | — | — | 1.773,83 | 1.773,83 |
| ISS | — | 21% | 32,5% | 1.602,30 | 1.693,90 |
| IBS | 0,17% | 0,21% | 0,19% | 25,02 | 18,90 |
| Soma das rubricas exibidas | | | | 12.925,02 | 10.507,01 |
| Soma exibida menos DAS bruto | | | | +0,02 | +0,01 |

[CÓDIGO][EXECUTADO] A política decimal usa 34 dígitos para divisões, arredondamento de metade para cima e mínimo de R$ 0,01 para valor positivo demonstrado. A estimativa guarda separadamente o resíduo das rubricas de cada atividade, o das rubricas consolidadas e o da soma dos dois DAS exibidos. Nos dois exemplos, as duas parcelas exibidas somam o DAS bruto exatamente. Os testes usam valores esperados independentes do simulador. [Referências executáveis](../tests/test_mixed.py) · [Memória exportada I + V](evidencias/mistas01/c09-v.json) · [Memória exportada I + III](evidencias/mistas01/c09-iii.json)

## Verificações de 27/11/2026

[EXECUTADO] Campanha local com entradas sintéticas, CPython 3.14.10, Django 5.2.19 e chave efêmera conforme o README. O código da memória C09 teve SHA-256 `c74c536ddbd24f0e1bdc4dbdfb9c5fbc7b601011b2533a029c3ea0c39442a1c9`, com quebras de linha normalizadas. A imagem Linux e a JVM privada foram executadas pelo Docker Desktop 28.5.1 na mesma estação Windows.

| Verificação | Comando e entrada | Resultado |
|---|---|---|
| Aplicação e software no Windows | `python manage.py check`, `python -m pip check`, `python -m pytest -q` | Zero problemas de sistema ou dependências. 323 aprovados, incluindo 50 novos, quatro integrações desmarcadas. |
| Software Linux sem rede | `docker compose -p c09-ensaio build web regular` e `docker run --rm --network none -e DJANGO_SECRET_KEY c09-ensaio-web python -m pytest -q -p no:cacheprovider` | 323 aprovados, quatro desmarcados. Os replays arquivados do C09 foram exercitados dentro da imagem. |
| Motor Windows | Lançador privado do README e `python -m pytest tests -q -m engine_integration --record-engine=scratch/mixed01/replay` | Quatro aprovados. C03 com e sem tipo 55, C15 parcial e mTLS. O JSON canônico de C03, retirado apenas o instante, reproduziu o hash da 05, `c5aca5f12b6191f8eb53d731d246be3137cd10cd22a071a9badee2257cfe7b66`. |
| Motor Linux | `docker compose -p c09-ensaio up -d --wait web` e `docker compose -p c09-ensaio exec -T web python -m pytest tests -q -p no:cacheprovider -m engine_integration` | Quatro aprovados com a JVM e V0059 na rede fiscal privada. |
| Interface | No ambiente de navegador do projeto, `python tests/browser/check_mixed.py http://127.0.0.1:8019 docs/evidencias/mistas01` no Django Windows. Repetição em `http://127.0.0.1:8003` com Django Linux/Compose e saída em `scratch/mixed01/compose` | Chrome/Windows, 320 e 1366 px, JavaScript desligado. Retorno 0 nos dois servidores. Entrada pela home, teclado, foco do resultado, preservação do formulário, duas fronteiras, memória sem rolagem horizontal e folha incompleta com DAS comercial visível. As duas exportações de cada servidor coincidiram byte a byte. |
| Replay do C09 | `python manage.py replay_mixed docs/evidencias/mistas01/c09-v.json` e repetição com `c09-iii.json` | Retorno 0, igualdade integral. A suíte também reproduziu memória parcial e rejeitou adulteração do hash da edição. |
| Regressão das memórias da empresa | `python manage.py replay_traditional docs/evidencias/05/c01.json`; `replay_services` nos dois JSON de `servicos01`; `replay_service_comparison` nos dois de `servicos-hibrido01`; `replay_comparison` em zero, middle e high das fases 04 e 05 | Todos com retorno 0. Também foram executados `replay_traditional` com C01 da 03 e `replay_comparison` com os três casos da 04 nos respectivos checkouts de emissão preservados em `scratch/services-hybrid`. |

[EXECUTADO] Na sondagem inicial, o daemon Docker estava desligado. Após `docker desktop start`, o build, os testes e os replays concluíram. O projeto de ensaio foi encerrado por `docker compose -p c09-ensaio down --volumes`. A comparação de Git com a revisão inicial preservou as evidências, os parâmetros e os cálculos fiscais anteriores. Os testes de software e de compatibilidade passaram nos dois ambientes. A interface teve ensaio automatizado em Chrome com os dois servidores.

## Pendências de utilização

[DOCUMENTADO] Para homologação, obter o demonstrativo do PGDAS-D de março/2027 com as duas segregações da mesma empresa, confrontar faixa, folha, partilha e ordem dos arredondamentos e registrar o parecer de um profissional. Em dados reais, conferir opção, limites dos anos completos, documentos da revenda e do contrato de software, receitas e encargos efetivamente recolhidos. Observação de gestores reais, publicação e eventual fase híbrida mista dependem de definição e autorização próprias.
