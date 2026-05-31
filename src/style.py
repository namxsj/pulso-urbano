import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio


# ── Paleta de cores ────────────────────────────────────────────────────────────
CORES = [
    "#7c3aed", "#a78bfa", "#6d28d9", "#ef4444",
    "#fbbf24", "#4ade80", "#22d3ee", "#f472b6",
    "#fb923c", "#34d399",
]
ESCALA_ROXA  = ["#312e81", "#7c3aed", "#ef4444"]
ESCALA_CRIME = ["#0f1117", "#4c1d95", "#7c3aed", "#ef4444"]
TEMPLATE     = "crimedata"


BG       = "#0b0e17"   
BG2      = "#111520"   


def registrar_template() -> None:
    pio.templates[TEMPLATE] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=BG,
            plot_bgcolor=BG,
            font=dict(family="Google Sans Flex, Google Sans Text, sans-serif", color="#cbd5e1", size=13),
            colorway=CORES,
            xaxis=dict(gridcolor="#1e2535", linecolor="#1e2535", zerolinecolor="#1e2535"),
            yaxis=dict(gridcolor="#1e2535", linecolor="#1e2535", zerolinecolor="#1e2535"),
            legend=dict(bgcolor=BG, bordercolor="#1e2535"),
            margin=dict(l=40, r=20, t=30, b=10),
        )
    )


def bg_layout() -> dict:
    return dict(paper_bgcolor=BG, plot_bgcolor=BG)


def aplicar_tema() -> None:
    registrar_template()
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300;400;500;600;700&family=Google+Sans+Text:wght@400;500&display=swap');

:root {
    --bg:        #0b0e17;
    --bg2:       #111520;
    --bg3:       #161b2a;
    --border:    #1e2535;
    --border2:   #2a3045;
    --purple:    #7c3aed;
    --purple-lt: #a78bfa;
    --purple-dk: #1e1540;
    --text:      #e2e8f0;
    --muted:     #4a5568;
    --sub:       #8892a4;
    --red:       #f87171;
    --green:     #4ade80;
    --amber:     #fbbf24;
    --cyan:      #22d3ee;
}

/* ── Base ─────────────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section {
    background: var(--bg) !important;
    font-family: 'Google Sans Flex', 'Google Sans Text', sans-serif !important;
    color: var(--text) !important;
    font-size: 17px !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { font-size: 17px !important; line-height: 1.7 !important; }
[data-testid="stWidgetLabel"] p        { font-size: 16px !important; font-weight: 500 !important; }
[data-baseweb="tag"] span              { font-size: 14px !important; }
[role="option"]                        { font-size: 16px !important; }

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-size: 15px !important;
}

/* ── Radio (navegação) — só a bolinha muda de cor ─────────── */
[data-testid="stSidebar"] [data-baseweb="radio"] svg {
    color: var(--purple) !important;
    fill: var(--purple) !important;
}
/* ── Widgets gerais (multiselect, select_slider, slider) ──── */

/* Container dos widgets — fundo dark, sem overflow cortado */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] .stSelectSlider,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stSlider {
    overflow: visible !important;
}

/* Input box do multiselect */
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: var(--bg3) !important;
    border-color: var(--border2) !important;
    border-radius: 8px !important;
    min-height: 40px !important;
    overflow: visible !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:focus-within {
    border-color: var(--purple) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* Select slider (período) */
[data-testid="stSidebar"] [data-testid="stSliderThumbValue"],
[data-testid="stSidebar"] .stSelectSlider [data-baseweb="select"] > div {
    background: var(--bg3) !important;
    border-color: var(--border2) !important;
    border-radius: 8px !important;
    overflow: visible !important;
}

/* Dropdown popover — fundo dark, sem corte */
[data-baseweb="popover"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
    overflow: visible !important;
    z-index: 9999 !important;
}
[data-baseweb="popover"] ul,
[data-baseweb="popover"] [role="listbox"] {
    background: var(--bg3) !important;
    border-radius: 8px !important;
    padding: 4px !important;
}
[role="option"] {
    background: var(--bg3) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-size: 15px !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: var(--purple-dk) !important;
    color: var(--purple-lt) !important;
}

/* Tags selecionadas no multiselect */
[data-baseweb="tag"] {
    background: var(--purple-dk) !important;
    border: 1px solid rgba(124,58,237,.4) !important;
    border-radius: 6px !important;
    margin: 2px !important;
}
[data-baseweb="tag"] span {
    color: var(--purple-lt) !important;
    font-size: 13px !important;
}
[data-baseweb="tag"] [role="presentation"] svg {
    fill: var(--purple-lt) !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: var(--purple-dk) !important;
    border: 1px solid rgba(124,58,237,.4) !important;
}

/* Slider range (select_slider e stSlider) */
[data-testid="stSlider"] [role="slider"] {
    background: var(--purple) !important;
    border-color: var(--purple-lt) !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] {
    color: var(--muted) !important;
}
[data-testid="stSlider"] > div {
    overflow: visible !important;
}
/* Trilha do slider */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="progressbar"],
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    background: var(--border2) !important;
}
/* Parte preenchida */
[data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stSliderTrackFill"] {
    background: linear-gradient(to right, #4c1d95, #7c3aed) !important;
}

/* Label flutuante do valor no slider — forçar acima do thumb sem sobreposição */
[data-testid="stSlider"] div[data-testid="stSliderThumbValue"],
[data-testid="stSelectSlider"] span {
    background: var(--bg3) !important;
    color: var(--purple-lt) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 4px !important;
    font-size: 12px !important;
    padding: 2px 6px !important;
    white-space: nowrap !important;
}

/* Tick labels (2015, 2024) ficam abaixo sem sobrepor */
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: var(--muted) !important;
    font-size: 12px !important;
    margin-top: 4px !important;
}

