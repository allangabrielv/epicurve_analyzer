# -*- coding: utf-8 -*-
"""
LazyPredict aplicado à previsão de casos diários de COVID-19 (SP).

Ideia (bem simples de explicar):
  1) Uma série temporal é só uma coluna de números ao longo do tempo.
  2) Transformamos essa série numa TABELA comum de aprendizado supervisionado:
     para prever o dia de hoje, usamos como "pistas" (features) os dias
     anteriores (lags), a média da última semana e o dia da semana.
  3) O LazyPredict treina DEZENAS de modelos de uma vez e devolve um ranking
     de qual erra menos. Não precisamos deduzir a matemática de cada um.

Saídas:
  dados/lazy_leaderboard.csv    -> ranking completo dos modelos
  dados/lazy_resultados.json    -> números usados nos slides
  figuras/lazy_01_leaderboard.png
  figuras/lazy_02_previsao.png
  figuras/lazy_00_tabela.png     -> ilustra "série -> tabela"
"""

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, mean_absolute_error
from lazypredict.Supervised import LazyRegressor

warnings.filterwarnings("ignore")

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
FIG = RAIZ / "figuras"
FIG.mkdir(exist_ok=True)

H_TESTE = 28          # horizonte de previsão (4 semanas)
CORTE = "2021-10-31"  # mesma janela do seminário: treina até aqui, prevê nov/2021
COR_FUNDO = "#0b0b0b"
COR_VERM = "#C81E1E"
COR_VERM_CLARO = "#FF5C5C"
COR_VERDE = "#43D17A"
COR_TXT = "#EDEDED"


# ----------------------------------------------------------------------
# 1) Série -> tabela supervisionada
# ----------------------------------------------------------------------
def carregar_serie():
    df = pd.read_csv(DADOS / "serie_sp.csv", parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def montar_tabela(df):
    """Cria as features (pistas) a partir do passado da própria série."""
    d = df.copy()
    y = d["new_confirmed"].astype(float)

    tab = pd.DataFrame({"y": y})
    # lags: casos de 1, 2, 3, 7 e 14 dias atrás
    for L in (1, 2, 3, 7, 14):
        tab[f"lag_{L}"] = y.shift(L)
    # média e desvio da última semana (já conhecidos ontem)
    tab["media_7d"] = y.shift(1).rolling(7).mean()
    tab["max_7d"] = y.shift(1).rolling(7).max()
    # dia da semana (0=segunda ... 6=domingo) em one-hot
    dow = d["date"].dt.dayofweek
    for k in range(7):
        tab[f"dow_{k}"] = (dow == k).astype(int)
    # índice de tendência (tempo)
    tab["t"] = np.arange(len(tab))

    tab = tab.dropna().reset_index(drop=True)
    datas = d["date"].iloc[-len(tab):].reset_index(drop=True)
    tab["date"] = datas.values
    return tab, datas


# ----------------------------------------------------------------------
# 2) LazyPredict
# ----------------------------------------------------------------------
def rodar_lazy(tab, datas):
    feats = [c for c in tab.columns if c not in ("y", "date")]
    X = tab[feats].values
    y = tab["y"].values

    # split temporal (mesma janela do seminário): treina até CORTE,
    # testa os 28 dias seguintes (nov/2021). Sem embaralhar.
    corte_idx = int((tab["date"] <= CORTE).sum())
    ini, fim = corte_idx, corte_idx + H_TESTE
    X_tr, X_te = X[:corte_idx], X[ini:fim]
    y_tr, y_te = y[:corte_idx], y[ini:fim]
    datas_te = datas.iloc[ini:fim].reset_index(drop=True)

    reg = LazyRegressor(verbose=0, ignore_warnings=True, predictions=True)
    modelos, previsoes = reg.fit(X_tr, X_te, y_tr, y_te)

    # recalcula RMSE/MAE/MAPE de forma consistente para todos
    linhas = []
    for nome in previsoes.columns:
        yhat = np.asarray(previsoes[nome], dtype=float)
        if not np.all(np.isfinite(yhat)):
            continue
        rmse = float(np.sqrt(mean_squared_error(y_te, yhat)))
        mae = float(mean_absolute_error(y_te, yhat))
        mask = y_te > 0
        mape = float(np.mean(np.abs((y_te[mask] - yhat[mask]) / y_te[mask])) * 100)
        r2 = float(modelos.loc[nome, "R-Squared"]) if nome in modelos.index else np.nan
        linhas.append({"modelo": nome, "rmse": rmse, "mae": mae,
                       "mape": mape, "r2": r2})

    rank = pd.DataFrame(linhas).sort_values("rmse").reset_index(drop=True)
    return rank, previsoes, y_te, datas_te


# ----------------------------------------------------------------------
# 3) Figuras
# ----------------------------------------------------------------------
def _estilo(ax):
    ax.set_facecolor(COR_FUNDO)
    for s in ax.spines.values():
        s.set_color("#555")
    ax.tick_params(colors=COR_TXT)
    ax.yaxis.label.set_color(COR_TXT)
    ax.xaxis.label.set_color(COR_TXT)
    ax.title.set_color("#FFFFFF")


def fig_tabela(tab, datas):
    """Ilustra a transformação série -> tabela."""
    cols = ["y", "lag_1", "lag_7", "media_7d", "dow_3"]
    amostra = tab[cols].iloc[40:48].copy()
    amostra.insert(0, "data", datas.iloc[40:48].dt.strftime("%d/%m").values)
    ren = {"y": "casos hoje", "lag_1": "ontem", "lag_7": "7 dias atrás",
           "media_7d": "média 7d", "dow_3": "é quinta?"}
    amostra = amostra.rename(columns=ren)

    # formata cada célula como texto (datas string, números inteiros)
    def _fmt(col, v):
        if col == "data":
            return str(v)
        if col == "é quinta?":
            return "sim" if float(v) >= 0.5 else "—"
        return f"{float(v):,.0f}"
    texto = [[_fmt(c, v) for c, v in zip(amostra.columns, linha)]
             for linha in amostra.values]

    fig, ax = plt.subplots(figsize=(9, 3.2), facecolor=COR_FUNDO)
    ax.axis("off")
    tabla = ax.table(cellText=texto,
                     colLabels=amostra.columns, loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1, 1.6)
    for (r, c), cell in tabla.get_celld().items():
        cell.set_edgecolor("#444")
        if r == 0:
            cell.set_facecolor(COR_VERM)
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#151515")
            cor = COR_VERDE if c == 1 else COR_TXT
            if c == 1:  # coluna alvo "casos hoje"
                cell.set_facecolor("#1c2b1c")
            cell.set_text_props(color=cor)
    ax.set_title("Série temporal vira uma tabela comum: prever HOJE a partir do passado",
                 color="white", fontsize=12, pad=14)
    fig.tight_layout()
    fig.savefig(FIG / "lazy_00_tabela.png", dpi=150, facecolor=COR_FUNDO)
    plt.close(fig)


def fig_leaderboard(rank, top=12):
    r = rank.head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 5.2), facecolor=COR_FUNDO)
    _estilo(ax)
    cores = [COR_VERDE if i == len(r) - 1 else COR_VERM_CLARO for i in range(len(r))]
    ax.barh(r["modelo"], r["rmse"], color=cores, edgecolor="#222")
    for i, (v, m) in enumerate(zip(r["rmse"], r["modelo"])):
        ax.text(v, i, f"  {v:,.0f}", va="center", ha="left",
                color=COR_TXT, fontsize=9)
    ax.set_xlabel("RMSE (erro de previsão — menor é melhor)")
    ax.set_title(f"LazyPredict: ranking automático dos modelos (top {top})")
    ax.margins(x=0.12)
    fig.tight_layout()
    fig.savefig(FIG / "lazy_01_leaderboard.png", dpi=150, facecolor=COR_FUNDO)
    plt.close(fig)


