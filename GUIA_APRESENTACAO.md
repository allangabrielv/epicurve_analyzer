# Guia de Apresentação — EpiCurve Analyzer

> **Para quem vai apresentar sem ser especialista.** Este arquivo explica tudo
> do zero: o problema, os dados, a limpeza, a ideia, os algoritmos, as
> conclusões e — principalmente — **as perguntas que o professor pode fazer com
> respostas prontas**. Leia uma vez com calma antes de apresentar. O que estiver
> em **negrito** vale a pena decorar.

---

## 0. Resumo em 30 segundos (decore isto)

> "Peguei os dados oficiais de COVID-19 de São Paulo — **3,85 milhões de
> registros** do DataSUS. Transformei a série de casos diários numa **tabela
> comum** (para prever hoje, uso os dias anteriores como pistas) e usei o
> **LazyPredict**, uma ferramenta que **treina dezenas de modelos de uma vez e
> mostra um ranking** de qual erra menos. Em uma linha de código ele testou **39
> modelos**; o melhor foi o **BaggingRegressor**, que ficou lado a lado com os
> modelos clássicos de séries temporais feitos à mão — **sem eu precisar deduzir
> nenhuma fórmula**."

Se você só decorar esse parágrafo, já sustenta a apresentação.

---

## 1. Qual é o problema (e por que importa)

**A pergunta:** *quantos casos de COVID vamos ter nas próximas semanas?*

Por que isso vale ouro:
- Define **quantos leitos de UTI, cilindros de oxigênio e equipes** o hospital
  precisa preparar.
- Ajuda o governo a decidir **quando apertar ou afrouxar** as restrições.
- **Prever cedo = se preparar. Errar = ou hospital lotado, ou dinheiro público
  jogado fora.**

É um problema de **previsão de série temporal**: temos o histórico dia a dia e
queremos "adivinhar" o futuro próximo.

---

## 2. Os dados

### 2.1 De onde vêm
- **Fonte oficial:** DataSUS (Ministério da Saúde), distribuído de forma
  organizada pelo projeto **Brasil.IO**.
- **Arquivo:** `caso_full.csv.gz` — casos e óbitos de COVID por dia, para **todos
  os municípios e estados do Brasil**.
- **Período:** **25/02/2020 a 27/03/2022** (início da pandemia até o fim da onda
  Ômicron).

### 2.2 Escala — o contexto "big data"
- **3.853.648 registros** (linhas) no arquivo bruto.
- 18 colunas no total; **5.570 municípios**.
- 92 MB **compactado** (`.gz`) — descompactado é muito maior.
- **Truque de eficiência:** o programa lê **apenas 6 colunas** das 18 (as que
  interessam), para não estourar a memória. Esse é um cuidado típico de quem
  lida com dados grandes.

### 2.3 De 3,85 milhões de linhas para 762 pontos
Não modelamos as 3,85 milhões de linhas diretamente. Fazemos um **recorte**:
1. Filtramos as linhas de **nível estadual** (`place_type == "state"`) do estado
   de **São Paulo**. Essas linhas já trazem o **total do estado somado por dia** —
   ou seja, a soma de todos os municípios de SP já vem pronta.
2. Resultado: uma **série diária de 762 dias** (uma linha por dia), com o número
   de **casos novos** e **óbitos novos**. É essa série que alimenta os modelos.

> **Por que São Paulo e nível estadual?** Porque dá uma série longa (2 anos),
> contínua e com um padrão semanal bem forte — perfeita para estudar previsão.

### 2.4 Limpeza e preparação (o que fizemos)
O programa `src/preparar_dados.py` aplica várias **travas de segurança** de
limpeza:
- **Frequência diária garantida:** força um calendário dia a dia; se faltasse
  alguma data, ela seria preenchida com 0.
- **Valores negativos:** correções retroativas do governo às vezes geram números
  negativos ("tira casos que foram contados errado"). O código **zera** qualquer
  valor negativo.
- **Tipos e formato:** converte tudo para inteiro e ordena por data.

**Detalhe honesto e importante:** para São Paulo, a série **já estava limpa** —
**0 datas faltando** e **0 valores negativos**. Ou seja, as travas existem e
deixam o código robusto para outros estados, mas **em SP não foi preciso corrigir
nada**. Se o professor perguntar "você limpou os dados?", a resposta é:

> "Sim, a preparação garante série contínua, sem gaps, sem negativos e com tipos
> corretos. No caso de SP, a série já vinha íntegra, então nenhuma linha precisou
> ser corrigida — mas a rotina de limpeza está lá e funciona para qualquer UF."

