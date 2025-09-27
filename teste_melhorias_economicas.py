#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das Melhorias na Análise Econômica
Demonstra as melhorias implementadas no cálculo econômico:
1. Formatação inteligente de valores (resolve problema do 0.0M)
2. Taxa de economia dinâmica (resolve percentuais fixos para cidades pequenas)
3. Fatores de escala e urgência personalizados
"""

import numpy as np
import sys
import os

# Adicionar o diretório atual ao path para importar as funções
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar as novas funções do script principal
try:
    from modelagem_epidemias_dataset import formatar_valor_economico, calcular_taxa_economia_dinamica
except ImportError:
    print("⚠️ Não foi possível importar as funções. Executando como standalone...")
    
    def formatar_valor_economico(valor):
        """Formata valores econômicos de forma inteligente"""
        if valor >= 1000000000:  # Bilhões
            return f"R$ {valor/1000000000:.2f}B"
        elif valor >= 100000000:  # Centenas de milhões
            return f"R$ {valor/1000000:.0f}M"
        elif valor >= 10000000:   # Dezenas de milhões
            return f"R$ {valor/1000000:.1f}M"
        elif valor >= 1000000:    # Milhões
            return f"R$ {valor/1000000:.2f}M"
        elif valor >= 100000:     # Centenas de milhares
            return f"R$ {valor/1000:.0f}K"
        elif valor >= 10000:      # Dezenas de milhares
            return f"R$ {valor/1000:.1f}K"
        else:                     # Milhares ou menos
            return f"R$ {valor:,.0f}"
    
    def calcular_taxa_economia_dinamica(r2, casos_projetados, populacao_estimada=None):
        """Calcula taxa de economia dinâmica baseada em múltiplos fatores"""
        # Taxa base por R²
        if r2 >= 0.9:
            taxa_base = 0.52  # 52% para modelos excelentes
        elif r2 >= 0.7:
            taxa_base = 0.45  # 45% para modelos bons
        elif r2 >= 0.5:
            taxa_base = 0.35  # 35% para modelos moderados
        elif r2 >= 0.3:
            taxa_base = 0.25  # 25% para modelos fracos
        elif r2 >= 0.1:
            taxa_base = 0.15  # 15% para modelos muito fracos mas utilizáveis
        else:
            taxa_base = 0.08  # 8% economia mínima
        
        # Ajuste por escala de casos (cidades pequenas têm mais eficiência relativa)
        if casos_projetados <= 10:
            fator_escala = 1.3    # +30% para cidades muito pequenas
        elif casos_projetados <= 50:
            fator_escala = 1.2    # +20% para cidades pequenas
        elif casos_projetados <= 200:
            fator_escala = 1.1    # +10% para cidades médias
        elif casos_projetados <= 1000:
            fator_escala = 1.0    # Taxa padrão
        else:
            fator_escala = 0.85   # -15% para grandes centros (mais complexo)
        
        # Ajuste por urgência (mais casos = maior economia potencial)
        if casos_projetados >= 500:
            fator_urgencia = 1.15  # +15% para situações críticas
        elif casos_projetados >= 100:
            fator_urgencia = 1.08  # +8% para situações preocupantes
        else:
            fator_urgencia = 1.0   # Taxa padrão
        
        taxa_final = min(taxa_base * fator_escala * fator_urgencia, 0.65)  # Máximo 65%
        
        return taxa_final, fator_escala, fator_urgencia

def formatar_valor_antigo(valor):
    """Formatação antiga (problemática)"""
    return f"R$ {valor/1000000:.1f}M"

def calcular_taxa_economia_antiga(r2):
    """Cálculo antigo de taxa de economia (fixo)"""
    if r2 >= 0.7:
        return 0.45  # 45%
    elif r2 >= 0.4:
        return 0.32  # 32%
    else:
        return 0.18  # 18%

def demonstrar_melhorias():
    print("🔬 TESTE DAS MELHORIAS NA ANÁLISE ECONÔMICA")
    print("=" * 60)
    
    # Cenários de teste
    cenarios = [
        {"nome": "Cidade Pequena - R² Alto", "valor": 45000, "r2": 0.85, "casos": 8},
        {"nome": "Cidade Pequena - R² Baixo", "valor": 12000, "r2": 0.25, "casos": 3},
        {"nome": "Cidade Média - R² Médio", "valor": 850000, "r2": 0.55, "casos": 150},
        {"nome": "Cidade Grande - R² Alto", "valor": 25000000, "r2": 0.78, "casos": 1200},
        {"nome": "Metrópole - R² Baixo", "valor": 180000000, "r2": 0.35, "casos": 8500},
        {"nome": "Valor Muito Baixo", "valor": 2500, "r2": 0.42, "casos": 1},
    ]
    
    print("\n1️⃣ PROBLEMA DA FORMATAÇÃO (0.0M quando < 0.1M)")
    print("-" * 50)
    
    for cenario in cenarios:
        valor = cenario["valor"]
        antigo = formatar_valor_antigo(valor)
        novo = formatar_valor_economico(valor)
        
        status = "✅ Resolvido" if "0.0M" not in novo and "0.0M" in antigo else "📊 Melhorado"
        print(f"📍 {cenario['nome']}:")
        print(f"   Antigo: {antigo}")
        print(f"   Novo:   {novo} {status}")
        print()
    
    print("\n2️⃣ PROBLEMA DOS PERCENTUAIS FIXOS")
    print("-" * 50)
    
    for cenario in cenarios:
        r2 = cenario["r2"]
        casos = cenario["casos"]
        
        # Cálculo antigo
        taxa_antiga = calcular_taxa_economia_antiga(r2)
        
        # Cálculo novo
        taxa_nova, fator_escala, fator_urgencia = calcular_taxa_economia_dinamica(r2, casos)
        
        diferenca = ((taxa_nova - taxa_antiga) / taxa_antiga) * 100
        
        print(f"📍 {cenario['nome']} ({casos} casos projetados):")
        print(f"   R² = {r2:.2f}")
        print(f"   Taxa Antiga: {taxa_antiga*100:.1f}% (fixo)")
        print(f"   Taxa Nova:   {taxa_nova*100:.1f}% (dinâmico)")
        print(f"   Fatores:     Escala={fator_escala:.2f}x | Urgência={fator_urgencia:.2f}x")
        print(f"   Diferença:   {diferenca:+.1f}% {'📈' if diferenca > 0 else '📉' if diferenca < 0 else '➡️'}")
        print()
    
    print("\n3️⃣ COMPARAÇÃO DE ECONOMIA ESTIMADA")
    print("-" * 50)
    
    for cenario in cenarios:
        valor = cenario["valor"]
        r2 = cenario["r2"]
        casos = cenario["casos"]
        
        # Cálculo antigo
        taxa_antiga = calcular_taxa_economia_antiga(r2)
        economia_antiga = valor * taxa_antiga
        
        # Cálculo novo
        taxa_nova, _, _ = calcular_taxa_economia_dinamica(r2, casos)
        economia_nova = valor * taxa_nova
        
        print(f"📍 {cenario['nome']}:")
        print(f"   Custo Total: {formatar_valor_economico(valor)}")
        print(f"   Economia Antiga: {formatar_valor_economico(economia_antiga)} ({taxa_antiga*100:.1f}%)")
        print(f"   Economia Nova:   {formatar_valor_economico(economia_nova)} ({taxa_nova*100:.1f}%)")
        
        diferenca_valor = economia_nova - economia_antiga
        print(f"   Diferença: {formatar_valor_economico(abs(diferenca_valor))} {'📈' if diferenca_valor > 0 else '📉' if diferenca_valor < 0 else '➡️'}")
        print()
    
    print("\n🎯 RESUMO DAS MELHORIAS:")
    print("✅ Formatação inteligente resolve o problema do '0.0M'")
    print("✅ Taxas dinâmicas consideram tamanho da cidade e urgência")
    print("✅ Cidades pequenas recebem bonificação adequada (+20% a +30%)")
    print("✅ Grandes centros têm ajuste realístico (-15% pela complexidade)")
    print("✅ Situações críticas (>500 casos) recebem bonus de urgência")
    print("✅ Valores são apresentados em K, M ou B conforme apropriado")
    print("\n💡 As melhorias tornam a análise mais precisa e contextualizada!")

if __name__ == "__main__":
    demonstrar_melhorias()