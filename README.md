# 🎯 EpiCurve Analyzer - Projeto Numbiosis

**Transformando dados em decisões que salvam vidas**

---

## 📋 Sobre o Projeto

O **EpiCurve Analyzer** é uma ferramenta inovadora desenvolvida para o projeto **Numbiosis** da disciplina de Cálculo Numérico, seguindo a metodologia **IMAGINAR • CRIAR • IMPACTAR**.

### 🎯 Objetivo
Implementar e comparar métodos de ajuste de curvas para modelagem epidemiológica, utilizando exclusivamente as técnicas abordadas em aula:
- **Regressão Linear** (`scipy.stats.linregress`)
- **Ajuste Exponencial** via linearização logarítmica
- **Ajustes Polinomiais** (`numpy.polyfit`) de graus 2 a 5

### 🌟 Diferencial
- **Análise automatizada** de precisão com métricas RMSE, MAE e MAPE
- **Predições futuras** para os próximos 14 dias
- **Interpretação epidemiológica** completa dos resultados
- **Impacto econômico** quantificado das decisões baseadas em dados
- **Visualizações interativas** para gestores de saúde pública

---

## 🔧 Pré-requisitos

### Bibliotecas Python necessárias:
```bash
pip install pandas numpy scipy matplotlib
```

### Arquivos necessários:
- `caso_full.csv.gz` - Dataset com dados epidemiológicos
- `modelagem_epidemias_dataset.py` - Script principal

---

## 🚀 Como Executar

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

## 📊 Funcionalidades

### 1. 🔍 Análise Exploratória
- Carregamento e limpeza automática dos dados
- Visualização inicial da distribuição de casos
- Seleção interativa de cidade para análise

### 2. 📈 Modelagem Matemática
- **Linear**: Identifica tendências de crescimento/declínio
- **Exponencial**: Calcula taxa de crescimento e tempo de duplicação
- **Polinomial**: Estima picos epidêmicos (grau 2) e curvas complexas

### 3. 🎯 Análise de Precisão
- **R²**: Coeficiente de determinação
- **RMSE**: Raiz do erro quadrático médio
- **MAE**: Erro absoluto médio
- **MAPE**: Erro percentual absoluto médio

### 4. 🔮 Predições Futuras
- Projeções para os próximos 14 dias
- Cenários de alavancagem de casos
- Estimativa de tempo para dobrar/triplicar casos

### 5. 💰 Impacto Econômico
- Cálculo de custos evitados com ação preventiva
- ROI (Retorno sobre Investimento) da ferramenta
- Comparação de cenários com/sem intervenção

### 6. 📱 Visualizações
- **6 gráficos especializados**:
  1. Dados originais e análise inicial
  2. Comparação Linear vs Exponencial
  3. Todos os ajustes polinomiais
  4. Melhor modelo destacado
  5. Projeções futuras com zona de incerteza
  6. Dashboard de precisão (2x2)

---

## 🧮 Metodologia Científica

### Alinhamento com Material do Professor
- ✅ **scipy.stats.linregress**: Regressão linear completa
- ✅ **numpy.polyfit**: Ajustes polinomiais de múltiplos graus
- ✅ **Linearização exponencial**: Transformação ln(y) vs x
- ✅ **Comparação por R²**: Critério de seleção do melhor modelo
- ✅ **Interpretação estatística**: Significado epidemiológico

### Inovações Implementadas
- 🚀 **Automação completa** do processo de análise
- 📊 **Métricas de precisão** além do R²
- 🔮 **Sistema de predições** com intervalo de confiança
- 💼 **Contexto de negócio** para gestores públicos
- 📈 **Storytelling quantitativo** do valor gerado

---

## 📈 Exemplo de Uso

```python
# Execução automática:
python modelagem_epidemias_dataset.py

# Saída esperada:
🏙️  CIDADES DISPONÍVEIS PARA ANÁLISE:
1. São Paulo - 1000 registros
2. Rio de Janeiro - 800 registros
...

📍 Digite o nome da cidade (ou Enter para São Paulo): 

🔄 PROCESSANDO DADOS...
✅ Dados carregados: 1000 registros válidos

📊 RESULTADOS DA MODELAGEM:
🥇 Melhor modelo: Polinômio Grau 2 (R² = 0.891)
🎯 Erro médio: ±12.3 casos/dia
📈 Pico estimado: Dia 45 com 287 casos

💰 IMPACTO ECONÔMICO:
💸 Economia potencial: R$ 2.450.000
📈 ROI da ferramenta: 300x o investimento
```

---

## 🎭 Storytelling: O Valor Real

### 💼 Cenário de Aplicação
**Sexta-feira, 17h**: Secretário de Saúde recebe ligação sobre aumento de casos.

**❌ ANTES**: Reunião de emergência no fim de semana, análise manual de 2-3 dias
**✅ DEPOIS**: Análise automatizada em 30 segundos, decisões científicas na segunda-feira

### 🌟 Diferenciais Competitivos
- 🎓 **Base científica**: Métodos validados academicamente
- 🔬 **Transparência total**: Metodologia explicada passo a passo
- 📱 **Interface simples**: Gestores não-técnicos conseguem usar
- 🔄 **Atualizável**: Novos dados incorporados diariamente
- 🌐 **Escalável**: Qualquer cidade do dataset

---

## 📝 Estrutura do Projeto

```
linear_regression_project/
├── README.md                        # Este arquivo
├── modelagem_epidemias_dataset.py   # Script principal
├── caso_full.csv.gz                # Dataset (3.8M registros)
└── requirements.txt                 # Dependências (opcional)
```

---

## 👥 Equipe & Contato

**Projeto Numbiosis - Cálculo Numérico**  
**Metodologia**: IMAGINAR • CRIAR • IMPACTAR  
**Foco**: Transformação de conhecimento acadêmico em soluções práticas

---

## 🏆 Resultados Esperados

### Para a Disciplina:
- ✅ Aplicação prática de todos os métodos de ajuste vistos em aula
- ✅ Comparação sistemática de modelos matemáticos
- ✅ Interpretação estatística rigorosa dos resultados
- ✅ Conexão entre teoria e aplicação real

### Para a Sociedade:
- 🏥 **Gestão pública mais eficiente** baseada em dados
- ⚡ **Tomada de decisão acelerada** em cenários críticos
- 💰 **Otimização de recursos** públicos limitados
- 📊 **Transparência científica** nas políticas de saúde

---

**🎯 EpiCurve Analyzer: Onde a matemática encontra a realidade, e os dados salvam vidas.**

---

*Desenvolvido com 💙 para o Projeto Numbiosis*
*Cálculo Numérico - 2024*