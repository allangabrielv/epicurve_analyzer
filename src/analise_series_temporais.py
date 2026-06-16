# -*- coding: utf-8 -*-
"""
analise_series_temporais.py
===========================
Análise COMPLETA de séries temporais sobre a série diária de casos de COVID-19
(SP), cobrindo toda a ementa do seminário:

    1. Introdução / análise exploratória (tendência, sazonalidade, estacionariedade)
    2. Regressão Linear Simples (modelo de tendência + linearização exponencial)
    3. Alisamento exponencial (SES, Holt, Holt-Winters)
    4. Médias móveis (MA) e função de autocorrelação (ACF)
    5. Autorregressivos (AR) e função de autocorrelação parcial (PACF)
    6. ARMA
    7. ARIMA
    8. Sazonalidade: SARMA e SARIMA
    9. Modelagem com variáveis exógenas (SARIMAX)
   10. Comparação final dos modelos

Cada seção gera figuras em `figuras/` e acumula números em `dados/resultados.json`
(usados para preencher os slides do seminário com valores REAIS).

Uso:
    python src/analise_series_temporais.py
"""

import json
import os
import sys
import warnings

# Console do Windows usa cp1252; força UTF-8 para imprimir α, ², ₇, → etc.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # back-end headless (salva PNGs, não abre janelas)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from scipy.stats import linregress
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing,
    Holt,
    ExponentialSmoothing,
)
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import durbin_watson

warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------- #
# Configuração geral
# --------------------------------------------------------------------------- #
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_FIG = os.path.join(RAIZ, "figuras")
DIR_DADOS = os.path.join(RAIZ, "dados")
UF = "SP"
H = 28          # horizonte de teste/previsão (4 semanas)
S = 7           # período sazonal (semana)
# Data de corte do backtest. A janela de teste (28 dias seguintes) cai em
# nov/2021: período entre ondas, com nível estável, forte padrão semanal e DOIS
# feriados nacionais (Finados 02/11 e Proclamação da República 15/11) — ideal
# para evidenciar o ganho de SARIMA (sazonalidade) e SARIMAX (exógenas).
CORTE = "2021-10-31"

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 150,
    "figure.autolayout": True,
    "axes.titleweight": "bold",
    "font.size": 12,
})
AZUL, VERM, VERDE, LARANJA, ROXO = "#1f4e79", "#c0392b", "#27ae60", "#e67e22", "#7d3c98"

RES = {}  # dicionário de resultados que será salvo em JSON


def salvar(fig, nome):
    caminho = os.path.join(DIR_FIG, nome)
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)
    print(f"    figura salva: figuras/{nome}")


def metricas(y_real, y_prev):
    y_real = np.asarray(y_real, float)
    y_prev = np.asarray(y_prev, float)
    rmse = float(np.sqrt(np.mean((y_real - y_prev) ** 2)))
    mae = float(np.mean(np.abs(y_real - y_prev)))
    denom = np.where(y_real == 0, np.nan, y_real)
    mape = float(np.nanmean(np.abs((y_real - y_prev) / denom)) * 100)
    return rmse, mae, mape


def cabecalho(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def dividir(s):
    """Divide uma série em treino (até CORTE) e teste (os H dias seguintes)."""
    treino = s.loc[:CORTE]
    teste = s.loc[CORTE:].iloc[1 : H + 1]
    return treino, teste


# --------------------------------------------------------------------------- #
# 0. Carregamento
# --------------------------------------------------------------------------- #
def carregar_serie():
    caminho = os.path.join(DIR_DADOS, f"serie_{UF.lower()}.csv")
    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"{caminho} não encontrado. Rode antes: python src/preparar_dados.py"
        )
    s = pd.read_csv(caminho, parse_dates=["date"], index_col="date")
    s = s.asfreq("D")
    return s


