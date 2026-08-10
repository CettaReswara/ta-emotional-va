"""Detail entry; circumplex from the selected model (roberta/deberta/ensemble)."""
import streamlit as st

import config
import state
import ui
import data
from inference.predictor import predict_for_entry
from viz.circumplex import svg_circumplex

QUAD_DESC = {
    "Excited": "excited and energized",
    "Calm":    "calm and at ease",
    "Tense":   "tense and restless",
    "Sad":     "sad and low",
}

def _intensity(x):
    m = abs(x)
    return "slightly" if m < 0.15 else ("moderately" if m < 0.45 else "strongly")

def _explanation(label, v, a):
    val_word = "positive" if v >= 0 else "negative"
    aro_word = "high" if a >= 0 else "low"
    return (
        f'The model reads the tone as {_intensity(v)} <b>{val_word}</b> '
        f'(valence {config.fmt_v(v)}), with <b>{aro_word}</b> energy '
        f'(arousal {config.fmt_a(a)}). Together this suggests you\'re feeling '
        f'{QUAD_DESC.get(label, "")}.'
    )

def render():
    P = config.PALETTE
    entry = state.selected_entry()
    if entry is None:
        state.go("diary")
        return

    model = st.session_state.model

    if st.button("\u2190 Back", key="back"):
        state.go("diary")

    pred = predict_for_entry(entry, model)
    label, key = pred.quadrant

    # header
    st.markdown(
        f'<div style="padding:6px 2px 2px;">'
        f'<div class="mini">{entry["day"]}, {entry["date"]}</div>'
        f'<div style="font-size:12px;color:#B46A72;margin-top:2px;">'
        f'model: {data.model_label(model)}</div></div>',
        unsafe_allow_html=True)

    # entry text
    txt = entry["text"]
    size = 22 if len(txt) < 60 else (18 if len(txt) < 160 else 15)
    st.markdown(
        f'<div style="font-size:{size}px;line-height:1.5;color:{P["midnight"]};'
        f'font-weight:500;padding:10px 2px 16px;">{txt}</div>',
        unsafe_allow_html=True)

    st.markdown(
            '<div style="display:flex;align-items:center;justify-content:space-between;'
            'padding:8px 2px;gap:8px;">'
            '<span style="font-size:12px;font-weight:500;color:#2D3A47;">'
            'Emotion the model detected</span>'
            f'{ui.chip(label, key)}</div>',
            unsafe_allow_html=True)
    st.markdown(f'<div style="display:flex;justify-content:center;">'
                f'{svg_circumplex((pred.valence, pred.arousal), width=220)}</div>',
                unsafe_allow_html=True)

    st.markdown(f'<div style="padding:8px 2px;">{ui.va_chips(pred)}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="background:#FFFFFF;border-radius:18px;padding:16px 16px 14px;'
        f'box-shadow:0 2px 12px rgba(45,58,71,0.08);margin-bottom:10px;">'

        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'margin-bottom:14px;">'
        f'<span style="display:flex;align-items:center;gap:6px;font-size:12px;color:#8a8a85;">'
        f'&#9728; Why this?</span>'
        f'</div>'

        f'<div style="text-align:center;font-size:15px;font-weight:500;line-height:1.5;'
        f'color:{P["midnight"]};padding:0 6px 14px;">'
        f'{_explanation(label, pred.valence, pred.arousal)}</div>'

        f'</div>',
        unsafe_allow_html=True)
