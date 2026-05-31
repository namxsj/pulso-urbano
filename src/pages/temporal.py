import streamlit as st
import plotly.express as px
import pandas as pd

from src.components import page_header, section, insight
from src.style import TEMPLATE, CORES, ESCALA_CRIME
def render(df: pd.DataFrame) -> None:
    page_header(
        "Análise Temporal",
        "Evolução da criminalidade ao longo dos anos",
        badge="2015 – 2024"
    )
    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # ── Linha por tipo ─────────────────────────────────────────────────────────
    section("Ocorrências por ano e tipo de crime")
    ev2 = df.groupby(["ano", "tipo_crime"])["ocorrencias"].sum().reset_index()
    fig = px.line(
        ev2, x="ano", y="ocorrencias", color="tipo_crime",
        color_discrete_sequence=CORES, markers=True,
    )
    fig.update_traces(line_width=2, marker_size=6)
    fig.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=320,
        xaxis_title="", yaxis_title="",
        legend=dict(font=dict(size=13, color="#cbd5e1")),
        xaxis=dict(tickvals=sorted(df["ano"].unique())),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Ano: <b>%{x}</b><br>"
            "🚨 Ocorrências: <b>%{y:,.0f}</b><extra></extra>"
        ),
    )
    fig.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

    # ── Área por região ────────────────────────────────────────────────────────
    section("Ocorrências por ano e região")
    ev3 = df.groupby(["ano", "regiao"])["ocorrencias"].sum().reset_index()
    fig2 = px.area(
        ev3, x="ano", y="ocorrencias", color="regiao",
        color_discrete_sequence=CORES,
    )
    fig2.update_traces(line_width=1.5)
    fig2.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=320,
        xaxis_title="", yaxis_title="",
        legend=dict(font=dict(size=13, color="#cbd5e1")),
        xaxis=dict(tickvals=sorted(df["ano"].unique())),
    )
    fig2.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Ano: <b>%{x}</b><br>"
            "🚨 Ocorrências: <b>%{y:,.0f}</b><extra></extra>"
        ),
    )
    fig2.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displayModeBar": False})

    # ── Heatmap mês x ano ─────────────────────────────────────────────────────
    section("Heatmap — ocorrências por mês e ano")
    heat = df.groupby(["ano", "mes"])["ocorrencias"].sum().reset_index()
    heat_piv = heat.pivot(index="mes", columns="ano",
                          values="ocorrencias").fillna(0)
    meses_nome = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
    }
    heat_piv.index = [meses_nome[m] for m in heat_piv.index]
    fig3 = px.imshow(
        heat_piv,
        color_continuous_scale=ESCALA_CRIME,
        aspect="auto", text_auto=True,
    )
    # Force all year labels to show on x-axis
    anos_cols = [str(c) for c in heat_piv.columns]
    fig3.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=320,
        xaxis_title="", yaxis_title="",
        coloraxis_showscale=False,
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(anos_cols))),
            ticktext=anos_cols,
        ),
    )
    fig3.update_traces(
        textfont_size=13, textfont_color="#cbd5e1",
        hovertemplate=(
            "📅 <b>%{y} · %{x}</b><br>"
            "🚨 Ocorrências: <b>%{z:,.0f}</b><extra></extra>"
        ),
    )
    fig3.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})

    # ── Barras período do dia ─────────────────────────────────────────────────
    section("Período do dia mais crítico por ano")
    per = df.groupby(["ano", "periodo_dia"])["ocorrencias"].sum().reset_index()
    ordem_per = ["Madrugada", "Manhã", "Tarde", "Noite"]
    per["periodo_dia"] = pd.Categorical(
        per["periodo_dia"], categories=ordem_per, ordered=True)
    per = per.sort_values(["ano", "periodo_dia"])
    fig4 = px.bar(
        per, x="ano", y="ocorrencias", color="periodo_dia",
        barmode="group", color_discrete_sequence=CORES,
    )
    fig4.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=300,
        xaxis_title="", yaxis_title="",
        legend=dict(font=dict(size=13, color="#cbd5e1")),
        xaxis=dict(tickvals=sorted(df["ano"].unique())),
        bargap=0.15,
    )
    fig4.update_traces(
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Ano: <b>%{x}</b><br>"
            "🚨 Ocorrências: <b>%{y:,.0f}</b><extra></extra>"
        ),
    )
    fig4.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig4, use_container_width=True,
                    config={"displayModeBar": False})

    insight("""
    <strong>Interpretação temporal:</strong> O heatmap revela concentrações sazonais de
    criminalidade ao longo do período. A análise por período do dia permite identificar
    janelas de maior risco. Variações anuais refletem mudanças em políticas públicas,
    crises econômicas e fatores regionais específicos.
    """)