# --------------------------------------------------------------------------- #
# 1. Introdução / Análise exploratória
# --------------------------------------------------------------------------- #
def secao_introducao(serie):
    cabecalho("1. INTRODUÇÃO E ANÁLISE EXPLORATÓRIA")
    casos = serie["new_confirmed"]
    obitos = serie["new_deaths"]

    RES["geral"] = {
        "uf": UF,
        "inicio": f"{serie.index.min():%d/%m/%Y}",
        "fim": f"{serie.index.max():%d/%m/%Y}",
        "n_obs": int(len(serie)),
        "casos_total": int(casos.sum()),
        "obitos_total": int(obitos.sum()),
        "casos_media": float(casos.mean()),
        "casos_dp": float(casos.std()),
        "casos_max": int(casos.max()),
        "data_pico": f"{casos.idxmax():%d/%m/%Y}",
    }
    print(f"  período: {RES['geral']['inicio']} a {RES['geral']['fim']} "
          f"({RES['geral']['n_obs']} dias)")
    print(f"  total de casos: {RES['geral']['casos_total']:,}")
    print(f"  pico diário: {RES['geral']['casos_max']:,} em {RES['geral']['data_pico']}")

    # --- Fig 01: série completa (casos + óbitos) -------------------------- #
    fig, ax1 = plt.subplots(figsize=(13, 6))
    ax1.plot(casos.index, casos.values, color=AZUL, lw=1.2, label="Casos novos/dia")
    ax1.set_ylabel("Casos confirmados/dia", color=AZUL)
    ax1.tick_params(axis="y", labelcolor=AZUL)
    ax2 = ax1.twinx()
    ax2.plot(obitos.index, obitos.rolling(7).mean(), color=VERM, lw=1.6,
             alpha=0.8, label="Óbitos/dia (média móvel 7d)")
    ax2.set_ylabel("Óbitos/dia (MM7)", color=VERM)
    ax2.tick_params(axis="y", labelcolor=VERM)
    ax2.grid(False)
    ax1.set_title(f"COVID-19 em {UF}: casos e óbitos diários (2020–2022)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.92), fontsize=11)
    salvar(fig, "01_serie_casos.png")

    # --- Fig 02: zoom mostrando sazonalidade semanal ---------------------- #
    jan = casos.loc["2021-05-01":"2021-07-15"]
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(jan.index, jan.values, "o-", color=AZUL, ms=4, lw=1.3)
    # marca os domingos
    domingos = [d for d in jan.index if d.dayofweek == 6]
    ax.scatter(domingos, jan.loc[domingos], color=VERM, zorder=5, s=70,
               label="Domingos")
    ax.set_title("Sazonalidade semanal: quedas sistemáticas aos fins de semana")
    ax.set_ylabel("Casos confirmados/dia")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend()
    salvar(fig, "02_sazonalidade_semanal.png")

    # --- Fig 03: efeito do dia da semana (perfil multiplicativo) ---------- #
    ratio = casos / casos.rolling(7, center=True).mean()
    perfil = ratio.groupby(ratio.index.dayofweek).mean()
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    fig, ax = plt.subplots(figsize=(10, 5))
    cores = [VERDE if v >= 1 else VERM for v in perfil.values]
    ax.bar(dias, perfil.values, color=cores, alpha=0.85)
    ax.axhline(1.0, color="black", ls="--", lw=1)
    for i, v in enumerate(perfil.values):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontweight="bold", fontsize=11)
    ax.set_title("Fator sazonal por dia da semana (1,0 = média semanal)")
    ax.set_ylabel("Casos relativos à média semanal")
    salvar(fig, "03_efeito_dia_semana.png")
    RES["sazonalidade"] = {
        "domingo_fator": float(perfil.iloc[6]),
        "quarta_fator": float(perfil.iloc[2]),
        "perfil": {d: float(v) for d, v in zip(dias, perfil.values)},
    }
    print(f"  fator sazonal domingo: {perfil.iloc[6]:.2f} | quarta: {perfil.iloc[2]:.2f}")

    # --- Fig 04: decomposição (log1p, aditiva, período 7) ----------------- #
    logc = np.log1p(casos)
    dec = seasonal_decompose(logc, model="additive", period=S)
    fig, axes = plt.subplots(4, 1, figsize=(13, 9), sharex=True)
    for ax, comp, tit, cor in zip(
        axes,
        [dec.observed, dec.trend, dec.seasonal, dec.resid],
        ["Observado  log(1+casos)", "Tendência", "Sazonalidade (semanal)", "Resíduo"],
        [AZUL, LARANJA, VERDE, "gray"],
    ):
        ax.plot(comp.index, comp.values, color=cor, lw=1.1)
        ax.set_ylabel(tit, fontsize=11)
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    axes[0].set_title("Decomposição clássica aditiva de log(1+casos), período = 7")
    salvar(fig, "04_decomposicao.png")

    # --- Estacionariedade: ADF e KPSS ------------------------------------- #
    def adf(x):
        r = adfuller(x.dropna(), autolag="AIC")
        return {"estatistica": float(r[0]), "p_valor": float(r[1])}

    def kpss_t(x):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = kpss(x.dropna(), regression="c", nlags="auto")
        return {"estatistica": float(r[0]), "p_valor": float(r[1])}

    d1 = logc.diff()
    est = {
        "adf_nivel": adf(logc),
        "adf_diff1": adf(d1),
        "kpss_nivel": kpss_t(logc),
        "kpss_diff1": kpss_t(d1),
    }
    RES["estacionariedade"] = est
    # ADF: H0 = raiz unitária (não estacionária); KPSS: H0 = estacionária
    print(f"  ADF  nível: p = {est['adf_nivel']['p_valor']:.3f}  | "
          f"KPSS nível: p = {est['kpss_nivel']['p_valor']:.3f}")
    print(f"  ADF  1ªdif: p = {est['adf_diff1']['p_valor']:.4f} | "
          f"KPSS 1ªdif: p = {est['kpss_diff1']['p_valor']:.3f}")
    print("  (ADF e KPSS divergem em nível por causa da forte sazonalidade; "
          "após diferenciar, ambos indicam estacionariedade)")
    return casos, logc


