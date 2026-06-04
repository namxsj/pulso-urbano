import streamlit as st
import plotly.express as px
import pandas as pd

from src.components import page_header, section, insight, ranking_card
from src.style import TEMPLATE, ESCALA_ROXA

# Coordenadas geográficas fixas de cada cidade do dataset
# Mapbox precisa de lat/lon explícitos; não tem como inferir do nome da cidade
COORDS = {
    "Manaus": (-3.1190, -60.0217), "Belém": (-1.4558, -48.5044),
    "Santarém": (-2.4448, -54.7081), "Porto Velho": (-8.7612, -63.9004),
    "Palmas": (-10.2491, -48.3243), "Salvador": (-12.9714, -38.5014),
    "Feira de Santana": (-12.2663, -38.9663), "Recife": (-8.0476, -34.8770),
    "Jaboatão dos Guararapes": (-8.1131, -35.0014), "Fortaleza": (-3.7319, -38.5267),
    "Juazeiro do Norte": (-7.2136, -39.3153), "João Pessoa": (-7.1195, -34.8450),
    "São Luís": (-2.5297, -44.3028), "São Paulo": (-23.5505, -46.6333),
    "Rio de Janeiro": (-22.9068, -43.1729), "Belo Horizonte": (-19.9167, -43.9345),
    "Campinas": (-22.9099, -47.0626), "Ribeirão Preto": (-21.1775, -47.8103),
    "Nova Iguaçu": (-22.7592, -43.4511), "Niterói": (-22.8833, -43.1036),
    "Petrópolis": (-22.5050, -43.1786), "Uberlândia": (-18.9186, -48.2772),
    "Juiz de Fora": (-21.7642, -43.3503), "Vitória": (-20.3155, -40.3128),
    "Vila Velha": (-20.3297, -40.2922), "Serra": (-20.1289, -40.3076),
    "Curitiba": (-25.4284, -49.2733), "Londrina": (-23.3045, -51.1696),
    "Florianópolis": (-27.5954, -48.5480), "Joinville": (-26.3044, -48.8487),
    "Porto Alegre": (-30.0346, -51.2177), "Caxias do Sul": (-29.1678, -51.1794),
    "Brasília": (-15.7797, -47.9297), "Goiânia": (-16.6869, -49.2648),
    "Aparecida de Goiânia": (-16.8231, -49.2439),
    "Cuiabá": (-15.6014, -56.0979), "Campo Grande": (-20.4697, -54.6201),
}

# Métricas disponíveis pra visualizar no mapa — chave = coluna do df, valor = label
METRICAS = {
    "ocorrencias":      "Ocorrências",
    "vitimas":          "Vítimas",
    "indice_violencia": "Índice de violência",
}


