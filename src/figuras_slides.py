# -*- coding: utf-8 -*-
"""
Gera figuras no TEMA ESCURO do deck (pitch) que espelham os gráficos do notebook
Colab — para os slides fazerem sentido junto com a apresentação ao vivo.

Saídas:
  figuras/slide_distribuicao.png   -> histograma (casos e log)
  figuras/slide_dia_semana.png     -> boxplot por dia da semana
  figuras/slide_treino_teste.png   -> separação treino/teste no tempo
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
FIG = RAIZ / "figuras"

BG = "#0b0b0b"
VERM = "#C81E1E"
VERM_HI = "#FF5C5C"
VERDE = "#43D17A"
AZUL = "#6FA8CC"
TXT = "#EDEDED"
MUT = "#9a9a9a"
CORTE = "2021-10-31"
H = 28


def estilo(ax):
    ax.set_facecolor(BG)
    for s in ax.spines.values():
        s.set_color("#555")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors=TXT)
    ax.yaxis.label.set_color(TXT)
    ax.xaxis.label.set_color(TXT)
    ax.title.set_color("#FFFFFF")
    ax.grid(alpha=0.18, color="#888")


def carregar():
    d = pd.read_csv(DADOS / "serie_sp.csv", parse_dates=["date"])
    return d.sort_values("date").reset_index(drop=True)


def fig_distribuicao(d):
    y = d["new_confirmed"].astype(float)
    fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.6), facecolor=BG)
    for ax in axs:
        estilo(ax)
    axs[0].hist(y, bins=40, color=AZUL, alpha=0.9)
    axs[0].set_title("Casos diários — distribuição real")
    axs[0].set_xlabel("casos/dia"); axs[0].set_ylabel("frequência")
    axs[1].hist(np.log1p(y), bins=40, color=VERDE, alpha=0.9)
    axs[1].set_title("Em escala log — equilibra")
    axs[1].set_xlabel("log(1 + casos/dia)")
    fig.tight_layout()
    fig.savefig(FIG / "slide_distribuicao.png", dpi=150, facecolor=BG)
    plt.close(fig)


def fig_dia_semana(d):
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    dow = d["date"].dt.dayofweek
    dados = [d.loc[dow == k, "new_confirmed"].values for k in range(7)]
    fig, ax = plt.subplots(figsize=(9.2, 4.0), facecolor=BG)
    estilo(ax)
    bp = ax.boxplot(dados, tick_labels=dias, patch_artist=True, showfliers=False,
                    medianprops=dict(color="white", lw=1.4),
                    whiskerprops=dict(color="#888"), capprops=dict(color="#888"))
    for i, box in enumerate(bp["boxes"]):
        box.set_facecolor(VERM if i in (0, 6) else AZUL)
        box.set_alpha(0.75)
        box.set_edgecolor("#aaa")
    ax.set_title("Distribuição de casos por dia da semana")
    ax.set_ylabel("casos/dia")
    fig.tight_layout()
    fig.savefig(FIG / "slide_dia_semana.png", dpi=150, facecolor=BG)
    plt.close(fig)


def fig_treino_teste(d):
    fim = pd.Timestamp(CORTE) + pd.Timedelta(days=H)
    fig, ax = plt.subplots(figsize=(10, 4.0), facecolor=BG)
    estilo(ax)
    ax.plot(d["date"], d["new_confirmed"], color=AZUL, lw=0.8, label="série (treino)")
    ax.axvspan(pd.Timestamp(CORTE), fim, color=VERM, alpha=0.28,
               label="teste (28 dias · nov/2021)")
    ax.axvline(pd.Timestamp(CORTE), color=VERM_HI, ls="--", lw=1.4)
    ax.set_title("Separação treino / teste no tempo (sem “colar”)")
    ax.set_ylabel("casos/dia")
    leg = ax.legend(loc="upper left", facecolor="#151515", edgecolor="#444")
    for t in leg.get_texts():
        t.set_color(TXT)
    fig.tight_layout()
    fig.savefig(FIG / "slide_treino_teste.png", dpi=150, facecolor=BG)
    plt.close(fig)


def fig_comparacao(d):
    """Comparação final: modelos clássicos + melhor do LazyPredict (mesma janela)."""
    res = json.loads((DADOS / "resultados.json").read_text(encoding="utf-8"))
    lz = json.loads((DADOS / "lazy_resultados.json").read_text(encoding="utf-8"))

    # naïve sazonal (repete a última semana observada antes do corte)
    casos = d.set_index("date")["new_confirmed"].asfreq("D")
    treino = casos.loc[:CORTE]
    teste = casos.loc[CORTE:].iloc[1:H + 1]
    naive = np.tile(treino.iloc[-7:].values, int(np.ceil(H / 7)))[:H]
    rmse_naive = float(np.sqrt(np.mean((teste.values - naive) ** 2)))

    lz_nome = lz["melhor"]["modelo"]
    dados = {
        "Naïve sazonal": rmse_naive,
        "ARIMA": res["modelos"]["ARIMA(2,1,2)"]["rmse"],
        f"LazyPredict\n({lz_nome})": lz["melhor"]["rmse"],
        "SARIMA": res["modelos"]["SARIMA(2,1,2)(1,1,1)7"]["rmse"],
        "Holt-Winters": res["alisamento"]["Holt-Winters"]["rmse"],
    }
    comp = pd.Series(dados).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9.2, 4.4), facecolor=BG)
    estilo(ax)
    cor = []
    for m in comp.index:
        if "Holt" in m:
            cor.append(VERDE)
        elif "LazyPredict" in m:
            cor.append("#9B7BE0")
        elif m == "SARIMA":
            cor.append(VERM_HI)
        else:
            cor.append(AZUL)
    ax.barh(comp.index, comp.values, color=cor, alpha=0.9)
    for i, v in enumerate(comp.values):
        ax.text(v, i, f"  {v:,.0f}", va="center", fontsize=10, color=TXT)
    ax.set_xlabel("RMSE no teste — 28 dias (nov/2021) · menor é melhor")
    ax.set_title("Comparação: séries temporais clássicas × LazyPredict")
    ax.margins(x=0.14)
    fig.tight_layout()
    fig.savefig(FIG / "slide_comparacao.png", dpi=150, facecolor=BG)
    plt.close(fig)


def main():
    d = carregar()
    fig_distribuicao(d)
    fig_dia_semana(d)
    fig_treino_teste(d)
    fig_comparacao(d)
    print(">> Geradas: slide_distribuicao, slide_dia_semana, slide_treino_teste, slide_comparacao")


if __name__ == "__main__":
    main()
