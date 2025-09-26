import pandas as pd

df = pd.read_csv('caso_full.csv.gz')

print("Primeiras linhas:")
print(df.head())

print(f"\nTamanho: {df.shape[0]} linhas e {df.shape[1]} colunas")