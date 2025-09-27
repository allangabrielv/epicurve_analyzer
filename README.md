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
- **Predições futuras** para os próximos 14 dias
- **Interpretação epidemiológica** completa dos resultados
- **Impacto econômico** quantificado das decisões baseadas em dados
- **Visualizações interativas** para gestores de saúde pública e instituições

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
- O sistema irá listar as cidades disponíveis
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

### Inovações Implementadas
- **Automação completa** do processo de análise
- **Métricas de precisão** além do R²
- **Sistema de predições** com intervalo de confiança
- **Contexto de negócio** para gestores públicos
- **Storytelling quantitativo** do valor gerado

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
![](/assets/Figure_1.png)
---
![](/assets/Figure_2.png)
---
![](/assets/Figure_3.png)
---

## Estrutura do Projeto

```
linear_regression_project/
├── README.md                        # Este arquivo
├── modelagem_epidemias_dataset.py   # Script principal
├── examinar_dataset.py              # Script de verificação
├── caso_full.csv.gz                # Dataset (3.8M registros)
├── material_ajuste_de_curvas.ipynb # Material-base do projeto
├── assets/                        # Imagens do dashboard do projeto
└── requirements.txt                 # Dependências (opcional)

```

---
