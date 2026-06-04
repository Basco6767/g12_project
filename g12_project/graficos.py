# -*- coding: utf-8 -*-
"""
graficos.py — Geração de gráficos com Matplotlib (Fase 2, passo 3).

Construído por cima do analise.py. Módulo isolado, independente da web.
Cada função devolve uma imagem PNG codificada em base64, pronta a injetar
mais tarde num <img src="data:image/png;base64,..."> (quando existir interface).

Testar diretamente com:  python graficos.py
Isto gera ficheiros _preview_*.png que se podem abrir para confirmar
que os gráficos estão legíveis.
"""
import io
import base64

import matplotlib
matplotlib.use("Agg")  # backend sem GUI, essencial fora de ambiente gráfico
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import analise

# Paleta de cores dos gráficos
COR_PRIMARIA = "#2b6777"
COR_SECUNDARIA = "#c8a35b"
COR_FUNDO = "#f7f4ec"


def _fig_para_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def grafico_inscricoes_por_mes():
    """Série temporal mensal das inscrições (análise principal)."""
    serie = analise.memberships_per_month()

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(COR_FUNDO)
    ax.set_facecolor(COR_FUNDO)

    ax.plot(serie.index, serie.values, color=COR_PRIMARIA, linewidth=2)
    ax.fill_between(serie.index, serie.values, color=COR_PRIMARIA, alpha=0.12)

    ax.set_title("Inscrições em associações ao longo do tempo (mensal)",
                 fontsize=14, fontweight="bold", color="#222")
    ax.set_xlabel("Data")
    ax.set_ylabel("Nº de inscrições")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(True, alpha=0.25)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    return _fig_para_base64(fig)


def grafico_inscricoes_por_ano():
    """Barras: total de inscrições por ano."""
    serie = analise.memberships_per_year()

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(COR_FUNDO)
    ax.set_facecolor(COR_FUNDO)

    barras = ax.bar(serie.index.astype(str), serie.values,
                    color=COR_PRIMARIA, width=0.6)
    # destacar o ano de pico
    pico = serie.idxmax()
    for ano, barra in zip(serie.index, barras):
        if ano == pico:
            barra.set_color(COR_SECUNDARIA)
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() + max(serie.values) * 0.01,
                str(int(barra.get_height())),
                ha="center", va="bottom", fontsize=9, color="#444")

    ax.set_title("Inscrições por ano", fontsize=14, fontweight="bold", color="#222")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Nº de inscrições")
    ax.grid(True, axis="y", alpha=0.25)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    return _fig_para_base64(fig)


def grafico_receita_por_ano():
    """Barras: receita total (soma dos fees) por ano + linha do fee médio."""
    df = analise.fee_per_year()

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(COR_FUNDO)
    ax.set_facecolor(COR_FUNDO)

    anos = df.index.astype(str)
    ax.bar(anos, df["sum"], color=COR_PRIMARIA, width=0.6, label="Receita total")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Receita total (fees)", color=COR_PRIMARIA)
    ax.tick_params(axis="y", labelcolor=COR_PRIMARIA)

    ax2 = ax.twinx()
    ax2.plot(anos, df["mean"], color=COR_SECUNDARIA, marker="o",
             linewidth=2, label="Fee médio")
    ax2.set_ylabel("Fee médio", color=COR_SECUNDARIA)
    ax2.tick_params(axis="y", labelcolor=COR_SECUNDARIA)

    ax.set_title("Receita total e fee médio por ano",
                 fontsize=14, fontweight="bold", color="#222")
    for spine in ["top"]:
        ax.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)

    return _fig_para_base64(fig)


if __name__ == "__main__":
    # Teste manual: gera os três gráficos para ficheiro, para inspeção visual.
    for nome, func in [
        ("inscricoes_por_mes", grafico_inscricoes_por_mes),
        ("inscricoes_por_ano", grafico_inscricoes_por_ano),
        ("receita_por_ano", grafico_receita_por_ano),
    ]:
        data = func()
        ficheiro = f"_preview_{nome}.png"
        with open(ficheiro, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"Gerado {ficheiro} — abre o ficheiro para confirmar a legibilidade.")
