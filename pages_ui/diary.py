"""Page 1 - Diary: write today's entry, view history. One diary owner."""
import streamlit as st

import config
import state
import ui
import data
from inference.predictor import predict_for_entry


def render():
    model = st.session_state.model

    _users = state.list_users()
    _cur = st.session_state.get("current_user")
    _name = next((u["label"] for u in _users if u["key"] == _cur), "Chaerish")
    
    _hc = st.container(key="headerrow")
    with _hc:
        c1, c2 = st.columns([3, 1], vertical_alignment="center")
        with c1:
            ui.header("Tuesday, June 24", f"Hi, {_name}", "How's your day?")
        with c2:
            ui.user_switcher()

    st.markdown('<div style="font-size:16px;font-weight:800;color:#4f5e38;'
                'margin:8px 2px 6px;">Today\'s story</div>', unsafe_allow_html=True)
    st.text_area("entry", key="today_text", height=110,
                 placeholder="Write whatever you're feeling...",
                 label_visibility="collapsed")

    def _save():
        t = st.session_state.today_text
        if t and t.strip():
            state.add_entry(t)
            st.session_state.today_text = ""

    st.button("Save", key="save_today", on_click=_save)

    st.selectbox("Model", data.MODELS, format_func=data.model_label,
                 key="model", label_visibility="visible")

    st.markdown('<div style="display:flex;justify-content:space-between;'
                'align-items:center;padding:6px 2px;"><span style="font-size:12px;'
                'font-weight:500;color:#2D3A47;">Earlier</span>'
                f'<span class="mini">{len(st.session_state.entries)} entries</span></div>',
                unsafe_allow_html=True)

    for e in st.session_state.entries:
        pred = predict_for_entry(e, model)
        label, key = pred.quadrant
        st.markdown(ui.entry_row_html(e, label, key), unsafe_allow_html=True)
        if st.button("See details \u2192", key=f"open_{e['id']}"):
            state.open_entry(e["id"])
