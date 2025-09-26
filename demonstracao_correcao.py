import pandas as pd

print("="*80)
print("DEMONSTRAÇÃO DA CORREÇÃO DO PROBLEMA DE CIDADES HOMÔNIMAS")
print("="*80)

# Carregar dados
df = pd.read_csv('caso_full.csv.gz')

print("\n🔴 PROBLEMA ORIGINAL (ANTES DA CORREÇÃO):")
print("-"*50)
print("Usando apenas o nome da cidade (df['city'].value_counts()):")
print()
cidades_problema = df['city'].value_counts().head(10)
for i, (cidade, count) in enumerate(cidades_problema.items(), 1):
    # Verificar quantos estados essa cidade aparece
    estados = df[df['city'] == cidade]['state'].unique()
    num_estados = len([e for e in estados if pd.notna(e)])
    print(f"  {i:2d}. {cidade}: {count} registros em {num_estados} estado(s)")
    if num_estados > 1:
        print(f"      ⚠️  Estados: {sorted([e for e in estados if pd.notna(e)])}")

print("\n\n🟢 SOLUÇÃO IMPLEMENTADA (APÓS A CORREÇÃO):")
print("-"*50)
print("Usando identificador único 'Cidade - Estado':")
print()

# Aplicar a correção
df['cidade_estado'] = df['city'] + ' - ' + df['state']

# Filtrar dados válidos
df_valido = df[(df['city'] != 'Importados/Indefinidos') & 
               (df['city'].notna()) & 
               (df['state'].notna()) & 
               (df['new_confirmed'].notna())].copy()

cidades_corrigido = df_valido['cidade_estado'].value_counts().head(10)
for i, (cidade_estado, count) in enumerate(cidades_corrigido.items(), 1):
    # Extrair informações da cidade
    cidade_info = df_valido[df_valido['cidade_estado'] == cidade_estado].iloc[0]
    pop = cidade_info['estimated_population']
    pop_str = f"{pop:,.0f}" if not pd.isna(pop) else "N/A"
    print(f"  {i:2d}. {cidade_estado}: {count} registros (pop: {pop_str})")

print("\n\n📊 ESTATÍSTICAS DA CORREÇÃO:")
print("-"*40)
print(f"Total de registros originais: {len(df):,}")
print(f"Registros após limpeza: {len(df_valido):,}")
print(f"Registros removidos: {len(df) - len(df_valido):,}")
print(f"Cidades únicas originais: {df['city'].nunique():,}")
print(f"Combinações cidade-estado: {df_valido['cidade_estado'].nunique():,}")

# Mostrar exemplos específicos do problema resolvido
print("\n\n🔍 EXEMPLOS DE CIDADES HOMÔNIMAS CORRIGIDAS:")
print("-"*50)
exemplos = ['Bom Jesus', 'São Domingos', 'Santa Luzia', 'Bonito']

for cidade in exemplos:
    df_cidade = df[df['city'] == cidade]
    if len(df_cidade) > 0:
        estados = sorted(df_cidade['state'].dropna().unique())
        total_registros = len(df_cidade)
        print(f"\n📍 {cidade}:")
        print(f"  - Total aparente (problema): {total_registros} registros")
        print(f"  - Estados envolvidos: {estados} ({len(estados)} estados)")
        print(f"  - Divisão correta:")
        
        for estado in estados:
            df_estado = df_cidade[df_cidade['state'] == estado]
            registros_estado = len(df_estado)
            pop = df_estado['estimated_population'].iloc[0]
            pop_str = f"{pop:,.0f}" if not pd.isna(pop) else "N/A"
            print(f"    • {cidade} - {estado}: {registros_estado} registros (pop: {pop_str})")

print("\n\n✅ CONCLUSÃO:")
print("-"*30)
print("O problema foi completamente resolvido!")
print("- Cidades homônimas agora são tratadas separadamente")
print("- Eliminados registros 'Importados/Indefinidos' que distorciam a análise")
print("- Cada cidade é identificada uniquamente por 'Cidade - Estado'")
print("- Os dados agora refletem corretamente o tamanho real de cada municipio")
print("\nA análise epidemiológica agora é muito mais precisa e confiável! 🎯")