import streamlit as st
import pandas as pd

from src.components import page_header, section, kpi
def render(df: pd.DataFrame) -> None:
    page_header(
        "🗃️ Explorador de Dados",
        "Tabela completa com os dados filtrados e estatísticas descritivas"
    )
    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # ── KPIs rápidos ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("Registros filtrados", f"{len(df):,}".replace(",", "."), idx=0)
    with c2:
        kpi("Cidades", str(df["cidade"].nunique()), idx=1)
    with c3:
        kpi("Anos cobertos", f"{df['ano'].min()} – {df['ano'].max()}", idx=2)
    with c4:
        kpi("Estados", str(df["uf"].nunique()), idx=3)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Tabela dinâmica ────────────────────────────────────────────────────────
    section("Tabela de dados")
    st.dataframe(
        df.sort_values(["ano", "mes", "cidade"]),
        use_container_width=True,
        height=420,
        column_config={
            "ano":              st.column_config.NumberColumn("Ano",               format="%d"),
            "mes":              st.column_config.NumberColumn("Mês",               format="%d"),
            "data":             st.column_config.TextColumn("Data"),
            "regiao":           st.column_config.TextColumn("Região"),
            "uf":               st.column_config.TextColumn("UF"),
            "cidade":           st.column_config.TextColumn("Cidade"),
            "bairro":           st.column_config.TextColumn("Bairro"),
            "tipo_crime":       st.column_config.TextColumn("Tipo de crime"),
            "periodo_dia":      st.column_config.TextColumn("Período"),
            "ocorrencias":      st.column_config.NumberColumn("Ocorrências",       format="%d"),
            "vitimas":          st.column_config.NumberColumn("Vítimas",           format="%d"),
            "prisoes":          st.column_config.NumberColumn("Prisões",           format="%d"),
            "renda_media":      st.column_config.NumberColumn("Renda média",       format="R$ %.2f"),
            "indice_violencia": st.column_config.NumberColumn("Índice violência",  format="%.1f"),
            "nivel_risco":      st.column_config.TextColumn("Nível de risco"),
        },
    )

    # ── Exportar ───────────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇  Exportar dados filtrados (.csv)",
        csv, "criminalidade_filtrado.csv", "text/csv",
    )

    # ── Estatísticas descritivas ───────────────────────────────────────────────
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    section("Estatísticas descritivas")
    cols_num = ["ocorrencias", "vitimas", "prisoes", "renda_media", "indice_violencia"]
    st.dataframe(
        df[cols_num].describe().round(2),
        use_container_width=True,
    )