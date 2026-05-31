import streamlit as st
import plotly.express as px
import pandas as pd

from src.components import page_header, section, insight
from src.style import TEMPLATE, CORES, ESCALA_ROXA
def render(df: pd.DataFrame) -> None:
    page_header(
        "Por Cidade",
        "Comparativo e ranking entre cidades brasileiras"
    )
    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # ── Ranking Top 15 ────────────────────────────────────────────────────────
    section("Ranking de ocorrências por cidade (Top 15)")
    rank = (df.groupby("cidade")["ocorrencias"].sum()
            .reset_index()
            .sort_values("ocorrencias", ascending=False)
            .head(15))
    fig = px.bar(
        rank, x="cidade", y="ocorrencias",
        color="ocorrencias", color_continuous_scale=ESCALA_ROXA,
        text="ocorrencias",
    )
    fig.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13,
        marker_line_width=0,
    )
    fig.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=380, xaxis_tickangle=-35,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
        margin=dict(t=50, b=10, l=40, r=20),
        yaxis=dict(autorange=True),
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

    # ── Índice de violência ────────────────────────────────────────────────────
    section("Índice médio de violência (Top 10)")
    idx_cid = (df.groupby("cidade")["indice_violencia"].mean()
               .reset_index()
               .sort_values("indice_violencia", ascending=False)
               .head(10))
    fig2 = px.bar(
        idx_cid, x="indice_violencia", y="cidade", orientation="h",
        color="indice_violencia",
        color_continuous_scale=["#4c1d95", "#ef4444"],
        text=idx_cid["indice_violencia"].round(1),
    )
    fig2.update_traces(
        texttemplate="%{text:.1f}", textposition="outside",
        textfont_color="#cbd5e1", textfont_size=13,
        marker_line_width=0,
    )
    fig2.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=340,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
    )
    fig2.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "📊 Índice de violência: <b>%{x:.1f}</b><extra></extra>"
        ),
    )
    fig2.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displayModeBar": False})

    # ── Dispersão renda x violência ───────────────────────────────────────────
    section("Dispersão — renda média × índice de violência")
    disp = df.groupby("cidade").agg(
        renda_media=("renda_media", "mean"),
        indice_violencia=("indice_violencia", "mean"),
        ocorrencias=("ocorrencias", "sum"),
        regiao=("regiao", "first"),
    ).reset_index()

    fig3 = px.scatter(
        disp, x="renda_media", y="indice_violencia",
        size="ocorrencias", color="regiao", text="cidade",
        color_discrete_sequence=CORES, size_max=20,
    )
    fig3.update_traces(
        textposition="top center",
        textfont_size=13, textfont_color="#cbd5e1",
        marker=dict(line=dict(color="#0b0e17", width=1)),
    )
    fig3.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=380,
        xaxis_title="Renda média (R$)",
        yaxis_title="Índice de violência",
        legend=dict(font=dict(size=13, color="#cbd5e1")),
    )
    fig3.update_traces(
        hovertemplate=(
            "<b>%{text}</b><br>"
            "💰 Renda média: <b>R$ %{x:,.0f}</b><br>"
            "📊 Índice de violência: <b>%{y:.1f}</b><br>"
            "🚨 Ocorrências: <b>%{marker.size:,.0f}</b><extra></extra>"
        ),
    )
    fig3.update_layout(
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})

    insight("""
    <strong>Análise urbana:</strong> O gráfico de dispersão investiga a relação entre renda
    média e índice de violência. Cidades com menor renda tendem a apresentar índices mais
    elevados, mas há exceções relevantes que indicam a influência de outros fatores — como
    presença policial, urbanização e desigualdade interna.
    """)