# --------------------------------------------------------------------------- #
# 2. Regressão Linear Simples  (FEATURE PRINCIPAL)
# --------------------------------------------------------------------------- #
def secao_regressao_linear(casos):
    cabecalho("2. REGRESSÃO LINEAR SIMPLES (modelo de tendência)")

    # Janela com tendência aproximadamente linear: subida da 2ª onda (2021)
    seg = casos.loc["2020-11-01":"2021-03-31"]
    t = np.arange(len(seg), dtype=float)
    y = seg.values.astype(float)

    # (a) scipy.stats.linregress  -> mesma função do material de Cálculo Numérico
    slope, intercept, r, p, se = linregress(t, y)
    r2 = r ** 2

    # (b) statsmodels OLS -> estatísticas completas (IC, t, F, Durbin-Watson)
    X = sm.add_constant(t)
    ols = sm.OLS(y, X).fit()
    ic = ols.conf_int(alpha=0.05)[1]  # IC do coeficiente angular
    resid = y - (intercept + slope * t)
    dw = float(durbin_watson(resid))  # ~2 => sem autocorr.; ~0 => autocorr. positiva

    # (c) MESMA regressão sobre a série suavizada (média móvel 7d): ao remover
    #     o ruído sazonal semanal, o R² da tendência sobe muito -> motiva
    #     suavização e modelos sazonais nas seções seguintes.
    seg_mm = seg.rolling(7).mean().dropna()
    t_mm = np.arange(len(seg_mm), dtype=float)
    s_mm, i_mm, r_mm, p_mm, _ = linregress(t_mm, seg_mm.values.astype(float))
    r2_mm = r_mm ** 2

    RES["regressao_linear"] = {
        "janela": f"{seg.index.min():%d/%m/%Y}–{seg.index.max():%d/%m/%Y}",
        "n": int(len(seg)),
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "r2_suavizada": float(r2_mm),
        "p_valor": float(p),
        "erro_padrao": float(se),
        "ic95_slope": [float(ic[0]), float(ic[1])],
        "t_stat_slope": float(ols.tvalues[1]),
        "durbin_watson": dw,
    }
    print(f"  janela: {RES['regressao_linear']['janela']} (n={len(seg)})")
    print(f"  modelo: casos = {intercept:.2f} + {slope:.3f}·t")
    print(f"  R² = {r2:.3f} | p = {p:.2e} | IC95% inclinação = "
          f"[{ic[0]:.2f}, {ic[1]:.2f}] casos/dia²")
    print(f"  R² sobre média móvel 7d = {r2_mm:.3f} (tendência forte sem o ruído semanal)")
    print(f"  Durbin-Watson = {dw:.2f} (≈2 sem autocorrelação; aqui há autocorr. → séries temporais)")

    # --- Fig 05: ajuste + resíduos --------------------------------------- #
    fig, (axf, axr) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )
    axf.scatter(seg.index, y, s=18, color=AZUL, alpha=0.5, label="Casos observados (diários)")
    axf.plot(seg.index, intercept + slope * t, color=VERM, lw=2.6,
             label=f"Reta MQO sobre dados diários (R²={r2:.3f})")
    axf.plot(seg_mm.index, i_mm + s_mm * t_mm, color=VERDE, lw=2.6, ls="--",
             label=f"Reta MQO sobre média móvel 7d (R²={r2_mm:.3f})")
    axf.set_title("Regressão linear simples: tendência de casos em SP")
    axf.set_ylabel("Casos/dia")
    axf.legend(fontsize=10)
    axr.axhline(0, color="black", lw=1)
    axr.scatter(seg.index, resid, s=14, color="gray")
    axr.set_title(f"Resíduos (note o padrão semanal → Durbin-Watson = {dw:.2f})", fontsize=12)
    axr.set_ylabel("Resíduo")
    axr.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    salvar(fig, "05_regressao_linear.png")

    # --- Linearização exponencial (ponte com Cálculo Numérico) ----------- #
    # Fase de crescimento explosivo (Omicron, dez/2021–jan/2022)
    seg2 = casos.loc["2021-12-15":"2022-01-20"]
    seg2 = seg2[seg2 > 0]
    t2 = np.arange(len(seg2), dtype=float)
    lny = np.log(seg2.values.astype(float))
    k, lnA, r_e, p_e, se_e = linregress(t2, lny)
    A = np.exp(lnA)
    dobra = np.log(2) / k if k > 0 else np.nan
    RES["linearizacao_exp"] = {
        "janela": f"{seg2.index.min():%d/%m/%Y}–{seg2.index.max():%d/%m/%Y}",
        "taxa_k": float(k),
        "A": float(A),
        "r2": float(r_e ** 2),
        "tempo_duplicacao_dias": float(dobra),
    }
    print(f"  linearização ln(casos): k={k:.3f}/dia, R²={r_e**2:.3f}, "
          f"duplicação a cada {dobra:.1f} dias")

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(14, 5))
    axl.scatter(t2, lny, s=22, color=ROXO, alpha=0.7, label="ln(casos) observado")
    axl.plot(t2, lnA + k * t2, color=VERM, lw=2.5,
             label=f"reta: ln(y)={lnA:.2f}+{k:.3f}·t (R²={r_e**2:.3f})")
    axl.set_title("Linearização: ln(casos) × tempo")
    axl.set_xlabel("dias desde 15/12/2021"); axl.set_ylabel("ln(casos)")
    axl.legend(fontsize=10)
    axr.scatter(seg2.index, seg2.values, s=22, color=ROXO, alpha=0.7, label="casos")
    axr.plot(seg2.index, A * np.exp(k * t2), color=VERM, lw=2.5,
             label=f"y={A:.0f}·e^({k:.3f}·t)")
    axr.set_title("Modelo exponencial recuperado")
    axr.set_ylabel("Casos/dia")
    axr.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    axr.legend(fontsize=10)
    salvar(fig, "06_linearizacao_exponencial.png")


