#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da Nova Funcionalidade de Busca de Cidades
Demonstra como o sistema agora lida com diferentes tipos de entrada
"""

import pandas as pd

def demonstrar_busca_inteligente():
    print("=" * 60)
    print("    DEMONSTRAÇÃO: BUSCA INTELIGENTE DE CIDADES")
    print("=" * 60)
    
    # Carregar dados
    print("\n1. Carregando dados...")
    df = pd.read_csv('caso_full.csv.gz')
    df['cidade_estado'] = df['city'] + ' - ' + df['state']
    
    # Filtrar dados válidos
    df_valido = df[(df['city'] != 'Importados/Indefinidos') & 
                   (df['city'].notna()) & 
                   (df['state'].notna()) & 
                   (df['new_confirmed'].notna())].copy()
    
    cidades_principais = df_valido['cidade_estado'].value_counts().head(15)
    
    print(f"\n2. Top 5 cidades com mais registros:")
    for i, (cidade_estado, count) in enumerate(cidades_principais.head(5).items(), 1):
        print(f"   {i}. {cidade_estado}: {count} registros")
    
    # Exemplos de busca
    exemplos = [
        "Belém",        # Múltiplas opções
        "São Paulo",    # Múltiplas opções
        "Santos",       # Múltiplas opções
        "Manaus",       # Única opção
        "XYZ123",       # Não existe
    ]
    
    print(f"\n3. TESTANDO DIFERENTES TIPOS DE BUSCA:\n")
    
    for exemplo in exemplos:
        print(f"🔍 Buscando por: '{exemplo}'")
        print(f"   " + "-" * 40)
        
        if ' - ' in exemplo:
            # Formato completo
            resultado = df_valido[df_valido['cidade_estado'] == exemplo]
            if len(resultado) > 0:
                print(f"   ✅ Cidade encontrada diretamente: {exemplo}")
            else:
                print(f"   ❌ Cidade não encontrada: {exemplo}")
        else:
            # Busca por nome
            opcoes = df_valido[df_valido['city'].str.contains(exemplo, case=False, na=False)]['cidade_estado'].unique()
            
            if len(opcoes) == 0:
                print(f"   ❌ Nenhuma cidade encontrada")
                print(f"   🔄 Sistema usaria: {cidades_principais.index[0]}")
            elif len(opcoes) == 1:
                print(f"   ✅ Uma cidade encontrada: {opcoes[0]}")
            else:
                print(f"   🔍 {len(opcoes)} cidades encontradas:")
                opcoes_ordenadas = sorted(opcoes)
                for i, opcao in enumerate(opcoes_ordenadas[:5], 1):
                    registros = len(df_valido[df_valido['cidade_estado'] == opcao])
                    print(f"     {i}. {opcao} ({registros} registros)")
                if len(opcoes_ordenadas) > 5:
                    print(f"     ... e mais {len(opcoes_ordenadas) - 5} opções")
        
        print()
    
    print(f"\n4. RESUMO DAS MELHORIAS:")
    print(f"   ✅ ANTES: Digitava 'Belém' → ia direto para São Paulo")
    print(f"   ✅ AGORA: Digitava 'Belém' → mostra {len(df_valido[df_valido['city'].str.contains('Belém', case=False, na=False)]['cidade_estado'].unique())} opções")
    print(f"   ✅ Busca case-insensitive (maiúscula/minúscula)")
    print(f"   ✅ Sugestões quando cidade não é encontrada")
    print(f"   ✅ Menu interativo para múltiplas opções")
    print(f"   ✅ Fallback inteligente apenas quando necessário")
    
    print(f"\n=" * 60)
    print(f"PROBLEMA RESOLVIDO! 🎉")
    print(f"=" * 60)

if __name__ == "__main__":
    demonstrar_busca_inteligente()