# -*- coding: utf-8 -*-
"""
preparar_dados.py
=================
Constrói a SÉRIE TEMPORAL diária de COVID-19 usada no seminário de Séries Temporais.

Lê o dataset bruto `caso_full.csv.gz` (DataSUS / Brasil.IO, ~3,8 milhões de
registros) e extrai a série de casos e óbitos diários de uma Unidade da
Federação (padrão: São Paulo). O resultado é uma série regularmente espaçada
(frequência diária), pronta para modelagem, salva em `dados/serie_<UF>.csv`.

Por que nível estadual?
  - As linhas com `place_type == 'state'` já agregam todos os municípios da UF
    num único valor diário, produzindo uma série longa (~2 anos), contínua e com
    forte SAZONALIDADE SEMANAL (subnotificação em fins de semana/feriados) -
    exatamente o que precisamos para demonstrar SARIMA e variáveis exógenas.

Uso:
    python src/preparar_dados.py            # usa SP
    python src/preparar_dados.py --uf RJ    # outra UF
"""

import argparse
import os

import numpy as np
import pandas as pd

# Apenas as colunas necessárias -> leitura rápida e econômica de memória
COLS = [
    "date",
    "state",
    "place_type",
    "new_confirmed",
    "new_deaths",
    "estimated_population",
]

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_BRUTO = os.path.join(RAIZ, "caso_full.csv.gz")
DIR_DADOS = os.path.join(RAIZ, "dados")


def construir_serie(uf: str = "SP") -> pd.DataFrame:
    """Lê o CSV bruto e devolve a série diária contínua da UF informada."""
    print(f"Lendo {ARQ_BRUTO} (apenas {len(COLS)} colunas)...")
    df = pd.read_csv(
        ARQ_BRUTO,
        usecols=COLS,
        parse_dates=["date"],
        dtype={"state": "category", "place_type": "category"},
    )
    print(f"  registros lidos: {len(df):,}")

    # Nível estadual -> totais diários já agregados da UF
    s = df[(df["place_type"] == "state") & (df["state"] == uf)].copy()
    if s.empty:
        raise ValueError(f"Nenhum registro estadual encontrado para UF={uf!r}.")

    populacao = int(s["estimated_population"].dropna().max())
    s = s[["date", "new_confirmed", "new_deaths"]].sort_values("date")

    # Índice diário CONTÍNUO (preenche eventuais datas ausentes)
    s = s.set_index("date").asfreq("D")
    faltantes = int(s["new_confirmed"].isna().sum())
    s[["new_confirmed", "new_deaths"]] = s[["new_confirmed", "new_deaths"]].fillna(0)

    # Correções retroativas geram valores negativos -> truncar em zero
    negativos = int((s["new_confirmed"] < 0).sum())
    s["new_confirmed"] = s["new_confirmed"].clip(lower=0)
    s["new_deaths"] = s["new_deaths"].clip(lower=0)

    s = s.astype({"new_confirmed": "int64", "new_deaths": "int64"})
    s.attrs["uf"] = uf
    s.attrs["populacao"] = populacao

    print(f"  UF........................: {uf}")
    print(f"  período...................: {s.index.min():%d/%m/%Y} a {s.index.max():%d/%m/%Y}")
    print(f"  dias (observações)........: {len(s)}")
    print(f"  datas preenchidas (gaps)..: {faltantes}")
    print(f"  valores negativos zerados.: {negativos}")
    print(f"  população estimada........: {populacao:,}")
    print(f"  casos/dia (min..max)......: {s['new_confirmed'].min()} .. {s['new_confirmed'].max()}")
    return s


def main():
    ap = argparse.ArgumentParser(description="Prepara série temporal diária de COVID-19.")
    ap.add_argument("--uf", default="SP", help="Sigla da Unidade da Federação (padrão: SP)")
    args = ap.parse_args()

    os.makedirs(DIR_DADOS, exist_ok=True)
    serie = construir_serie(args.uf.upper())

    destino = os.path.join(DIR_DADOS, f"serie_{args.uf.lower()}.csv")
    serie.to_csv(destino, encoding="utf-8")
    print(f"\nSérie salva em: {destino}")


if __name__ == "__main__":
    main()