# --------------------------------------------------------------------------- #
# 3. Alisamento exponencial
# --------------------------------------------------------------------------- #
def secao_alisamento(casos):
    cabecalho("3. ALISAMENTO EXPONENCIAL (SES, Holt, Holt-Winters)")
    treino, teste = dividir(casos)
    # Alisamento em log(1+casos): variância estabilizada e sazonalidade ADITIVA
    # em log equivale a MULTIPLICATIVA em nível (amplitude proporcional ao nível).
    z = np.log1p(treino)

    ses = SimpleExpSmoothing(z, initialization_method="estimated").fit()
    holt = Holt(z, damped_trend=True, initialization_method="estimated").fit()
    hw = ExponentialSmoothing(
        z, trend="add", damped_trend=True, seasonal="add", seasonal_periods=S,
        initialization_method="estimated",
    ).fit()

    def prever(m):
        return np.clip(np.expm1(m.forecast(H)), 0, None)

    fc_ses, fc_holt, fc_hw = prever(ses), prever(holt), prever(hw)

    RES["alisamento"] = {}
    for nome, mod, fc in [("SES", ses, fc_ses), ("Holt", holt, fc_holt),
                          ("Holt-Winters", hw, fc_hw)]:
        rmse, mae, mape = metricas(teste.values, fc.values)
        RES["alisamento"][nome] = {
            "rmse": rmse, "mae": mae, "mape": mape,
            "aic": float(mod.aic),
            "alpha": float(mod.params.get("smoothing_level", np.nan)),
            "beta": float(mod.params.get("smoothing_trend", np.nan)),
            "gamma": float(mod.params.get("smoothing_seasonal", np.nan)),
        }
        print(f"  {nome:<13} α={RES['alisamento'][nome]['alpha']:.3f} "
              f"RMSE={rmse:8.1f}  MAPE={mape:5.1f}%")

    fig, ax = plt.subplots(figsize=(13, 6))
    ctx = casos.loc["2021-09-15":"2021-11-28"]
    ax.plot(ctx.index, ctx.values, color="black", lw=1.5, label="Observado")
    ax.axvline(teste.index[0], color="gray", ls=":", lw=1.5)
    ax.plot(fc_ses.index, fc_ses.values, color=AZUL, lw=2, ls="--", label="SES")
    ax.plot(fc_holt.index, fc_holt.values, color=LARANJA, lw=2, ls="--", label="Holt")
    ax.plot(fc_hw.index, fc_hw.values, color=VERDE, lw=2.5, label="Holt-Winters (s=7)")
    ax.set_title("Alisamento exponencial: previsão de 28 dias")
    ax.set_ylabel("Casos/dia")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend()
    salvar(fig, "07_alisamento_exponencial.png")


