import streamlit as st
import plotly.express as px
import pandas as pd

from src.components import page_header, section, insight
from src.style import TEMPLATE, CORES, ESCALA_CRIME


def render(df: pd.DataFrame) -> None:
    page_header(
        "Por Crime",
        "Frequência, horários e padrões criminais"
    )

    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # Barras simples com o total de ocorrências por tipo de crime
    # Ordenado de forma decrescente pra deixar o mais frequente em primeiro
    section("Ocorrências por tipo de crime")
    tc = (df.groupby("tipo_crime")["ocorrencias"].sum()
          .reset_index()
          .sort_values("ocorrencias", ascending=False))
    fig = px.bar(
        tc, x="tipo_crime", y="ocorrencias",
        color="tipo_crime", color_discrete_sequence=CORES,
        text="ocorrencias",
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13,
        marker_line_width=0,
    )
    fig.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=340,
        xaxis_title="", yaxis_title="", showlegend=False,
        margin=dict(t=50, b=10, l=40, r=20),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
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

    # Heatmap cruzando tipo de crime com período do dia
    # pivot() gera a matriz necessária pro imshow(); fillna(0) evita erros no render
    section("Heatmap — crime × período do dia")
    hc = df.groupby(["tipo_crime", "periodo_dia"])["ocorrencias"].sum().reset_index()
    hc_piv = hc.pivot(
        index="tipo_crime", columns="periodo_dia", values="ocorrencias"
    ).fillna(0)
    # Reordena as colunas na sequência cronológica do dia
    ordem_per = [p for p in ["Madrugada", "Manhã", "Tarde", "Noite"]
                 if p in hc_piv.columns]
    hc_piv = hc_piv[ordem_per]
    fig2 = px.imshow(
        hc_piv,
        color_continuous_scale=ESCALA_CRIME,
        text_auto=True, aspect="auto",
    )
    fig2.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=300,
        xaxis_title="", yaxis_title="",
        coloraxis_showscale=False,
    )
    fig2.update_traces(
        textfont_size=13, textfont_color="#cbd5e1",
        hovertemplate=(
            "🔍 <b>%{y}</b><br>"
            "🕐 Período: <b>%{x}</b><br>"
            "🚨 Ocorrências: <b>%{z:,.0f}</b><extra></extra>"
        ),
    )
    fig2.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displayModeBar": False})

    # Barras horizontais de vítimas — ascending=True deixa o maior no topo do gráfico
    section("Vítimas por tipo de crime")
    vit = (df.groupby("tipo_crime")["vitimas"].sum()
           .reset_index()
           .sort_values("vitimas", ascending=True))
    fig3 = px.bar(
        vit, x="vitimas", y="tipo_crime", orientation="h",
        color="vitimas",
        color_continuous_scale=["#4c1d95", "#ef4444"],
        text="vitimas",
    )
    fig3.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13,
        marker_line_width=0,
    )
    fig3.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=300,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
    )
    fig3.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "🤕 Vítimas: <b>%{x:,.0f}</b><extra></extra>"
        ),
    )
    fig3.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})

    # Comparativo de prisões por crime: complementa a visão de vítimas
    # A diferença entre os dois gráficos revela a efetividade policial por modalidade
    section("Prisões por tipo de crime")
    pris = (df.groupby("tipo_crime")["prisoes"].sum()
            .reset_index()
            .sort_values("prisoes", ascending=True))
    fig4 = px.bar(
        pris, x="prisoes", y="tipo_crime", orientation="h",
        color="prisoes",
        color_continuous_scale=["#1e3a5f", "#22d3ee"],
        text="prisoes",
    )
    fig4.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13,
        marker_line_width=0,
    )
    fig4.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=300,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
    )
    fig4.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "🔒 Prisões: <b>%{x:,.0f}</b><extra></extra>"
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
    <strong>Padrões criminais:</strong> O heatmap revela quais tipos de crime predominam em
    cada período do dia. Roubos tendem a se concentrar no período noturno, enquanto furtos são
    mais distribuídos ao longo do dia. A relação entre ocorrências e prisões indica a
    efetividade das respostas policiais por modalidade criminal.
    """)
