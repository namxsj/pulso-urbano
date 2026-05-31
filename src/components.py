import streamlit as st


# Cores de acento por posição de KPI
_KPI_ACCENTS = ["#7c3aed", "#6d28d9", "#a78bfa", "#ef4444", "#fbbf24", "#4ade80"]


def page_header(titulo: str, subtitulo: str, badge: str = "", badge_extra: str = "",
                pagina: str = "") -> None:
    st.title(titulo)
    st.caption(subtitulo)
    st.divider()


def section(titulo: str) -> None:
    st.markdown(f"<div class='section-title'>{titulo}</div>", unsafe_allow_html=True)


def insight(texto: str) -> None:
    st.markdown(f"<div class='insight-box'>{texto}</div>", unsafe_allow_html=True)


def kpi(label: str, valor: str, delta: str = "", delta_dir: str = "neu",
        sub: str = "", idx: int = 0) -> None:
    accent = _KPI_ACCENTS[idx % len(_KPI_ACCENTS)]
    delta_html = f"<div class='kpi-delta delta-{delta_dir}'>{delta}</div>" if delta else ""
    sub_html = f"<div class='kpi-sub'>{sub}</div>" if sub else ""
    st.markdown(f"""
    <div class='kpi-card' style='--kpi-accent:{accent}'>
      <div class='kpi-label'>{label}</div>
      <div class='kpi-value'>{valor}</div>
      {sub_html}
      {delta_html}
    </div>
    """, unsafe_allow_html=True)


def ranking_card(cidade: str, label_metrica: str, valor: str, pct: int) -> None:
    st.markdown(f"""
    <div style='background:#111520;border:1px solid #1e2535;border-left:3px solid #7c3aed;
                border-radius:8px;padding:10px 12px;margin-bottom:7px;
                transition:border-color .2s'>
      <div style='font-size:15px;font-weight:500;color:#e2e8f0;margin-bottom:4px;
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{cidade}</div>
      <div style='display:flex;justify-content:space-between;align-items:center;
                  font-size:13px;color:#4a5568;margin-bottom:6px'>
        <span>{label_metrica}</span>
        <span style='color:#a78bfa;font-family:"Google Sans Flex",monospace;font-size:14px'>{valor}</span>
      </div>
      <div style='background:#1e2535;border-radius:3px;height:3px'>
        <div style='width:{pct}%;background:linear-gradient(to right,#4c1d95,#7c3aed,#a78bfa);
                    height:3px;border-radius:3px'></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def chart_card(conteudo_fn, titulo: str = "") -> None:
    titulo_html = f"<div class='section-title'>{titulo}</div>" if titulo else ""
    st.markdown(f"<div class='chart-card'>{titulo_html}", unsafe_allow_html=True)
    conteudo_fn()
    st.markdown("</div>", unsafe_allow_html=True)
