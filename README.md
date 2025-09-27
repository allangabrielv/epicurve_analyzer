#  EpiCurve Analyzer - Projeto de Cálculo Numérico

**Transformando dados em decisões que salvam vidas**

---

## Sobre o Projeto

O **EpiCurve Analyzer** é uma ferramenta desenvolvida para o projeto da disciplina de Cálculo Numérico, seguindo a metodologia do LMVN (Laboratório Virtual de Métodos Numéricos) do Prof. Dr. Gustavo Charles Peixoto de Oliveira, docente da Cadeira de Cálculo Numérico para o Curso de Ciência da Computação da UFPB.

### Objetivo
Implementar e comparar métodos de ajuste de curvas para modelagem epidemiológica, utilizando exclusivamente as técnicas abordadas em aula:
- **Regressão Linear** (`scipy.stats.linregress`)
- **Ajuste Exponencial** via linearização logarítmica
- **Ajustes Polinomiais** (`numpy.polyfit`) de graus 2 a 5

### Diferencial
- **Análise automatizada** de precisão com métricas RMSE, MAE e MAPE
- **Predições futuras de disseminação** para os próximos 14 dias
- **Interpretação epidemiológica** dos resultados
- **Impacto econômico** quantificado das decisões baseadas em dados
- **Visualizações interativas** para gestores de saúde pública e instituições

---

## Sobre o Dataset (Conjunto de Dados)

O caso_full.csv.gz é um dataset epidemiológico fornecido pelo Ministério da Saúde contendo registros históricos de casos relacionados à COVID-19. O arquivo foi projetado para análise de tendências epidemiológicas e modelagem preditiva.
O Conjunto de Dados contém **3.8 Milhões de Registros** de Reports Municipais Diários, para todas as **5570 cidades** do país. O arquivo bruto foi extraído diretamente do **DataSUS (SEIDIGI) - TABNET**.
O Período epidemiológico analisado se inicia em **24 de fevereiro de 2020** e se estende até **27 de fevereiro de 2022**.

### Estrutura : Dados tabulares organizados por localização geográfica e período temporal
**Características Técnicas:**
- **Tamanho em memória**: 1.39 GB
- **Número de registros**: 3,853,648 (Reports)
- **Número de colunas**: 18
   **Colunas Disponíveis:**
  1. `city` - Nome do município
  2. `city_ibge_code` - Código IBGE da cidade
  3. `date` - Data do registro (YYYY-MM-DD)
  4. `epidemiological_week` - Semana epidemiológica
  5. `estimated_population` - População estimada atual
  6. `estimated_population_2019` - População estimada em 2019
  7. `is_last` - Indica se é o último registro
  8. `is_repeated` - Indica registro repetido
  9. `last_available_confirmed` - Últimos casos confirmados disponíveis
  10. `last_available_confirmed_per_100k_inhabitants` - Casos por 100k habitantes
  11. `last_available_date` - Data do último registro disponível
  12. `last_available_death_rate` - Taxa de mortalidade mais recente
  13. `last_available_deaths` - Óbitos mais recentes
  14. `order_for_place` - Ordem cronológica por localização
  15. `place_type` - Tipo de localização (município/estado)
  16. `state` - Estado (UF)
  17. `new_confirmed` - **Novos casos confirmados** (variável-alvo principal)
  18. `new_deaths` - Novos óbitos

---

## Pré-requisitos

### Bibliotecas Python necessárias:
```bash
pip install pandas numpy scipy matplotlib scikit-learn
```

### Arquivos necessários:
- `caso_full.csv.gz` - Dataset com dados epidemiológicos
- `modelagem_epidemias_dataset.py` - Script principal

---

## Como Executar

### Passo 1: Preparação
1. Certifique-se de que o arquivo `caso_full.csv.gz` está na pasta do projeto
2. Instale as dependências listadas acima

### Passo 2: Execução
```bash
python modelagem_epidemias_dataset.py
```

### Passo 3: Interação
- O sistema irá listar algumas das cidades disponíveis
- Digite o nome de uma cidade ou pressione Enter para usar a padrão
- Aguarde a análise automática ser executada

---

## Funcionalidades

### 1. Análise Exploratória
- Carregamento e limpeza automática dos dados
- Visualização inicial da distribuição de casos
- Seleção interativa de cidade para análise

### 2. Modelagem Matemática
- **Linear**: Identifica tendências de crescimento/declínio
- **Exponencial**: Calcula taxa de crescimento e tempo de duplicação
- **Polinomial**: Estima picos epidêmicos (grau 2) e curvas complexas

