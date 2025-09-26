import pandas as pd
import numpy as np

# Carregar e examinar o dataset
print("=" * 60)
print("ANÁLISE EXPLORATÓRIA DO DATASET caso_full.csv.gz")
print("=" * 60)

# Carregar dados
df = pd.read_csv('caso_full.csv.gz')

print(f"\n1. INFORMAÇÕES BÁSICAS:")
print(f"   - Número de registros: {df.shape[0]:,}")
print(f"   - Número de colunas: {df.shape[1]}")
print(f"   - Tamanho em memória: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print(f"\n2. COLUNAS DISPONÍVEIS:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col} ({df[col].dtype})")

print(f"\n3. PRIMEIRAS 5 LINHAS:")
print(df.head())

print(f"\n4. ESTATÍSTICAS DESCRITIVAS (colunas numéricas):")
print(df.describe())

print(f"\n5. VALORES AUSENTES:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print(f"\n6. ANÁLISE DE COLUNAS TEMPORAIS:")
date_cols = df.select_dtypes(include=['datetime64', 'object']).columns
for col in date_cols:
    unique_vals = df[col].nunique()
    print(f"   {col}: {unique_vals} valores únicos")
    if unique_vals <= 10:
        print(f"   Valores: {df[col].unique()[:10]}")
    else:
        print(f"   Amostra: {df[col].unique()[:5]}...")

print(f"\n7. COLUNAS NUMÉRICAS PARA MODELAGEM:")
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    print(f"   {col}: min={df[col].min()}, max={df[col].max()}, média={df[col].mean():.2f}")