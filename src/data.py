import os
import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("dados/simulacao_criminalidade_brasil.csv", encoding="utf-8-sig")
    df["data"] = pd.to_datetime(df["data"])
    return df


def aplicar_filtros(df: pd.DataFrame):
    with st.sidebar:
        # ── Logo ───────────────────────────────────────────────────────────────
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagens", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

        # ── Navegação ──────────────────────────────────────────────────────────
        st.markdown("<div class=\'section-title\'>Navegação</div>", unsafe_allow_html=True)

        PAGINAS_NAV = [
            "Visão Geral",
            "Análise Temporal",
            "Por Cidade",
            "Por Crime",
            "Mapa",
            "Dados",
        ]

        if "pagina_ativa" not in st.session_state:
            st.session_state["pagina_ativa"] = "Visão Geral"

        pagina = st.radio(
            "",
            PAGINAS_NAV,
            index=PAGINAS_NAV.index(st.session_state["pagina_ativa"]),
            label_visibility="collapsed",
            key="nav_radio",
        )

        if pagina != st.session_state["pagina_ativa"]:
            st.session_state["pagina_ativa"] = pagina
            st.session_state["scroll_topo"] = True
            st.rerun()

        st.markdown(
            "<div class='section-title' style='margin-top:24px'>Filtros</div>",
            unsafe_allow_html=True,
        )

        # ── Período ────────────────────────────────────────────────────────────
        anos_disp = sorted(df["ano"].unique())
        ano_min, ano_max = int(anos_disp[0]), int(anos_disp[-1])

        if "ano_inicio" not in st.session_state:
            st.session_state["ano_inicio"] = ano_min
        if "ano_fim" not in st.session_state:
            st.session_state["ano_fim"] = ano_max

        st.markdown(
            "<label style='font-size:13px;color:#cbd5e1;font-weight:500;"
            "letter-spacing:.03em;margin-bottom:4px;display:block'>Período</label>",
            unsafe_allow_html=True,
        )

        # CSS para corrigir legibilidade dos inputs de ano
        st.markdown("""
        <style>
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
            background: #161b2a !important;
            color: #e2e8f0 !important;
            border: 1px solid #2a3045 !important;
            border-radius: 8px !important;
            font-size: 15px !important;
            text-align: center !important;
        }
        [data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus {
            border-color: #7c3aed !important;
            box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
            outline: none !important;
        }
        [data-testid="stSidebar"] [data-testid="stNumberInput"] button {
            background: #161b2a !important;
            border-color: #2a3045 !important;
            color: #a78bfa !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col_a, col_sep, col_b = st.columns([2, 0.5, 2])
        with col_a:
            ini = st.number_input(
                "De", min_value=ano_min, max_value=ano_max,
                value=st.session_state["ano_inicio"],
                step=1, key="ni_inicio", label_visibility="collapsed",
            )
        with col_sep:
            st.markdown(
                "<div style='text-align:center;padding-top:10px;"
                "color:#a78bfa;font-size:18px'>→</div>",
                unsafe_allow_html=True,
            )
        with col_b:
            fim = st.number_input(
                "Até", min_value=ano_min, max_value=ano_max,
                value=st.session_state["ano_fim"],
                step=1, key="ni_fim", label_visibility="collapsed",
            )

        ini, fim = int(ini), int(fim)
        if ini > fim:
            ini, fim = fim, ini
        st.session_state["ano_inicio"] = ini
        st.session_state["ano_fim"] = fim

        # Barra visual de progresso entre os anos
        pct_start = (ini - ano_min) / max(ano_max - ano_min, 1) * 100
        pct_end   = (fim - ano_min) / max(ano_max - ano_min, 1) * 100
        st.markdown(f"""
        <div style="position:relative;height:6px;background:#1e2535;
                    border-radius:3px;margin:4px 0 12px">
          <div style="position:absolute;left:{pct_start:.1f}%;right:{100-pct_end:.1f}%;
                      height:100%;background:linear-gradient(to right,#4c1d95,#7c3aed);
                      border-radius:3px"></div>
        </div>""", unsafe_allow_html=True)

        anos = (ini, fim)

        # ── Região ─────────────────────────────────────────────────────────────
        regioes_disp = sorted(df["regiao"].unique())
        regioes = st.multiselect("Região", regioes_disp, default=regioes_disp)

        # ── UF encadeada ───────────────────────────────────────────────────────
        _regioes = regioes or regioes_disp
        ufs_disp = sorted(df[df["regiao"].isin(_regioes)]["uf"].unique())
        ufs = st.multiselect("Estado (UF)", ufs_disp, default=ufs_disp)

        # ── Cidade encadeada ───────────────────────────────────────────────────
        _ufs = ufs or ufs_disp
        cidades_disp = sorted(df[df["uf"].isin(_ufs)]["cidade"].unique())
        cidades = st.multiselect("Cidade", cidades_disp, default=cidades_disp)

        # ── Tipo de crime ──────────────────────────────────────────────────────
        crimes_disp = sorted(df["tipo_crime"].unique())
        crimes = st.multiselect("Tipo de crime", crimes_disp, default=crimes_disp)

        # ── Nível de risco ─────────────────────────────────────────────────────
        riscos = st.multiselect(
            "Nível de risco",
            ["Baixo", "Médio", "Alto", "Crítico"],
            default=["Baixo", "Médio", "Alto", "Crítico"],
        )

        # ── Rodapé ─────────────────────────────────────────────────────────────
        st.markdown("""
        <div style='margin-top:36px;padding-top:16px;border-top:1px solid #1e2535;
             font-size:11px;color:#374151;text-align:center;line-height:1.8'>
            Projeto G2 · Análise de Dados<br>
            <span style='color:#7c3aed;font-weight:500'>LA SALLE</span>
            <span style='color:#2a3045'> · 2015 – 2024</span>
        </div>""", unsafe_allow_html=True)

    # ── Aplica filtros ─────────────────────────────────────────────────────────
    _regioes  = regioes  or regioes_disp
    _ufs      = ufs      or ufs_disp
    _cidades  = cidades  or cidades_disp
    _crimes   = crimes   or crimes_disp
    _riscos   = riscos   or ["Baixo", "Médio", "Alto", "Crítico"]

    df_filtrado = df[
        (df["ano"]        >= anos[0])      & (df["ano"] <= anos[1]) &
        (df["regiao"]     .isin(_regioes)) &
        (df["uf"]         .isin(_ufs))     &
        (df["cidade"]     .isin(_cidades)) &
        (df["tipo_crime"] .isin(_crimes))  &
        (df["nivel_risco"].isin(_riscos))
    ].copy()

    return df_filtrado, pagina