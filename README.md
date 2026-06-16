# EpiCurve Analyzer — Séries Temporais aplicadas à COVID-19

Seminário de **Séries Temporais** construído sobre uma série real: os **casos
diários de COVID-19 no estado de São Paulo** (DataSUS / Brasil.IO). O projeto
nasceu de um trabalho de *Cálculo Numérico* (ajuste de curvas / regressão
linear) e foi **adaptado** para cobrir toda a ementa de séries temporais — da
**regressão linear simples** até o **SARIMAX**.

> **Entregável principal:** a apresentação em LaTeX/Beamer
> [`slides/seminario_series_temporais.pdf`](slides/seminario_series_temporais.pdf)
> (48 slides), gerada a partir das figuras e dos números produzidos pelos
> scripts em [`src/`](src/).

---

## Cobertura da ementa

| Tópico da ementa | Onde está | Figura(s) |
|---|---|---|
| Introdução aos modelos de séries temporais | Slides §1; conceitos + estudo de caso | `01` |
| Análise exploratória e estacionariedade (ADF/KPSS) | Slides §2 | `02`, `03`, `04` |
| **Regressão linear simples** (modelo de tendência) | Slides §3; `secao_regressao_linear` | `05`, `06` |
| Alisamento exponencial (SES, Holt, Holt-Winters) | Slides §4; `secao_alisamento` | `07` |
| Médias móveis (MA) e função de autocorrelação (ACF) | Slides §5–6; `secao_acf_pacf` | `08`, `09` |
| Autorregressivos (AR) e autocorrelação parcial (PACF) | Slides §7 | `09` |
| ARMA | Slides §8 | — |
| ARIMA | Slides §9; `secao_arima_familia` | `10`, `11` |
| Sazonalidade: SARMA e SARIMA | Slides §10 | `10` |
| Modelagem com variáveis exógenas (SARIMAX) | Slides §11; `secao_exogena_obitos` | `12`, `14` |
| Comparação de modelos e conclusões | Slides §12 | `13` |

A **regressão linear simples** é o elo com a disciplina de origem: além do
modelo de tendência `y = β₀ + β₁·t`, mostramos a **linearização** do
crescimento exponencial (`ln y = ln A + k·t`) e usamos o teste de
**Durbin-Watson** para evidenciar a autocorrelação dos resíduos — a motivação
para todo o restante do seminário.

---

## Estrutura do projeto

```
Epicurve-analyzer/
├── README.md
├── requirements.txt
├── caso_full.csv.gz                 # dataset bruto (DataSUS/Brasil.IO, ~3,85M registros)
├── src/
│   ├── preparar_dados.py            # extrai e limpa a série diária (UF) -> dados/serie_*.csv
│   └── analise_series_temporais.py  # toda a análise; gera figuras/ e dados/resultados.json
├── dados/
│   ├── serie_sp.csv                 # série diária pronta (casos e óbitos)
│   └── resultados.json              # números exatos usados nos slides
├── figuras/                         # 14 figuras (PNG) geradas pela análise
├── slides/
│   ├── seminario_series_temporais.tex
│   └── seminario_series_temporais.pdf
└── (legado de Cálculo Numérico)
    ├── modelagem_epidemias_dataset.py
    ├── examinar_dataset.py
    └── material_ajuste_de_curvas.ipynb
```

---

## Como executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Preparar a série temporal
Lê o `caso_full.csv.gz` e gera `dados/serie_sp.csv` (use `--uf` para outra UF):
```bash
python src/preparar_dados.py --uf SP
```

### 3. Rodar toda a análise (gera figuras + resultados)
```bash
python src/analise_series_temporais.py
```

### 4. Compilar os slides (requer LaTeX, ex.: MiKTeX)
A partir da raiz do projeto, rode **duas vezes** (para o sumário):
```bash
pdflatex -output-directory=slides slides/seminario_series_temporais.tex
pdflatex -output-directory=slides slides/seminario_series_temporais.tex
```

---

## Principais resultados (backtest de 28 dias — nov/2021)

| Modelo | RMSE | MAPE | AIC |
|---|---:|---:|---:|
| SES | 725 | 80% | — |
| Holt | 709 | 83% | — |
| **Holt-Winters** | **498** | **40%** | — |
| ARIMA(2,1,2) | 714 | 79% | 1877 |
| SARIMA(2,1,2)(1,1,1)₇ | 567 | 40% | 1663 |
| SARIMAX (+feriados) | 566 | 40% | 1665 |

- Os modelos que tratam a **sazonalidade semanal** (Holt-Winters, SARIMA,
  SARIMAX) reduzem o erro em ~30% frente aos não-sazonais.
- **Variáveis exógenas** (exemplo óbitos ~ casos): o AIC cai de **1257 → 1011**
  e o RMSE −7%, ilustrando o ganho quando a covariável traz informação nova —
  ao contrário dos feriados, cujo efeito é mínimo (−0,5%) pois a sazonalidade
  já o captura.

---

## Sobre o Dataset

`caso_full.csv.gz` — registros diários de COVID-19 por município/estado
(DataSUS / SEIDIGI–TABNET, via Brasil.IO).

- **Período:** 25/02/2020 a 27/03/2022 · **~3,85 milhões** de registros · 18 colunas.
- **Recorte do seminário:** nível **estadual de SP** → série **diária** com
  **762 observações** (casos e óbitos novos), contínua e sem lacunas.
- **Variável-alvo:** `new_confirmed` (casos novos/dia); exógena de exemplo:
  `new_deaths`.

### Por que há sazonalidade semanal?
A subnotificação de fins de semana e feriados (menos testagem/registro, com
divulgação represada na semana seguinte) cria um padrão **semanal (s=7)**
sistemático no *processo de medição* — domingo ≈ 0,49× e quinta ≈ 1,38× a média
semanal. É justamente o que torna esta série ideal para demonstrar
**SARIMA/SARIMAX**.

---

## Referências

- BOX, JENKINS, REINSEL, LJUNG. *Time Series Analysis: Forecasting and Control*. 5ª ed. Wiley, 2015.
- MORETTIN, P. A.; TOLOI, C. M. C. *Análise de Séries Temporais*. 3ª ed. Blucher, 2018.
- HYNDMAN, R. J.; ATHANASOPOULOS, G. *Forecasting: Principles and Practice*. 3ª ed. OTexts, 2021 — [otexts.com/fpp3](https://otexts.com/fpp3/).
- BROCKWELL, P. J.; DAVIS, R. A. *Introduction to Time Series and Forecasting*. 3ª ed. Springer, 2016.
- **Dados:** DATASUS [datasus.saude.gov.br](https://datasus.saude.gov.br/) · Brasil.IO [brasil.io/dataset/covid19](https://brasil.io/dataset/covid19/).

---

> **Nota:** edite o autor/instituição no início de
> `slides/seminario_series_temporais.tex` antes de apresentar.