def render(df: pd.DataFrame) -> None:
    page_header(
        "Mapa",
        "Distribuição geográfica das cidades brasileiras"
    )

    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # Botões de seleção de métrica — armazenados no session_state pra não resetar
    if "mapa_metrica" not in st.session_state:
        st.session_state["mapa_metrica"] = "ocorrencias"

    btns = st.columns(len(METRICAS))
    for i, (chave, label) in enumerate(METRICAS.items()):
        with btns[i]:
            if st.button(label, key=f"btn_{chave}", use_container_width=True):
                st.session_state["mapa_metrica"] = chave
                st.rerun()

    metrica       = st.session_state["mapa_metrica"]
    label_metrica = METRICAS[metrica]

    # Consolida os dados por cidade — uma linha por cidade com a soma/média de cada métrica
    map_df = df.groupby("cidade").agg(
        ocorrencias=("ocorrencias", "sum"),
        vitimas=("vitimas", "sum"),
        indice_violencia=("indice_violencia", "mean"),
        regiao=("regiao", "first"),
        uf=("uf", "first"),
    ).reset_index()
    map_df["indice_violencia"] = map_df["indice_violencia"].round(1)

    # Adiciona as colunas de lat/lon buscando no dicionário de coordenadas
    # Cidades sem coordenadas ficam com (0, 0) e são removidas na linha seguinte
    map_df["lat"] = map_df["cidade"].map(lambda c: COORDS.get(c, (0, 0))[0])
    map_df["lon"] = map_df["cidade"].map(lambda c: COORDS.get(c, (0, 0))[1])
    map_df = map_df[map_df["lat"] != 0]

    # Layout dividido: mapa à esquerda (3/4) e ranking à direita (1/4)
    col_map, col_rank = st.columns([3, 1], gap="medium")

    # Função auxiliar que traduz o índice numérico em um label de risco legível
    def nivel_risco_label(idx):
        if idx < 30:   return "🟢 Baixo"
        if idx < 55:   return "🟡 Médio"
        if idx < 75:   return "🟠 Alto"
        return "🔴 Crítico"

    # Monta o texto do tooltip pra cada cidade usando apply() no dataframe
    map_df["tooltip"] = map_df.apply(
        lambda r: (
            f"<b style='font-size:15px'>{r['cidade']}</b><br>"
            f"<span style='color:#a78bfa'>📍 {r['uf']} · {r['regiao']}</span><br><br>"
            f"<b>🚨 Ocorrências:</b> {int(r['ocorrencias']):,}<br>"
            f"<b>🤕 Vítimas:</b> {int(r['vitimas']):,}<br>"
            f"<b>📊 Índice de violência:</b> {r['indice_violencia']:.1f}<br>"
            f"<b>⚠️ Nível de risco:</b> {nivel_risco_label(r['indice_violencia'])}"
        ).replace(",", "."),
        axis=1,
    )

    with col_map:
        fig = px.scatter_mapbox(
            map_df, lat="lat", lon="lon",
            size=metrica, color=metrica,
            hover_name="cidade",
            custom_data=["tooltip"],
            # Desativa os campos padrão do hover pra usar só o tooltip customizado
            hover_data={
                "uf": False, "regiao": False,
                "ocorrencias": False, "vitimas": False,
                "indice_violencia": False,
                "tooltip": False,
                "lat": False, "lon": False,
            },
            color_continuous_scale=["#312e81", "#7c3aed", "#c026d3", "#ef4444"],
            size_max=22, zoom=3.6,
            center={"lat": -14.0, "lon": -51.0},
            mapbox_style="carto-darkmatter",
        )
        fig.update_traces(
            hovertemplate="%{customdata[0]}<extra></extra>",
        )
        fig.update_layout(
            paper_bgcolor="#0b0e17",
            plot_bgcolor="#0b0e17",
            margin=dict(l=0, r=0, t=0, b=0),
            height=680,
            hoverlabel=dict(
                bgcolor="#111520",
                bordercolor="#2a3045",
                font=dict(color="#e2e8f0", size=13,
                          family="Google Sans Flex, sans-serif"),
                align="left",
            ),
            coloraxis_colorbar=dict(
                title=dict(text=label_metrica,
                           font=dict(color="#cbd5e1", size=13)),
                tickfont=dict(color="#cbd5e1", size=12),
                bgcolor="#111520",
                len=0.6,
            ),
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": False})

    with col_rank:
        # Ranking lateral das 10 cidades na métrica selecionada
        # pct calcula a proporção em relação ao máximo pra preencher a barra de progresso
        top10   = map_df.sort_values(metrica, ascending=False).head(10).reset_index(drop=True)
        val_max = top10[metrica].max()

        st.markdown(
            f"<div style='font-size:13px;color:#cbd5e1;text-transform:uppercase;"
            f"letter-spacing:.08em;padding:4px 0 12px'>Top 10 — {label_metrica}</div>",
            unsafe_allow_html=True,
        )

        for _, row in top10.iterrows():
            val = row[metrica]
            pct = int((val / val_max) * 100) if val_max > 0 else 0
            fmt = (f"{val:,.0f}".replace(",", ".")
                   if metrica != "indice_violencia" else f"{val:.1f}")
            ranking_card(row["cidade"], label_metrica, fmt, pct)

    # Gráficos secundários abaixo do mapa para análise por UF e por região
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    section("Ocorrências por UF")
    uf_df = (df.groupby("uf")["ocorrencias"].sum()
             .reset_index()
             .sort_values("ocorrencias", ascending=False))
    fig2 = px.bar(
        uf_df, x="uf", y="ocorrencias",
        color="ocorrencias", color_continuous_scale=ESCALA_ROXA,
        text="ocorrencias",
    )
    fig2.update_traces(
        texttemplate="%{text:,}", textposition="outside",
        textfont_color="#fbbf24", textfont_size=13, marker_line_width=0,
    )
    fig2.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=320,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
        margin=dict(t=50, b=10, l=40, r=20),
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    fig2.update_traces(
        hovertemplate="<b>%{x}</b><br>🚨 Ocorrências: <b>%{y:,.0f}</b><extra></extra>",
    )
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displayModeBar": False})

    section("Índice médio de violência por região")
    reg_idx = (df.groupby("regiao")["indice_violencia"].mean()
               .reset_index()
               .sort_values("indice_violencia", ascending=False))
    fig3 = px.bar(
        reg_idx, x="regiao", y="indice_violencia",
        color="indice_violencia",
        color_continuous_scale=["#4c1d95", "#ef4444"],
        text=reg_idx["indice_violencia"].round(1),
    )
    fig3.update_traces(
        texttemplate="%{text:.1f}", textposition="outside",
        textfont_color="#cbd5e1", textfont_size=13,
        marker_line_width=0,
    )
    fig3.update_layout(paper_bgcolor="#0b0e17", plot_bgcolor="#0b0e17",
        template=TEMPLATE, height=290,
        coloraxis_showscale=False, xaxis_title="", yaxis_title="",
        hoverlabel=dict(bgcolor="#111520", bordercolor="#2a3045",
            font=dict(color="#e2e8f0", size=13,
                      family="Google Sans Flex, sans-serif"), align="left"),
    )
    fig3.update_traces(
        hovertemplate="<b>%{x}</b><br>📊 Índice médio: <b>%{y:.1f}</b><extra></extra>",
    )
    st.plotly_chart(fig3, use_container_width=True,
                    config={"displayModeBar": False})

    insight("""
    <strong>Análise geográfica:</strong> O mapa de bolhas permite identificar visualmente
    a concentração de criminalidade pelo território nacional. Regiões metropolitanas do
    Sudeste concentram o maior volume absoluto de ocorrências, mas cidades do Norte e
    Nordeste apresentam índices de violência per capita mais elevados, revelando
    desigualdades estruturais significativas.
    """)