### 3. Análise de Precisão
- **R²**: Coeficiente de determinação
- **RMSE**: Raiz do erro quadrático médio
- **MAE**: Erro absoluto médio
- **MAPE**: Erro percentual absoluto médio

### 4. Predições Futuras
- Projeções para os próximos 14 dias
- Cenários de alavancagem de casos
- Estimativa de tempo para dobrar/triplicar casos

### 5. Impacto Econômico
- Cálculo de custos evitados com ação preventiva
- ROI (Retorno sobre Investimento) da ferramenta
- Comparação de cenários com/sem intervenção

### 6. Visualizações
- **6 gráficos especializados**:
  1. Dados originais e análise inicial
  2. Comparação Linear vs Exponencial
  3. Todos os ajustes polinomiais
  4. Melhor modelo destacado
  5. Projeções futuras com zona de incerteza
  6. Dashboard de precisão (2x2)

---

## Metodologia Científica

### Alinhamento com a Disciplina e Módulo do LVMN
- **scipy.stats.linregress**: Regressão linear completa
- **numpy.polyfit**: Ajustes polinomiais de múltiplos graus
- **Linearização exponencial**: Transformação ln(y) vs x
- **Comparação por R²**: Critério de seleção do melhor modelo
- **Interpretação estatística**: Significado epidemiológico

---

## Exemplo de Uso

```python
# Execução automática:
python modelagem_epidemias_dataset.py

# Saída esperada:
  CIDADES DISPONÍVEIS PARA ANÁLISE:
1. São Paulo - 1000 registros
2. Rio de Janeiro - 800 registros
...

 Digite o nome da cidade (ou Enter para São Paulo): 

 PROCESSANDO DADOS...
 Dados carregados: 1000 registros válidos

 RESULTADOS DA MODELAGEM:
 Melhor modelo: Polinômio Grau 2 (R² = 0.891)
 Erro médio: ±12.3 casos/dia
 Pico estimado: Dia 45 com 287 casos

 IMPACTO ECONÔMICO:
 Economia potencial: R$ 2.450.000
 ROI da ferramenta: 300x o investimento
```
---

## Imagens-exemplo do Dashboard para a cidade de Fortaleza - CE

![](/assets/Figure_1.png)
---
![](/assets/Figure_2.png)
---
![](/assets/Figure_3.png)
---

## Desafios
### Subnotificação Sistemática:
- **Casos assintomáticos**: Grande parcela não testada (~40-60% dos casos reais)
- **Testagem limitada**: Capacidade diagnóstica insuficiente, especialmente 2020-2021
- **Acesso desigual**: Populações vulneráveis com menor acesso a testes
- **Casos leves**: Muitos não procuram assistência médica

### Defasagem e Acúmulo de Reports:
- **Atraso de notificação**: 3-7 dias entre ocorrência e registro oficial
- **Reports acumulados**: Backlog de casos notificados em lotes
- **Fins de semana e Feriados**: Redução artificial nos sábados/domingos e distorções em períodos festivos
- **Regularização posterior**: Correções retroativas alteram histórico
- **Revisões retroativas**: Reclassificação de casos suspeitos


### Dependência de Infraestrutura Local:
- **Secretarias municipais**: Capacidade técnica heterogênea
- **Sistemas de informação**: SIVEP, e-SUS, GAL com inconsistências
- **Recursos humanos**: Equipes sobrecarregadas em períodos críticos
- **Padronização**: Critérios diagnósticos variam entre regiões

### Viés de Detecção Regional:
- **Capacidade laboratorial**: Grandes centros vs interior
- **Protocolos de testagem**: Mudanças de critério ao longo do tempo
- **Estratégias de vigilância**: Testagem ativa vs passiva
- **Recursos financeiros**: Orçamento municipal para vigilância epidemiológica
- **Duplicações**: Mesmo caso notificado em múltiplos sistemas

### Fatores Socioeconômicos Não Capturados:
- **Mobilidade populacional**: Fluxos migratórios não registrados
- **Densidade demográfica**: Variações intramunicipais significativas
- **Condições habitacionais**: Aglomeração e ventilação inadequada
- **Acesso a saúde**: Cobertura e qualidade dos serviços locais
- **Comportamento social**: Adesão a medidas preventivas

### Limitações Técnicas :
- **Definição de "novo caso"**: Critérios podem variar
- **Classificação final**: Confirmado vs provável vs descartado
- **Geocoding**: Problemas na identificação municipal precisa

