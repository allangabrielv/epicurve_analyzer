import pandas as pd

# Carregar dados
df = pd.read_csv('caso_full.csv.gz')

print("="*80)
print("INVESTIGAÇÃO: POR QUE CIDADES PEQUENAS TÊM TANTOS REGISTROS?")
print("="*80)

# Analisar o caso específico de "Importados/Indefinidos"
print("\n🔍 CASO ESPECIAL: 'Importados/Indefinidos'")
print("-"*50)
importados = df[df['city'] == 'Importados/Indefinidos']
print(f"Total de registros: {len(importados)}")
print(f"Estados envolvidos: {sorted(importados['state'].unique())}")
print(f"Número de estados: {len(importados['state'].unique())}")
print("\nDistribuição por estado:")
print(importados['state'].value_counts())

# Investigar outras cidades problemáticas
cidades_investigar = ['Bom Jesus', 'São Domingos', 'Santa Luzia', 'Bonito', 'Santa Helena']

print("\n\n🔍 INVESTIGAÇÃO DE CIDADES COM NOMES COMUNS")
print("="*60)

for cidade in cidades_investigar:
    print(f"\n📍 CIDADE: {cidade}")
    print("-"*30)
    
    df_cidade = df[df['city'] == cidade]
    
    if len(df_cidade) > 0:
        estados = df_cidade['state'].unique()
        print(f"Total de registros: {len(df_cidade)}")
        print(f"Estados: {sorted(estados)} ({len(estados)} estados)")
        
        if len(estados) > 1:
            print("⚠️  PROBLEMA IDENTIFICADO: Mesma cidade em múltiplos estados!")
            print("\nDistribuição por estado:")
            distribuicao = df_cidade.groupby('state').agg({
                'city': 'count',
                'estimated_population': 'first',
                'new_confirmed': 'sum',
                'new_deaths': 'sum'
            }).rename(columns={'city': 'registros'})
            
            for estado in distribuicao.index:
                pop = distribuicao.loc[estado, 'estimated_population']
                pop_str = f"{pop:,.0f}" if not pd.isna(pop) else "N/A"
                print(f"  {estado}: {distribuicao.loc[estado, 'registros']} registros, "
                      f"pop: {pop_str}, "
                      f"casos: {distribuicao.loc[estado, 'new_confirmed']}, "
                      f"óbitos: {distribuicao.loc[estado, 'new_deaths']}")
        else:
            pop = df_cidade['estimated_population'].iloc[0]
            pop_str = f"{pop:,.0f}" if not pd.isna(pop) else "N/A"
            print(f"✅ Cidade única no estado {estados[0]}, população: {pop_str}")
            
# Analisar padrão geral
print("\n\n🔍 ANÁLISE GERAL DO PROBLEMA")
print("="*50)

# Contar quantas cidades aparecem em múltiplos estados
cidades_por_estado = df.groupby('city')['state'].nunique().sort_values(ascending=False)
cidades_multiplos_estados = cidades_por_estado[cidades_por_estado > 1]

print(f"\nTotal de cidades únicas no dataset: {len(cidades_por_estado)}")
print(f"Cidades que aparecem em múltiplos estados: {len(cidades_multiplos_estados)}")
print(f"Porcentagem de cidades com problema: {len(cidades_multiplos_estados)/len(cidades_por_estado)*100:.1f}%")

print("\nTop 10 cidades com mais estados:")
for cidade, num_estados in cidades_multiplos_estados.head(10).items():
    total_registros = df[df['city'] == cidade].shape[0]
    print(f"  {cidade}: {num_estados} estados, {total_registros} registros")

# Verificar se isso explica o problema
print("\n\n💡 CONCLUSÃO")
print("="*30)
print("O problema identificado é que o dataset contém cidades com NOMES IDÊNTICOS")
print("em ESTADOS DIFERENTES, fazendo com que o .value_counts() some todos os")
print("registros de cidades homônimas como se fossem uma única cidade.")
print("\nExemplos:")
print("- 'Bom Jesus' existe no PB, PI, RN, RS e SC")
print("- 'São Domingos' existe na BA, GO, PB, SC e SE")
print("- 'Santa Luzia' existe em múltiplos estados")
print("\nQuando somamos todos os registros, parecem ser cidades grandes,")
print("mas na realidade são várias cidades pequenas com o mesmo nome!")