### 2.5 O "problema" dos dados: o padrão semanal
Um detalhe crucial: **os casos caem sistematicamente nos fins de semana** e sobem
no meio da semana. Isso **não é a doença mudando** — é o **cartório**: menos gente
testa e menos laboratórios registram no sábado/domingo, e o represado sai na
semana seguinte.

Números reais (comparando com a média da semana):
- **Domingo ≈ 0,49×** a média (metade).
- **Segunda ≈ 0,29×** (a mais baixa).
- **Quinta ≈ 1,38×** (a mais alta).

Isso se chama **sazonalidade semanal**, e é justamente o que um bom modelo
precisa aprender.

---

## 3. O mínimo de teoria (explicado do zero)

### 3.1 O que é uma série temporal
É só uma **sequência de números ao longo do tempo**, em ordem: casos de ontem,
de hoje, de amanhã… A diferença para uma tabela normal é que **a ordem importa** —
o valor de hoje depende do de ontem.

### 3.2 Tendência e sazonalidade (as duas "peças")
Qualquer série pode ser pensada como a soma de:
- **Tendência:** o movimento de longo prazo (a onda subindo ou descendo).
- **Sazonalidade:** um padrão que **se repete em período fixo** (aqui, a cada 7
  dias — o padrão semanal).
- **Ruído:** o que sobra, aleatório.

### 3.3 Como medimos se a previsão é boa (as métricas)
Comparamos o que o modelo previu com o que realmente aconteceu:
- **RMSE** (raiz do erro quadrático médio): o **erro médio em número de casos**.
  **Quanto menor, melhor.** É a métrica principal. Ex.: RMSE 593 = "erra, em
  média, uns 600 casos".
- **MAE** (erro absoluto médio): parecido, também em casos, mas menos sensível a
  erros grandes isolados.
- **MAPE** (erro percentual): o erro em **porcentagem**. Cuidado: **enche o saco
  quando há dias de poucos casos** (dividir por um número pequeno explode a
  porcentagem). Por isso aqui ele parece alto e engana.
- **R²**: de 0 a 1, o quanto o modelo "explica" a variação. Perto de 1 é ótimo,
  perto de 0 é fraco.

### 3.4 Treino e teste (por que não vale "colar")
Dividimos a série em duas partes **no tempo**:
- **Treino:** o passado, que o modelo estuda (aqui, até **31/10/2021** → 601
  dias).
- **Teste:** um pedaço que o modelo **nunca viu** (os **28 dias de novembro/2021**),
  para medir o erro de verdade.

> **Por que dividir no tempo e não sortear aleatoriamente?** Porque seria
> **colar**: usar dias do futuro para prever o passado. Em série temporal, o teste
> tem que ser **sempre depois** do treino.

---

## 4. A ideia central: transformar a série numa tabela

Modelos comuns de "machine learning" não entendem "tempo" — eles entendem
**tabelas** (colunas de pistas → uma resposta). Então fazemos a mágica de
conversão:

Para prever os **casos de hoje**, criamos colunas com pistas tiradas **do próprio
passado da série**:

| Pista (coluna) | O que é |
|---|---|
| `lag_1` | casos de **ontem** |
| `lag_7` | casos de **7 dias atrás** (mesmo dia da semana passada) |
| `media_7d` | **média** dos últimos 7 dias |
| `dia da semana` | é segunda? terça? … (captura o padrão semanal) |

Fazendo isso para todos os dias, a série vira uma **tabela de 748 linhas × 15
pistas (features)**. Agora é um problema de aprendizado de máquina **qualquer**, e
qualquer modelo de tabela consegue atacar.

> **Cuidado com "colar" (vazamento de dados):** todas as pistas usam **apenas o
> passado** (ontem, semana passada…), **nunca o dia que estamos tentando prever**.
> Isso é essencial e o professor pode perguntar.

---

## 5. A "mágica": LazyPredict

### 5.1 O que é
**LazyPredict** é uma biblioteca de Python que, **numa única linha**, treina
**dezenas de modelos diferentes** na sua tabela e devolve um **ranking** de qual
errou menos. Foi o **professor que sugeriu** usá-la.

```python
from lazypredict.Supervised import LazyRegressor
modelos, _ = LazyRegressor().fit(X_treino, X_teste, y_treino, y_teste)
```