---

## Referências

### Subnotificação de Casos

**Li, R., Pei, S., Chen, B., et al. (2020)**  
*"Substantial undocumented infection facilitates the rapid dissemination of novel coronavirus (SARS-CoV-2)"*  
Revela que a subnotificação é um fenômeno comum em vigilância epidemiológica.
[10.1126/science.abb3221](https://doi.org/10.1126/science.abb3221) 

**Maugeri, A., Barchitta, M., Battiato, S., et al. (2020)**  
*"Modeling the novel coronavirus (COVID-19) outbreak in Sicily, Italy"*  
Desenvolve métodos estatísticos para correção da subnotificação em dados epidemiológicos regionais.
[PMID:32660125](https://pubmed.ncbi.nlm.nih.gov/32660125) 

### Casos Leves/Assintomáticos Não Detectados

**Byambasuren, O., Cardona, M., Bell, K., et al. (2020)**  
*"Estimating the extent of asymptomatic COVID-19 and its potential for community transmission: systematic review and meta-analysis"*  
Quantifica a proporção de casos assintomáticos (estimativa: 20-40%), fundamentando a necessidade de ajustes em modelos epidemiológicos baseados apenas em casos sintomáticos notificados.
[PMID:36340059](https://pubmed.ncbi.nlm.nih.gov/36340059)

**Oran, D.P., Topol, E.J. (2020)**  
*"Prevalence of asymptomatic SARS-CoV-2 infection: a narrative review"*  
Compila evidências sobre a prevalência de infecções assintomáticas.
[PMID:32491919](https://pubmed.ncbi.nlm.nih.gov/32491919)

### Redução Artificial em Finais de Semana e Atrasos de Notificação

**Bastos, S.B., Cajueiro, D.O. (2020)**  
*"Modeling and forecasting the early evolution of the Covid-19 pandemic in Brazil"*  
Analisa padrões de notificação no Brasil, identificando reduções sistemáticas em finais de semana e feriados que afetam a qualidade dos dados para modelagem.
[Bastos & Cajueiro (2020) - Scientific Reports](https://www.nature.com/articles/s41598-020-76257-1)

**Dehning, J., Zierenberg, J., Spitzner, F.P., et al. (2020)**  
*"Inferring change points in the spread of COVID-19 reveals the effectiveness of interventions"*  
Desenvolve métodos estatísticos para correção de atrasos de notificação em séries temporais epidemiológicas.
[10.1126/science.abb9789](https://www.science.org/doi/10.1126/science.abb9789)

### Acesso Desigual aos Cuidados de Saúde

**Webb Hooper, M., Nápoles, A.M., Pérez-Stable, E.J. (2020)**  
*"COVID-19 and Racial/Ethnic Disparities"*  
Documenta disparidades significativas no acesso a testagem e cuidados médicos entre diferentes grupos socioeconômicos.
[Webb Hooper et al. (2020) - JAMA](https://jamanetwork.com/journals/jama/fullarticle/2766098)

**Mackey, K., Ayers, C.K., Kondo, K.K., et al. (2021)**  
*"Racial and Ethnic Disparities in COVID-19-Related Infections, Hospitalizations, and Deaths: A Systematic Review"*  
Revisão sistemática que quantifica disparidades no acesso aos serviços de saúde durante a pandemia.
[PMID:33253040](https://pubmed.ncbi.nlm.nih.gov/33253040)

### Fontes Oficiais do Ministério da Saúde

- **DATASUS**: [datasus.saude.gov.br](https://datasus.saude.gov.br/)
- **TABNET**: [Informações de Saúde](https://datasus.saude.gov.br/informacoes-de-saude-tabnet/)
- **INFOMS COVID-19**: [Painel COVID-19](https://infoms.saude.gov.br/extensions/covid-19_html/covid-19_html.html)
- **Portal COVID-19**: [covid.saude.gov.br](https://covid.saude.gov.br/)

---

## Estrutura do Projeto

```
linear_regression_project/
├── README.md                        # Este arquivo
├── modelagem_epidemias_dataset.py   # Script principal
├── examinar_dataset.py              # Script de verificação
├── caso_full.csv.gz                # Dataset (3.8M de Reports)
├── material_ajuste_de_curvas.ipynb # Material-base do projeto
├── assets/                        # Imagens do dashboard do projeto
└── requirements.txt                 # Dependências (opcional)

```

---
