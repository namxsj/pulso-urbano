import base64
import os
import streamlit as st

from src.style import aplicar_tema
from src.data import load_data, aplicar_filtros
from src.pages import visao_geral, temporal, cidades, crimes, mapa, dados


# Converte a logo.png pra base64 pra usar como favicon no navegador
# Sem isso o Streamlit mostraria o ícone padrão na aba
def _logo_favicon():
    logo_path = os.path.join(os.path.dirname(__file__), "imagens", "logo.png")
    try:
        with open(logo_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    except Exception:
        return "🔍"


# Configurações globais da página: título, ícone e layout expandido
st.set_page_config(
    page_title="Pulso Urbano",
    page_icon=_logo_favicon(),
    layout="wide",
    initial_sidebar_state="expanded",
)

# Aplica o tema visual customizado (cores, fontes, CSS global)
aplicar_tema()

# Carrega o dataset principal e aplica os filtros da sidebar
# O df filtrado e a página ativa são retornados juntos
df_raw = load_data()
df, pagina = aplicar_filtros(df_raw)

# Pequeno truque pra rolar a página pro topo quando o usuário troca de aba
# O Streamlit não faz isso automaticamente, então a gente injeta um script
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

# Mapeamento das páginas disponíveis no sistema de navegação
PAGINAS = {
    "Visão Geral":      visao_geral,
    "Análise Temporal": temporal,
    "Por Cidade":       cidades,
    "Por Crime":        crimes,
    "Mapa":             mapa,
    "Dados":            dados,
}

# Renderiza a página selecionada passando o dataframe já filtrado
PAGINAS[pagina].render(df)