Em vez de eu escolher e ajustar cada modelo à mão (o jeito difícil), o LazyPredict
**testa todos automaticamente** e eu só olho quem venceu.

### 5.2 O que ele fez aqui
- Testou **39 modelos** em segundos.
- Ordenou todos por RMSE (erro).
- **Vencedor: BaggingRegressor**, com **RMSE 593**.

---

## 6. Os algoritmos em uma frase cada (cola de bolso)

Se o professor apontar para um nome no ranking, responda assim:

**Modelos que apareceram no LazyPredict (nossa abordagem):**
- **BaggingRegressor (o vencedor):** treina **muitas árvores de decisão**, cada
  uma vendo uma amostra sorteada dos dados, e tira a **média** das respostas. Como
  um **comitê que vota** — juntando muitos palpites, o erro cai. ("Bagging" =
  *bootstrap aggregating*.)
- **RandomForest:** quase igual ao Bagging, mas cada árvore também sorteia
  **quais colunas** olhar — dá ainda mais variedade ao "comitê".
- **Árvore de decisão:** uma sequência de perguntas sim/não ("ontem teve mais de
  X casos? foi quinta?") que leva a um palpite.
- **ExtraTrees / HistGradientBoosting:** outras variações de "muitas árvores".
- **ElasticNet / Ridge / Lasso / BayesianRidge:** **regressões lineares** (uma
  fórmula de reta) com um freio para não exagerar nos pesos.

**Modelos clássicos de série temporal (feitos à mão no seminário, para comparar):**
- **Regressão linear:** ajusta uma **reta** à tendência. O modelo mais simples.
- **Média móvel (filtro):** **suaviza** a curva tirando a média de vários dias
  (remove o serrilhado semanal).
- **Alisamento exponencial / Holt / Holt-Winters:** faz uma **média do passado com
  pesos que decaem** (dias recentes contam mais). O **Holt-Winters** também
  aprende o **padrão semanal** — por isso é o mais forte da família.
- **ARIMA:** prevê usando os **valores passados** e os **erros passados** da série.
- **SARIMA:** o ARIMA **+ o padrão sazonal** (semanal). O "S" é de *seasonal*.
- **SARIMAX:** o SARIMA **+ uma variável extra** (ex.: feriados, ou o número de
  casos ajudando a prever óbitos).

---

## 7. Resultados e conclusões

### 7.1 O placar (todos na MESMA janela — 28 dias de nov/2021)

| Modelo | Como foi feito | RMSE (erro) |
|---|---|---:|
| **Holt-Winters** | clássico, à mão | **498** ⬅ melhor de todos |
| SARIMAX | clássico, à mão | 566 |
| SARIMA | clássico, à mão | 567 |
| **BaggingRegressor** | **LazyPredict (1 linha)** | **593** ⬅ melhor automático |
| RandomForest | LazyPredict | 624 |
| Holt | clássico, à mão | 709 |
| ARIMA | clássico, à mão | 714 |
| SES | clássico, à mão | 725 |

### 7.2 Conclusões finais (o que dizer no fim)
1. **O LazyPredict é um atalho poderoso:** com **uma linha** e **zero dedução
   matemática**, ele colocou um modelo (Bagging, RMSE 593) **no mesmo patamar** dos
   modelos clássicos, **empatando com o SARIMA** (567) e **ganhando** de ARIMA,
   SES e Holt.
2. **Mas o melhor modelo de todos ainda foi o clássico Holt-Winters (498)** — um
   modelo feito sob medida para o padrão semanal. Ou seja: **automatizar acha um
   ótimo ponto de partida rápido, mas conhecimento do problema ainda vence.**
3. **A sazonalidade semanal é a chave:** todos os melhores modelos (Holt-Winters,
   SARIMA e as florestas de árvores) têm em comum o fato de **capturarem o padrão
   de 7 dias**.
4. **Mensagem prática:** use o LazyPredict para **descobrir rápido quais famílias
   de modelo valem a pena**, e depois refine à mão a mais promissora.

---

## 8. Limitações e honestidade científica (LEIA — é onde o professor ataca)

Ser transparente aqui **impressiona mais** do que fingir que deu tudo perfeito.

1. **O R² do vencedor é baixo (~0,18).** Isso quer dizer que acertar **o número
   exato de cada dia** é difícil — porque o dado é **muito ruidoso** (o serrilhado
   de notificação é meio aleatório). O modelo acerta bem o **nível e a forma geral**
   da curva, mas erra o "soluço" diário. **É uma limitação do dado, não um bug.**

2. **O MAPE parece alto (71%), mas engana.** MAPE explode em dias de poucos casos
   (dividir por número pequeno). Por isso confiamos mais no **RMSE** e no **MAE**,
   que estão competitivos.

3. **A comparação com o SARIMA não é 100% "maçã com maçã".** Aqui está o ponto
   mais delicado — saiba explicar:
   - O nosso teste do LazyPredict é uma **previsão de um passo à frente**: para
     prever o dia *t*, ele usa como pista o valor **real** do dia *t−1*. Ou seja,
     a cada dia ele "espia" o passado recente verdadeiro.
   - O SARIMA do seminário faz uma **previsão de 28 dias de uma vez**, sem espiar —
     tarefa **mais difícil**.
   - **Conclusão honesta:** a tarefa do LazyPredict foi um pouco mais fácil, então
     o "empate" com o SARIMA deve ser lido com esse asterisco. Ainda assim, é
     impressionante conseguir isso com **uma linha de código**.

4. **LazyPredict não foi feito para séries temporais.** Ele é para tabelas comuns.
   **Nós adaptamos** a série para o formato de tabela (com as pistas de defasagem).
   Funciona bem como **primeira exploração**, mas ferramentas dedicadas a série
   temporal ainda são mais indicadas para previsão de longo prazo.

5. **Dados de COVID têm defeitos conhecidos:** subnotificação, atraso na
   divulgação e revisões retroativas. Prever com semanas de antecedência é
   genuinamente difícil.

---

## 9. Perguntas que o professor pode fazer (FAQ)

**"O que é uma série temporal?"**
> Uma sequência de números em ordem no tempo, em que o valor de hoje depende dos
> anteriores. Aqui, casos de COVID por dia.

**"O que é essa sazonalidade semanal?"**
> Os casos caem no fim de semana e sobem no meio da semana porque **menos gente
> testa e registra** aos sábados/domingos. Domingo tem ~metade da média; quinta,
> ~40% a mais. É efeito da **notificação**, não da doença.

**"O LazyPredict serve para série temporal?"**
> Ele é feito para **tabelas**. Nós **transformamos** a série numa tabela criando
> colunas com os dias anteriores (defasagens). Assim qualquer modelo de tabela
> consegue prever. É uma adaptação comum e prática.

**"Como você garante que não houve vazamento de dados (colar)?"**
> Duas coisas: (1) todas as pistas usam **só o passado** — ontem, semana passada,
> média dos 7 dias anteriores — **nunca o dia previsto**; (2) o teste é
> **posterior** ao treino no tempo (treino até out/2021, teste em nov/2021), nunca
> sorteado aleatoriamente.

**"Isso é previsão de quantos dias à frente?"** *(pergunta difícil — responda com
franqueza)*
> Na avaliação do LazyPredict, é **um passo à frente**: para cada dia, ele usa o
> valor real do dia anterior. O SARIMA do seminário prevê os 28 dias de uma vez,
> que é mais difícil. Por isso a comparação tem esse asterisco — sou transparente
> quanto a isso.

**"Por que o BaggingRegressor ganhou entre os automáticos?"**
> Porque ele junta **muitas árvores de decisão** e tira a média — isso reduz o erro
> e o exagero de cada árvore isolada. Modelos de "muitas árvores" costumam ir bem
> em dados com padrões não lineares como este.

**"Por que o R² é tão baixo?"**
> Porque o dado é **muito ruidoso** (o serrilhado de notificação é quase
> aleatório). O modelo acerta a **forma e o nível** da curva, mas não o número
> exato de cada dia. Isso é limite do **dado**, não do método.

**"MAPE de 71% não é péssimo?"**
> O MAPE **engana** aqui: ele explode nos dias de poucos casos. O RMSE (~593) e o
> MAE (~448) mostram que, em casos, o erro é competitivo com os modelos clássicos.

**"Você limpou os dados?"**
> Sim: a rotina garante calendário diário contínuo, zera negativos de correções
> retroativas e corrige tipos. Para SP, a série já vinha íntegra (0 gaps, 0
> negativos), então nada precisou ser alterado — mas o processo é robusto para
> qualquer estado.

**"Qual a diferença entre o filtro de média móvel e o modelo ARIMA?"**
> A média móvel só **suaviza** a curva (é descritiva). O ARIMA é um **modelo de
> previsão** que aprende com os valores e os erros passados. São coisas
> diferentes com o nome parecido.

**"Dava para prever outra onda ou outro estado?"**
> Sim. Basta rodar `preparar_dados.py --uf RJ` (ou outra UF) e repetir. O código
> é genérico.

**"Por que não normalizou / padronizou os dados?"**
> O LazyPredict já faz isso internamente: cada modelo roda dentro de um *pipeline*
> que preenche faltantes e padroniza as colunas automaticamente.

**"O que é 'big data' aqui, se no fim são só 762 pontos?"**
> A **matéria-prima** é grande (3,85 milhões de linhas, vários estados/municípios,
> 2 anos). O desafio de big data está em **ler e agregar** isso com eficiência
> (lemos só as 6 colunas necessárias). O resultado agregado é uma série enxuta.

---

## 10. Roteiro de fala, slide a slide

Use isto como "cola" durante a apresentação (10 slides).

1. **Capa** — "Vou mostrar como prever a onda de COVID **sem deduzir nenhuma
   fórmula**, usando LazyPredict."
2. **O problema** — "Prever casos decide leitos, oxigênio, equipes. Acertar salva
   recursos e vidas."
3. **A escala** — "SP teve 5,23 milhões de casos, pico de 37.611 num dia. Essa é a
   curva que queremos prever." (mostre o gráfico)
4. **Os dados** — "Vêm do DataSUS: **3,85 milhões de registros**. Recortei SP e
   virou uma série diária limpa de 762 dias."
5. **O dado é sujo** — "Fim de semana quase não testa, então a curva serrilha toda
   semana. Domingo tem metade da média. O modelo precisa aprender isso."
6. **O caminho difícil** — "O jeito clássico é o SARIMA (mostre a fórmula
   assustadora). Semanas de matemática. **Eu não quero fazer isso à mão.**"