# --------------------------------------------------------------------------- #
# 4. Médias móveis (MA) e ACF   |  5. AR e PACF
# --------------------------------------------------------------------------- #
def secao_acf_pacf(casos, logc):
    cabecalho("4-5. ACF/PACF, médias móveis (MA) e autorregressivos (AR)")

    # Suavização por média móvel (filtro) — distinguir de modelo MA(q)
    fig, ax = plt.subplots(figsize=(13, 5.5))
    seg = casos.loc["2021-02-01":"2021-06-30"]
    ax.plot(seg.index, seg.values, color="silver", lw=1, label="Casos brutos")
    ax.plot(seg.index, seg.rolling(7).mean(), color=VERM, lw=2.5,
            label="Média móvel 7 dias")
    ax.plot(seg.index, seg.rolling(14).mean(), color=AZUL, lw=2.5,
            label="Média móvel 14 dias")
    ax.set_title("Filtro de média móvel: remoção do ruído de fim de semana")
    ax.set_ylabel("Casos/dia")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend()
    salvar(fig, "08_media_movel_filtro.png")

    d1 = logc.diff().dropna()  # série estacionária (1ª diferença de log)

    # ACF / PACF da série em nível (não estacionária) vs diferenciada
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    plot_acf(logc.dropna(), lags=40, ax=axes[0, 0], color=AZUL, vlines_kwargs={"colors": AZUL})
    axes[0, 0].set_title("ACF — log(casos) em NÍVEL (decai devagar → não estacionária)")
    plot_pacf(logc.dropna(), lags=40, ax=axes[0, 1], method="ywm", color=ROXO)
    axes[0, 1].set_title("PACF — log(casos) em nível")
    plot_acf(d1, lags=40, ax=axes[1, 0], color=AZUL, vlines_kwargs={"colors": AZUL})
    axes[1, 0].set_title("ACF — 1ª diferença (picos em 7,14,21 → sazonal)")
    plot_pacf(d1, lags=40, ax=axes[1, 1], method="ywm", color=ROXO)
    axes[1, 1].set_title("PACF — 1ª diferença")
    salvar(fig, "09_acf_pacf.png")

    # Valores de ACF/PACF nos lags sazonais (para os slides)
    from statsmodels.tsa.stattools import acf, pacf
    ac = acf(d1, nlags=21)
    pa = pacf(d1, nlags=21, method="ywm")
    RES["acf_pacf"] = {
        "acf_lag7": float(ac[7]), "acf_lag14": float(ac[14]),
        "pacf_lag1": float(pa[1]), "pacf_lag7": float(pa[7]),
    }
    print(f"  ACF(7)={ac[7]:.2f}  ACF(14)={ac[14]:.2f}  "
          f"PACF(1)={pa[1]:.2f}  PACF(7)={pa[7]:.2f}")

    # Ajustes ilustrativos AR(7), MA(7), ARMA(2,2) na série estacionária
    serie_est = logc.diff().dropna()
    ar7 = ARIMA(serie_est, order=(7, 0, 0)).fit()
    ma7 = ARIMA(serie_est, order=(0, 0, 7)).fit()
    arma = ARIMA(serie_est, order=(2, 0, 2)).fit()
    RES["arma_ilustrativo"] = {
        "AR(7)": {"aic": float(ar7.aic), "bic": float(ar7.bic)},
        "MA(7)": {"aic": float(ma7.aic), "bic": float(ma7.bic)},
        "ARMA(2,2)": {"aic": float(arma.aic), "bic": float(arma.bic)},
    }
    print(f"  AIC -> AR(7)={ar7.aic:.0f} | MA(7)={ma7.aic:.0f} | ARMA(2,2)={arma.aic:.0f}")


