import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.components import page_header, section, insight, kpi
from src.style import TEMPLATE, ESCALA_ROXA
def render(df: pd.DataFrame) -> None:
    page_header(
        "Visão Geral",
        "Panorama geral da criminalidade em grandes cidades brasileiras",
        badge="2015 – 2024",
        badge_extra="Atualizado"
    )
    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total_oc    = df["ocorrencias"].sum()
    total_vit   = df["vitimas"].sum()
    total_pris  = df["prisoes"].sum()
    idx_medio   = round(df["indice_violencia"].mean(), 1)
    cidade_crit = df.groupby("cidade")["ocorrencias"].sum().idxmax()
    crime_freq  = df.groupby("tipo_crime")["ocorrencias"].sum().idxmax()
    regiao_crit = df.groupby("regiao")["ocorrencias"].sum().idxmax()
    cidades_n   = df["cidade"].nunique()

    cols = st.columns(4)
    with cols[0]:
        kpi("Total de ocorrências", f"{total_oc:,}".replace(",", "."),
            sub=f"{cidades_n} cidades monitoradas", idx=0)
    with cols[1]:
        kpi("Total de vítimas", f"{total_vit:,}".replace(",", "."),
            sub="impacto social direto", idx=1)
    with cols[2]:
        kpi("Índice médio de violência", str(idx_medio),
            sub="média geral do período", idx=2)
    with cols[3]:
        kpi("Total de prisões", f"{total_pris:,}".replace(",", "."),
            sub="efetividade policial", idx=3)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    cols2 = st.columns(3)
    with cols2[0]:
        kpi("Cidade mais crítica", cidade_crit,
            sub="maior volume de ocorrências", idx=4)
    with cols2[1]:
        kpi("Crime mais frequente", crime_freq,
            sub="tipo de crime líder", idx=5)
    with cols2[2]:
        kpi("Região mais crítica", regiao_crit,
            sub="maior concentração regional", idx=0)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Linha anual ────────────────────────────────────────────────────────────
    section("Evolução anual — total de ocorrências")
    ev = df.groupby("ano")["ocorrencias"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ev["ano"], y=ev["ocorrencias"],
        mode="lines+markers",
        line=dict(color="#7c3aed", width=2.5),
        marker=dict(size=7, color="#a78bfa",
                    line=dict(color="#7c3aed", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(124,58,237,0.10)",
        name="Ocorrências",
    ))
    fig.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=260,
        xaxis_title="", yaxis_title="",
        xaxis=dict(tickvals=ev["ano"].tolist(), range=[ev["ano"].min() - 0.3, ev["ano"].max() + 0.3]),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>Ano %{x}</b><br>"
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

    # ── Donuts lado a lado ─────────────────────────────────────────────────────
    col_d1, col_d2 = st.columns(2)

    LEGEND_STYLE = dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", size=13),
        orientation="v",
        x=1.02, xanchor="left",
        y=0.5,  yanchor="middle",
    )

    with col_d1:
        section("Distribuição por nível de risco")
        ordem = ["Baixo", "Médio", "Alto", "Crítico"]
        nr = df.groupby("nivel_risco")["ocorrencias"].sum().reset_index()
        nr["nivel_risco"] = pd.Categorical(
            nr["nivel_risco"], categories=ordem, ordered=True)
        nr = nr.sort_values("nivel_risco")
        fig2 = px.pie(
            nr, values="ocorrencias", names="nivel_risco",
            color_discrete_sequence=["#4ade80", "#fbbf24", "#f97316", "#ef4444"],
            hole=0.55,
        )
        fig2.update_traces(
            textinfo="percent",
            textfont=dict(size=13, color="#1a1a2e", family="Google Sans Flex, sans-serif"),
            insidetextfont=dict(color="#1a1a2e", size=13),
            marker=dict(line=dict(color="#0b0e17", width=2)),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "🚨 Ocorrências: <b>%{value:,.0f}</b><br>"
                "📊 Participação: <b>%{percent}</b><extra></extra>"
            ),
        )
        fig2.update_layout(
            paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
            template=TEMPLATE, height=320,
            showlegend=True,
            legend=LEGEND_STYLE,
            margin=dict(l=20, r=120, t=20, b=20),
            hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
                font=dict(color="#e2e8f0", size=13,
                          family="Google Sans Flex, sans-serif"), align="left"),
        )
        st.plotly_chart(fig2, use_container_width=True,
                        config={"displayModeBar": False})

    with col_d2:
        section("Distribuição por tipo de crime")
        tc = (df.groupby("tipo_crime")["ocorrencias"].sum()
              .reset_index().sort_values("ocorrencias", ascending=False))
        CORES_CRIME = ["#ef4444", "#a78bfa", "#f472b6", "#4ade80",
                       "#22d3ee", "#fbbf24"]
        fig4 = px.pie(
            tc, values="ocorrencias", names="tipo_crime",
            color_discrete_sequence=CORES_CRIME,
            hole=0.55,
        )
        fig4.update_traces(
            textinfo="percent",
            textfont=dict(size=13, color="#1a1a2e", family="Google Sans Flex, sans-serif"),
            insidetextfont=dict(color="#1a1a2e", size=13),
            marker=dict(line=dict(color="#0b0e17", width=2)),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "🚨 Ocorrências: <b>%{value:,.0f}</b><br>"
                "📊 Participação: <b>%{percent}</b><extra></extra>"
            ),
        )
        fig4.update_layout(
            paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
            template=TEMPLATE, height=320,
            showlegend=True,
            legend=LEGEND_STYLE,
            margin=dict(l=20, r=140, t=20, b=20),
            hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
                font=dict(color="#e2e8f0", size=13,
                          family="Google Sans Flex, sans-serif"), align="left"),
        )
        st.plotly_chart(fig4, use_container_width=True,
                        config={"displayModeBar": False})

    # ── Barras região ──────────────────────────────────────────────────────────
    section("Ocorrências por região")
    reg = (df.groupby("regiao")["ocorrencias"].sum()
           .reset_index().sort_values("ocorrencias", ascending=False))
    fig3 = px.bar(
        reg, x="regiao", y="ocorrencias",
        color="ocorrencias", color_continuous_scale=ESCALA_ROXA,
        text="ocorrencias",
    )
    fig3.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13,
        marker_line_width=0,
    )
    fig3.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=280,
        coloraxis_showscale=False,
        xaxis_title="", yaxis_title="",
    )
    fig3.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "🚨 Ocorrências: <b>%{y:,.0f}</b><extra></extra>"
        ),
    )
    fig3.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})

    # ── Insight ────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    insight(f"""
    <strong>Interpretação:</strong> No período selecionado foram registradas
    <strong>{total_oc:,} ocorrências</strong> com <strong>{total_vit:,} vítimas</strong>.
    A região <strong>{regiao_crit}</strong> concentra o maior volume de crimes, enquanto
    <strong>{crime_freq}</strong> é o tipo mais frequente. O índice médio de violência é
    <strong>{idx_medio}</strong>, com <strong>{cidade_crit}</strong> liderando o ranking urbano.
    """.replace(",", "."))