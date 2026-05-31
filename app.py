import base64, os
import streamlit as st

from src.style import aplicar_tema
from src.data import load_data, aplicar_filtros
from src.pages import visao_geral, temporal, cidades, crimes, mapa, dados


# ── Favicon a partir da logo.png ───────────────────────────────────────────────
def _logo_favicon():
    logo_path = os.path.join(os.path.dirname(__file__), "imagens", "logo.png")
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    except Exception:
        return "🔍"


# ── Configuração da página ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pulso Urbano",
    page_icon=_logo_favicon(),
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Tema global ────────────────────────────────────────────────────────────────
aplicar_tema()

# ── Dados ──────────────────────────────────────────────────────────────────────
df_raw = load_data()
df, pagina = aplicar_filtros(df_raw)

# ── Scroll para o topo ao trocar de página ────────────────────────────────────
if st.session_state.get("scroll_topo"):
    st.session_state["scroll_topo"] = False
    import streamlit.components.v1 as _c
    _c.html(
        "<script>"
        "window.parent.document.querySelectorAll("
        "  '.main .block-container, [data-testid=stAppViewBlockContainer]'"
        ").forEach(function(el){el.scrollTop=0;});"
        "window.parent.scrollTo(0,0);"
        "</script>",
        height=0,
    )

# ── Roteamento de páginas ──────────────────────────────────────────────────────
PAGINAS = {
    "Visão Geral":      visao_geral,
    "Análise Temporal": temporal,
    "Por Cidade":       cidades,
    "Por Crime":        crimes,
    "Mapa":             mapa,
    "Dados":            dados,
}

PAGINAS[pagina].render(df)