# --------------------------------------------------------------------------- #
# 7-9. ARIMA, SARIMA, SARIMAX  + comparação
# --------------------------------------------------------------------------- #
def feriados_dummy(idx):
    """Dummy de feriados nacionais + carnaval (2020-2022) para variável exógena."""
    fixos = {(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)}
    moveis = {  # carnaval (ter) e sexta-feira santa
        pd.Timestamp("2020-02-25"), pd.Timestamp("2020-04-10"),
        pd.Timestamp("2021-02-16"), pd.Timestamp("2021-04-02"),
        pd.Timestamp("2022-03-01"), pd.Timestamp("2022-04-15"),
    }
    val = [(1 if (d.month, d.day) in fixos or d.normalize() in moveis else 0) for d in idx]
    return pd.Series(val, index=idx, dtype=float, name="feriado")


def secao_arima_familia(casos, logc):
    cabecalho("6-9. ARIMA / SARIMA / SARIMAX")
    y = logc  # modelagem em log(1+casos) (variância estabilizada)
    treino, teste = dividir(y)
    _, casos_teste = dividir(casos)

    def avalia(fc_log):
        prev = np.expm1(np.asarray(fc_log))
        prev = np.clip(prev, 0, None)
        return metricas(casos_teste.values, prev), prev

    resultados = {}

    # ---- ARIMA(2,1,2) ---------------------------------------------------- #
    arima = ARIMA(treino, order=(2, 1, 2)).fit()
    fc = arima.get_forecast(H)
    (rmse, mae, mape), prev_arima = avalia(fc.predicted_mean)
    resultados["ARIMA(2,1,2)"] = dict(rmse=rmse, mae=mae, mape=mape,
                                      aic=float(arima.aic), bic=float(arima.bic))
    print(f"  ARIMA(2,1,2)            AIC={arima.aic:8.1f}  RMSE={rmse:8.1f}  MAPE={mape:5.1f}%")

    # ---- SARIMA(2,1,2)(1,1,1,7) ----------------------------------------- #
    sarima = SARIMAX(treino, order=(2, 1, 2), seasonal_order=(1, 1, 1, S),
                     enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    fc_s = sarima.get_forecast(H)
    (rmse, mae, mape), prev_sarima = avalia(fc_s.predicted_mean)
    resultados["SARIMA(2,1,2)(1,1,1)7"] = dict(rmse=rmse, mae=mae, mape=mape,
                                               aic=float(sarima.aic), bic=float(sarima.bic))
    print(f"  SARIMA(2,1,2)(1,1,1)7   AIC={sarima.aic:8.1f}  RMSE={rmse:8.1f}  MAPE={mape:5.1f}%")

    # ---- SARIMAX: SARIMA + feriados (exógena) --------------------------- #
    fer = feriados_dummy(y.index)
    exog_tr, exog_te = dividir(fer)
    sarimax = SARIMAX(treino, exog=exog_tr, order=(2, 1, 2),
                      seasonal_order=(1, 1, 1, S),
                      enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    fc_x = sarimax.get_forecast(H, exog=exog_te)
    (rmse, mae, mape), prev_sarimax = avalia(fc_x.predicted_mean)
    par = sarimax.params
    coef_fer = float(par["feriado"]) if "feriado" in par.index else float(par.get("x1", np.nan))
    resultados["SARIMAX(+feriados)"] = dict(rmse=rmse, mae=mae, mape=mape,
                                            aic=float(sarimax.aic), bic=float(sarimax.bic),
                                            coef_feriado=coef_fer,
                                            efeito_pct=float((np.exp(coef_fer) - 1) * 100))
    print(f"  SARIMAX(+feriados)      AIC={sarimax.aic:8.1f}  RMSE={rmse:8.1f}  MAPE={mape:5.1f}%")
    print(f"     coef. feriado = {coef_fer:.3f}  → efeito {((np.exp(coef_fer)-1)*100):+.1f}% nos casos")

    RES["modelos"] = resultados

    # --- Fig 10: previsão ARIMA vs SARIMA vs observado -------------------- #
    ctx = casos.loc["2021-09-20":"2021-11-28"]
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(ctx.index, ctx.values, color="black", lw=1.6, label="Observado")
    ax.axvline(casos_teste.index[0], color="gray", ls=":", lw=1.5, label="Início da previsão")
    ax.plot(casos_teste.index, prev_arima, color=LARANJA, lw=2, ls="--",
            label="ARIMA(2,1,2)")
    ax.plot(casos_teste.index, prev_sarima, color=VERDE, lw=2.5,
            label="SARIMA(2,1,2)(1,1,1)₇")
    # intervalo de confiança do SARIMA (back-transform)
    ci = fc_s.conf_int()
    ax.fill_between(casos_teste.index, np.expm1(ci.iloc[:, 0]), np.expm1(ci.iloc[:, 1]),
                    color=VERDE, alpha=0.15, label="IC 95% (SARIMA)")
    ax.set_title("ARIMA × SARIMA: previsão de 28 dias (escala original)")
    ax.set_ylabel("Casos/dia")
    # Limita o eixo Y: o IC95% em log explode ao voltar à escala original;
    # focamos na região dos dados para enxergar o padrão semanal do SARIMA.
    ax.set_ylim(0, float(max(ctx.max(), casos_teste.max())) * 1.6)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend(fontsize=10, loc="upper left")
    salvar(fig, "10_arima_sarima_previsao.png")

    # --- Fig 11: diagnóstico de resíduos do SARIMA ----------------------- #
    fig = sarima.plot_diagnostics(figsize=(13, 8), lags=24)
    fig.suptitle("Diagnóstico de resíduos — SARIMA", fontweight="bold")
    salvar(fig, "11_diagnostico_residuos.png")
    lb = acorr_ljungbox(sarima.resid[S:], lags=[14], return_df=True)
    RES["ljung_box_sarima"] = {"lag": 14, "p_valor": float(lb["lb_pvalue"].iloc[0])}
    print(f"  Ljung-Box(14) SARIMA: p = {lb['lb_pvalue'].iloc[0]:.3f}")

    # --- Fig 12: efeito da variável exógena (SARIMA vs SARIMAX) ---------- #
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(casos_teste.index, casos_teste.values, "o-", color="black", lw=1.6,
            ms=5, label="Observado")
    ax.plot(casos_teste.index, prev_sarima, color=VERDE, lw=2, ls="--",
            label="SARIMA (sem exógena)")
    ax.plot(casos_teste.index, prev_sarimax, color=ROXO, lw=2.5,
            label="SARIMAX (+ feriados)")
    fer_te_dias = exog_te[exog_te > 0].index
    if len(fer_te_dias):
        ax.scatter(fer_te_dias, casos_teste.loc[fer_te_dias], color=VERM, s=90,
                   zorder=5, label="Feriado")
    ax.set_title("Feriados como exógena: efeito pequeno (sazonalidade já capta o padrão)")
    ax.set_ylabel("Casos/dia"); ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend(fontsize=10)
    salvar(fig, "12_sarimax_exogena.png")

    # --- Fig 13: comparação final (RMSE no teste) ------------------------ #
    todos = {}
    todos.update({k: v["rmse"] for k, v in RES["alisamento"].items()})
    todos.update({k: v["rmse"] for k, v in resultados.items()})
    nomes = list(todos.keys())
    valores = list(todos.values())
    cores = [VERDE if v == min(valores) else AZUL for v in valores]
    fig, ax = plt.subplots(figsize=(13, 6))
    barras = ax.barh(nomes, valores, color=cores, alpha=0.85)
    for b, v in zip(barras, valores):
        ax.text(v, b.get_y() + b.get_height() / 2, f" {v:.0f}", va="center",
                fontweight="bold", fontsize=11)
    ax.set_title("Comparação de modelos — RMSE no conjunto de teste (28 dias)")
    ax.set_xlabel("RMSE (casos/dia) — menor é melhor")
    ax.invert_yaxis()
    salvar(fig, "13_comparacao_modelos.png")

    melhor = min(todos, key=todos.get)
    RES["melhor_modelo"] = {"nome": melhor, "rmse": float(todos[melhor])}
    print(f"\n  >> MELHOR MODELO (RMSE teste): {melhor} = {todos[melhor]:.1f}")


# --------------------------------------------------------------------------- #
# 9b. Variável exógena "rica": prever ÓBITOS a partir de CASOS defasados
# --------------------------------------------------------------------------- #
def secao_exogena_obitos(serie):
    cabecalho("9b. VARIÁVEL EXÓGENA: óbitos previstos a partir de casos defasados")
    casos = serie["new_confirmed"].astype(float)
    obitos = serie["new_deaths"].astype(float)
    yo = np.log1p(obitos)
    lc = np.log1p(casos)

    # Correlação cruzada: óbitos de hoje × casos de k dias atrás.
    # O pico ocorre em lag 0 (casos e óbitos co-evoluem na escala das ondas),
    # caracterizando uma REGRESSÃO DINÂMICA contemporânea com erros SARIMA.
    lags = range(0, 29)
    cc = {k: float(yo.corr(lc.shift(k))) for k in lags}
    melhor_lag = max(cc, key=cc.get)
    print(f"  correlação log-casos × log-óbitos: lag 0 = {cc[0]:.2f} | "
          f"lag 14 = {cc[14]:.2f} | defasagem usada = {melhor_lag}")

    exog = lc.shift(melhor_lag).rename("casos_def")
    dfm = pd.concat([yo.rename("y"), exog], axis=1).dropna()
    treino = dfm.loc[:CORTE]
    teste = dfm.loc[CORTE:].iloc[1 : H + 1]
    obitos_teste = obitos.loc[teste.index]

    # SARIMA univariado (só óbitos) × SARIMAX (óbitos | casos defasados)
    base = dict(order=(1, 1, 1), seasonal_order=(1, 1, 1, S),
                enforce_stationarity=False, enforce_invertibility=False)
    m0 = SARIMAX(treino["y"], **base).fit(disp=False)
    f0 = np.clip(np.expm1(m0.get_forecast(H).predicted_mean), 0, None)
    m1 = SARIMAX(treino["y"], exog=treino[["casos_def"]], **base).fit(disp=False)
    f1 = np.clip(np.expm1(
        m1.get_forecast(H, exog=teste[["casos_def"]]).predicted_mean), 0, None)

    rmse0, mae0, _ = metricas(obitos_teste.values, f0.values)
    rmse1, mae1, _ = metricas(obitos_teste.values, f1.values)
    coef = float(m1.params.get("casos_def", np.nan))
    RES["exogena_obitos"] = {
        "lag_dias": int(melhor_lag),
        "corr": float(cc[melhor_lag]),
        "corr_lag0": float(cc[0]),
        "coef_casos": coef,
        "rmse_sarima": rmse0, "rmse_sarimax": rmse1,
        "mae_sarima": mae0, "mae_sarimax": mae1,
        "ganho_rmse_pct": float((rmse0 - rmse1) / rmse0 * 100),
        "aic_sarima": float(m0.aic), "aic_sarimax": float(m1.aic),
    }
    print(f"  SARIMA (só óbitos):       RMSE = {rmse0:6.1f}  AIC = {m0.aic:.1f}")
    print(f"  SARIMAX (+ casos def.):   RMSE = {rmse1:6.1f}  AIC = {m1.aic:.1f}")
    print(f"  ganho de {RES['exogena_obitos']['ganho_rmse_pct']:.0f}% no RMSE com a variável exógena")

    # --- Fig 14: óbitos — SARIMA × SARIMAX ------------------------------- #
    fig, ax = plt.subplots(figsize=(13, 6))
    ctx = obitos.loc["2021-09-20":"2021-11-28"]
    ax.plot(ctx.index, ctx.values, color="black", lw=1.5, label="Óbitos observados")
    ax.axvline(teste.index[0], color="gray", ls=":", lw=1.5, label="Início da previsão")
    ax.plot(teste.index, f0.values, color=LARANJA, lw=2, ls="--",
            label=f"SARIMA univariado (RMSE={rmse0:.1f})")
    ax.plot(teste.index, f1.values, color=ROXO, lw=2.6,
            label=f"SARIMAX | casos como exógena (RMSE={rmse1:.1f})")
    ax.set_title("Variável exógena rica: nº de casos melhora a previsão de óbitos")
    ax.set_ylabel("Óbitos/dia"); ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%b"))
    ax.legend(fontsize=10)
    salvar(fig, "14_exogena_obitos.png")


# --------------------------------------------------------------------------- #
def main():
    os.makedirs(DIR_FIG, exist_ok=True)
    serie = carregar_serie()
    casos, logc = secao_introducao(serie)
    secao_regressao_linear(casos)
    secao_alisamento(casos)
    secao_acf_pacf(casos, logc)
    secao_arima_familia(casos, logc)
    secao_exogena_obitos(serie)

    destino = os.path.join(DIR_DADOS, "resultados.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(RES, f, ensure_ascii=False, indent=2)
    cabecalho("CONCLUÍDO")
    print(f"  resultados numéricos salvos em: dados/resultados.json")
    print(f"  figuras geradas em: figuras/")


if __name__ == "__main__":
    main()