def fig_previsao(previsoes, y_te, datas_te, rank):
    melhor = rank.iloc[0]["modelo"]
    yhat = np.asarray(previsoes[melhor], dtype=float)
    fig, ax = plt.subplots(figsize=(9.5, 4.8), facecolor=COR_FUNDO)
    _estilo(ax)
    x = datas_te
    ax.plot(x, y_te, "-o", color=COR_TXT, lw=2, ms=4, label="casos reais")
    ax.plot(x, yhat, "--o", color=COR_VERDE, lw=2, ms=4,
            label=f"previsão · {melhor}")
    ax.set_title(f"Melhor modelo do LazyPredict — previsão de {H_TESTE} dias (nov/2021)")
    ax.legend(facecolor="#151515", edgecolor="#444", labelcolor=COR_TXT)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIG / "lazy_02_previsao.png", dpi=150, facecolor=COR_FUNDO)
    plt.close(fig)


# ----------------------------------------------------------------------
def main():
    print(">> Carregando série e montando tabela...")
    df = carregar_serie()
    tab, datas = montar_tabela(df)
    nfeat = len([c for c in tab.columns if c not in ("y", "date")])
    print(f"   tabela: {tab.shape[0]} linhas x {nfeat} features")

    print(">> Rodando LazyPredict (testando dezenas de modelos)...")
    rank, previsoes, y_te, datas_te = rodar_lazy(tab, datas)
    print(f"   {len(rank)} modelos avaliados. Top 5:")
    print(rank.head(5).to_string(index=False))

    print(">> Gerando figuras...")
    fig_tabela(tab, datas)
    fig_leaderboard(rank)
    fig_previsao(previsoes, y_te, datas_te, rank)

    rank.to_csv(DADOS / "lazy_leaderboard.csv", index=False)
    melhor = rank.iloc[0]
    res = {
        "n_features": int(len([c for c in tab.columns if c not in ("y", "date")])),
        "n_treino": int((tab["date"] <= CORTE).sum()),
        "n_teste": int(H_TESTE),
        "janela_teste": "01/11/2021–28/11/2021",
        "n_modelos_testados": int(len(rank)),
        "melhor": {
            "modelo": str(melhor["modelo"]),
            "rmse": float(melhor["rmse"]),
            "mae": float(melhor["mae"]),
            "mape": float(melhor["mape"]),
            "r2": float(melhor["r2"]),
        },
        "top10": rank.head(10).to_dict(orient="records"),
    }
    with open(DADOS / "lazy_resultados.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(">> OK. Melhor modelo:", melhor["modelo"], f"(RMSE {melhor['rmse']:.0f})")


if __name__ == "__main__":
    main()