7. **O truque** — "Transformo a série numa **tabela**: para prever hoje, uso ontem,
   a semana passada e a média — as pistas do próprio passado."
8. **A mágica** — "Uma linha de LazyPredict testa **39 modelos** e ranqueia
   sozinho." (mostre o ranking)
9. **O resultado** — "O vencedor, BaggingRegressor, empatou com o SARIMA feito à
   mão. Fui honesto: o Holt-Winters ainda foi o melhor, mas eu cheguei perto com
   esforço quase zero."
10. **Resumo** — repita os 3 pontos: problema importa, big data real, LazyPredict é
    o atalho. "Obrigado, perguntas?"

---

## 11. Glossário relâmpago

| Termo | Em uma frase |
|---|---|
| Série temporal | Números em ordem no tempo. |
| Tendência | O movimento de longo prazo (subida/descida). |
| Sazonalidade | Padrão que se repete (aqui, a cada 7 dias). |
| Feature / pista | Uma coluna de entrada do modelo (ex.: casos de ontem). |
| Lag (defasagem) | Um valor de N dias atrás usado como pista. |
| Treino / teste | Parte que o modelo estuda / parte escondida para avaliar. |
| Vazamento de dados | "Colar" usando informação do futuro. Proibido. |
| RMSE | Erro médio em número de casos. Menor = melhor. |
| MAPE | Erro em %. Engana com valores pequenos. |
| R² | 0 a 1: quanto o modelo explica. |
| Regressão | Prever um número (aqui, casos). |
| Árvore de decisão | Perguntas sim/não que levam a um palpite. |
| Bagging / Floresta | Muitas árvores votando juntas. |
| ARIMA / SARIMA | Modelos clássicos de série temporal (com/sem sazonal). |
| LazyPredict | Testa dezenas de modelos de uma vez e ranqueia. |

---

## 12. Como reproduzir (se perguntarem)

```bash
# 1) instalar dependências
pip install -r requirements.txt

# 2) preparar a série diária a partir do dataset bruto
python src/preparar_dados.py --uf SP

# 3) rodar o LazyPredict (gera o ranking e as figuras)
python src/lazy_predict_forecast.py
```

Os números deste guia saem de `dados/lazy_resultados.json` (LazyPredict) e
`dados/resultados.json` (modelos clássicos). Os slides estão em
`slides/pitch_lazypredict.html` (abre no navegador) e
`slides/pitch_lazypredict.pdf` (LaTeX).

---

> **Dica final:** se travar numa pergunta, seja honesto — "essa é uma limitação
> que eu conheço" vale mais que inventar. Os pontos da **Seção 8** já te dão as
> respostas maduras para quase tudo que podem perguntar. Boa apresentação!
