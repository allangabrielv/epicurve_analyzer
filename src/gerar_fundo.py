# -*- coding: utf-8 -*-
"""
gerar_fundo.py
==============
Gera o fundo "pitch" do seminário: tela preta com silhuetas discretas de
coronavírus nas bordas (corpo cinza + espículas vermelho-escuras), evocando a
identidade visual do projeto EpiCurve Analyzer. Salvo em figuras/fundo_virus.png
para ser usado como background dos slides Beamer.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "figuras", "fundo_virus.png")

CINZA = "#343434"
VERM = "#6E1616"
VERM_KNOB = "#8E1C1C"


def desenhar_virus(ax, cx, cy, r, alpha, n_spikes=18):
    # corpo
    ax.add_patch(Circle((cx, cy), r, facecolor=CINZA, edgecolor="none", alpha=alpha, zorder=2))
    # textura interna (anel sutil)
    ax.add_patch(Circle((cx, cy), r * 0.62, facecolor="none",
                         edgecolor="#2A2A2A", lw=r * 2.2, alpha=alpha * 0.8, zorder=3))
    # espículas em forma de taça (haste + bolinha)
    for k in range(n_spikes):
        ang = 2 * np.pi * k / n_spikes
        x0, y0 = cx + r * np.cos(ang), cy + r * np.sin(ang)
        x1, y1 = cx + r * 1.27 * np.cos(ang), cy + r * 1.27 * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color=VERM, lw=r * 1.6, alpha=alpha, zorder=1,
                solid_capstyle="round")
        ax.add_patch(Circle((x1, y1), r * 0.085, facecolor=VERM_KNOB,
                            edgecolor="none", alpha=alpha, zorder=1))


def main():
    fig = plt.figure(figsize=(16, 9), dpi=120)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.add_patch(plt.Rectangle((0, 0), 16, 9, color="black", zorder=0))

    # (cx, cy, r, alpha) -- concentrados nas bordas; centro/topo-esquerdo livres
    virus = [
        (15.8, 8.6, 1.25, 0.42),
        (-0.2, 5.1, 1.05, 0.36),
        (16.4, 3.3, 1.15, 0.40),
        (1.4, -0.1, 1.30, 0.42),
        (7.6, -0.5, 1.35, 0.36),
        (13.1, 0.1, 1.05, 0.42),
        (11.0, 8.1, 0.62, 0.28),
        (4.6, 9.2, 0.9, 0.30),
    ]
    for (cx, cy, r, a) in virus:
        desenhar_virus(ax, cx, cy, r, a)

    fig.savefig(DESTINO, facecolor="black", dpi=120)
    plt.close(fig)
    print(f"fundo salvo em: {DESTINO}")


if __name__ == "__main__":
    main()
