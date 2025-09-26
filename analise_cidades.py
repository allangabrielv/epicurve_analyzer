import pandas as pd
import numpy as np

# Carregar dados
df = pd.read_csv('caso_full.csv.gz')

print("="*60)
print("ANÁLISE DAS CIDADES COM MAIS REGISTROS")
print("="*60)

# Top 15 cidades por número de registros
print("\nTop 15 cidades por número de registros:")
top_cidades = df['city'].value_counts().head(15)
print(top_cidades)

# Análise das cidades mencionadas pelo usuário
cidades_problema = ['Importados/Indefinidos', 'Bom Jesus', 'São Domingos', 'Santa Luzia', 
                   'Bonito', 'Santa Helena', 'São Francisco', 'Santa Inês', 'Vera Cruz', 'Planalto']

print("\n" + "-"*60)
print("ANÁLISE DETALHADA DAS CIDADES MENCIONADAS:")
print("-"*60)

for cidade in cidades_problema:
    df_cidade = df[df['city'] == cidade]
    if len(df_cidade) > 0:
        print(f"\n🏙️  CIDADE: {cidade}")
        print(f"   📊 Número de registros: {len(df_cidade)}")
        print(f"   📍 Estado(s): {df_cidade['state'].unique()}")
        print(f"   👥 População estimada: {df_cidade['estimated_population'].iloc[0] if not pd.isna(df_cidade['estimated_population'].iloc[0]) else 'N/A'}")
        print(f"   📅 Período dos dados: {df_cidade['date'].min()} a {df_cidade['date'].max()}")
        print(f"   🏥 Total de casos confirmados: {df_cidade['new_confirmed'].sum()}")
        print(f"   ⚰️  Total de óbitos: {df_cidade['new_deaths'].sum()}")
        
        # Verificar se tem dados válidos para análise
        dados_validos = df_cidade[(df_cidade['new_confirmed'] > 0) & 
                                 (~pd.isna(df_cidade['new_confirmed'])) & 
                                 (~pd.isna(df_cidade['order_for_place']))]
        print(f"   ✅ Registros válidos para análise: {len(dados_validos)}")
        
    else:
        print(f"\n❌ {cidade}: Não encontrada no dataset")

# Verificar se existe alguma inconsistência
print("\n" + "="*60)
print("ANÁLISE DE POSSÍVEIS PROBLEMAS NO DATASET:")
print("="*60)

# Verificar registros duplicados
print(f"\n🔍 Registros totais no dataset: {len(df)}")
print(f"🔍 Registros únicos (city + date): {len(df.drop_duplicates(['city', 'date']))}")
duplicados = len(df) - len(df.drop_duplicates(['city', 'date']))
print(f"❗ Possíveis registros duplicados: {duplicados}")

# Verificar valores ausentes na coluna city
print(f"\n🔍 Registros com city = NaN: {df['city'].isna().sum()}")
print(f"🔍 Registros com city vazia: {(df['city'] == '').sum()}")

# Verificar cidades com nomes similares
print("\n🔍 VERIFICAÇÃO DE NOMES SIMILARES:")
for cidade in ['São Francisco', 'Santa Luzia', 'Bom Jesus']:
    cidades_similares = df[df['city'].str.contains(cidade, na=False, case=False)]['city'].unique()
    if len(cidades_similares) > 1:
        print(f"   {cidade}: {len(cidades_similares)} variações encontradas")
        for variacao in cidades_similares:
            count = df[df['city'] == variacao].shape[0]
            print(f"      - {variacao}: {count} registros")