/* Garante espaço vertical suficiente no wrapper do slider */
[data-testid="stSidebar"] [data-testid="stSlider"] {
    padding-bottom: 8px !important;
    overflow: visible !important;
}
[data-testid="stSidebar"] .stSelectSlider {
    padding-bottom: 8px !important;
    overflow: visible !important;
}

/* ── KPI Cards ────────────────────────────────────────────── */
.kpi-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px 14px;
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: border-color .2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--kpi-accent, var(--purple));
    border-radius: 10px 10px 0 0;
}
.kpi-card:hover { border-color: var(--border2); }
.kpi-label {
    font-size: 15px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 8px;
    font-weight: 500;
}
.kpi-value {
    font-size: 32px;
    font-weight: 600;
    color: var(--text);
    font-family: 'Google Sans Flex', monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
}
.kpi-sub {
    font-size: 16px;
    color: var(--sub);
    margin-top: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-delta { font-size: 15px; margin-top: 5px; display: flex; align-items: center; gap: 4px; }
.delta-up   { color: var(--red); }
.delta-down { color: var(--green); }
.delta-neu  { color: var(--muted); }

/* ── Section titles ───────────────────────────────────────── */
.section-title {
    font-size: 16px;
    font-weight: 500;
    color: var(--sub);
    text-transform: uppercase;
    letter-spacing: .1em;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 14px;
    margin-top: 6px;
}

/* ── Page header ──────────────────────────────────────────── */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 22px;
}
.page-header-left { display: flex; align-items: center; gap: 14px; }
.page-header-icon {
    background: var(--purple-dk);
    border: 1px solid var(--border2);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 20px;
    line-height: 1;
}
.page-header h1 {
    font-size: 22px;
    font-weight: 600;
    color: var(--text);
    margin: 0;
    letter-spacing: -.01em;
}
.page-header p { font-size: 15px; color: var(--muted); margin: 2px 0 0; }

/* ── Badges ───────────────────────────────────────────────── */
.badge-pill {
    background: var(--purple-dk);
    color: var(--purple-lt);
    font-size: 13px;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 500;
    border: 1px solid rgba(124,58,237,.3);
    white-space: nowrap;
}
.badge-green {
    background: rgba(74,222,128,.08);
    color: var(--green);
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 20px;
    font-weight: 500;
    border: 1px solid rgba(74,222,128,.25);
}

/* ── Insight box ──────────────────────────────────────────── */
.insight-box {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--purple);
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 16px;
    color: var(--sub);
    line-height: 1.9;
    margin-top: 6px;
}
.insight-box strong { color: var(--purple-lt); }


/* ── Chart iframe wrapper ─────────────────────────────────── */
/* Streamlit 1.35+ embeds charts in iframes — bgcolor is set   */
/* via Plotly paper_bgcolor in the template (solid #0b0e17).   */
[data-testid="stPlotlyChart"] {
    background: transparent !important;
}
[data-testid="stPlotlyChart"] iframe {
    background: #0b0e17 !important;
}

/* ── Chart card wrapper ───────────────────────────────────── */
.chart-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px 10px;
    margin-bottom: 4px;
}

/* ── Dataframe / tabela ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: var(--bg2) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg3) !important;
    color: var(--sub) !important;
    font-size: 14px !important;
    letter-spacing: .06em !important;
    border-bottom: 1px solid var(--border2) !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text) !important;
    font-size: 14px !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: var(--purple-dk) !important;
}

/* ── Download button ──────────────────────────────────────── */
[data-testid="stDownloadButton"] button {
    background: var(--purple-dk) !important;
    color: var(--purple-lt) !important;
    border: 1px solid rgba(124,58,237,.4) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all .2s;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(124,58,237,.3) !important;
    border-color: var(--purple) !important;
}

/* ── Botões genéricos ─────────────────────────────────────── */
[data-testid="stButton"] button {
    background: var(--bg3) !important;
    color: var(--sub) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all .2s;
}
[data-testid="stButton"] button:hover {
    background: var(--purple-dk) !important;
    color: var(--purple-lt) !important;
    border-color: var(--purple) !important;
}

/* ── Warning / info ───────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(124,58,237,.08) !important;
    border: 1px solid rgba(124,58,237,.2) !important;
    border-radius: 8px !important;
    color: var(--sub) !important;
}

/* ── Layout ───────────────────────────────────────────────── */
[data-testid="stMainBlockContainer"] {
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    padding-top: 4.5rem !important;
    max-width: 100% !important;
}
[data-testid="stHeader"] {
    background: var(--bg) !important;
    border-bottom: 0 !important;
}

/* ── Esconde nativo ───────────────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
div[data-testid="stMetric"] { display: none; }
    
</style>

<script>
(function fixPlotlyIframes() {
    var BG = "#0b0e17";
    function paintIframes() {
        document.querySelectorAll('[data-testid="stPlotlyChart"] iframe').forEach(function(iframe) {
            iframe.style.background = BG;
            try {
                var doc = iframe.contentDocument || iframe.contentWindow.document;
                if (doc && doc.body) {
                    doc.body.style.background = BG;
                    doc.documentElement.style.background = BG;
                    doc.querySelectorAll(".bg, .paper, rect.bg").forEach(function(el) {
                        el.style.fill = BG;
                    });
                }
            } catch(e) {}
        });
    }
    paintIframes();
    var obs = new MutationObserver(function() { paintIframes(); });
    obs.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)