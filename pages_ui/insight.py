"""Insight: today's detection + 7-day V/A trajectory + forecast.

Trajectory uses the currently selected model (roberta/deberta/ensemble) per
entry. Forecast = simple extrapolation, clearly marked as NOT a model output.
"""
import streamlit as st

import config
import ui
from inference.predictor import predict_for_entry
from viz.trajectory import svg_trajectory


def _forecast(series):
    if not series:
        return 0.0
    recent = series[-3:]
    return round(0.6 * series[-1] + 0.4 * (sum(recent) / len(recent)), 2)

CARD_COLORS = {
    "Excited": {"bg": "#F7C8D3", "fg": "#7a3b4a", "sub": "#9c5a6e"},  # blush
    "Calm":    {"bg": "#A8B58A", "fg": "#36421f", "sub": "#4f5e38"},  # sage
    "Tense":   {"bg": "#A9B7C6", "fg": "#2D3A47", "sub": "#4b5b6a"},  # misty sky
    "Sad":     {"bg": "#2D3A47", "fg": "#FFFFFF", "sub": "#A9B7C6"},  # midnight lagoon
}


def _mood_card(label, v, a):
    c = CARD_COLORS[label]
    return (
        '<div style="background:#FFFFFF;border-radius:18px;padding:14px;'
        'box-shadow:0 2px 10px rgba(45,58,71,0.07);margin-bottom:10px;">'
        '<div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">'
        '<span style="color:#B46A72;font-size:15px;">&#9829;</span>'
        '<span style="font-size:12px;font-weight:500;color:#2D3A47;">Mood detected today</span>'
        '</div>'
        f'<div style="position:relative;overflow:hidden;background:{c["bg"]};'
        'border-radius:14px;padding:16px;min-height:104px;">'
        f'<div style="position:absolute;right:-34px;bottom:-46px;width:140px;height:140px;'
        'border-radius:50%;background:rgba(255,255,255,0.16);"></div>'
        f'<div style="position:absolute;right:6px;top:-30px;width:90px;height:90px;'
        'border-radius:50%;background:rgba(255,255,255,0.10);"></div>'
        f'<div style="font-size:11px;color:{c["sub"]};position:relative;">Today</div>'
        f'<div style="font-size:32px;font-weight:500;color:{c["fg"]};line-height:1.05;'
        'margin-top:2px;position:relative;">' + label + '</div>'
        f'<div style="position:absolute;right:14px;bottom:14px;background:rgba(255,255,255,0.88);'
        'border-radius:20px;padding:5px 12px;font-size:12px;font-weight:500;color:#2D3A47;">'
        f'V {config.fmt_v(v)} &#183; A {config.fmt_a(a)}</div>'
        '</div></div>'
    )

def _pattern_note(vser, aser):
    n = len(vser)
    if n == 0:
        return "Not enough data this week."
    avg_v = sum(vser) / n
    half = max(1, n // 2)
    aro_trend = (sum(aser[-half:]) / len(aser[-half:])) - (sum(aser[:half]) / len(aser[:half]))
    var_v = max(vser) - min(vser)

    # 1) overall mood
    if avg_v > 0.1:
        mood = "Overall your mood leans positive this week."
    elif avg_v < -0.1:
        mood = "Lately your mood has felt a bit low."
    else:
        mood = "Your mood is fairly neutral this week."

    # 2) energy + variability
    if aro_trend > 0.1:
        trend = ("Your energy (arousal) looks like it's rising. Maybe too many stressors are making "
                 "you tense; try making time to read, pray, or enjoy nature to feel calmer.")
    elif aro_trend < -0.1:
        trend = ("Your energy (arousal) is trending down, calmer and more relaxed. That's good! "
                 "Balance it by seeking out new joys so you don't lose your positive spark.")
    elif var_v > 0.8:
        trend = ("Your mood has been up and down lately. Rest when you're tired. "
                 "Hope you keep getting better at managing your feelings.")
    else:
        trend = "The pattern is fairly stable. Keep up your good habits and improve where needed!"

    return f"{mood} {trend}"


def render():
    model = st.session_state.model
    P = config.PALETTE
    ui.header("Tuesday, June 24", "Insight")

    entries = list(reversed(st.session_state.entries))[-7:]
    preds = [predict_for_entry(e, model) for e in entries]
    vser = [p.valence for p in preds]
    aser = [p.arousal for p in preds]
    today = preds[-1]
    label, key = today.quadrant

    st.markdown(_mood_card(label, today.valence, today.arousal),
                unsafe_allow_html=True)

    fc = (_forecast(vser), _forecast(aser))
    st.markdown('<div class="card plain"><div style="display:flex;'
                'justify-content:space-between;margin-bottom:6px;">'
                '<span style="font-size:12px;font-weight:500;color:#2D3A47;">'
                'Last 7 days</span><span style="font-size:10px;color:#2D3A47;">'
                f'<span class="dot" style="width:12px;height:3px;border-radius:2px;'
                f'background:{config.VALENCE_COLOR}"></span>valence&nbsp;&nbsp;'
                f'<span class="dot" style="width:12px;height:3px;border-radius:2px;'
                f'background:{config.AROUSAL_COLOR}"></span>arousal</span></div>'
                + svg_trajectory(vser, aser, forecast=fc) + '</div>',
                unsafe_allow_html=True)

    note = _pattern_note(vser, aser)

    st.markdown(
        f'<div style="background:#FFFFFF;border-radius:18px;padding:16px 16px 14px;'
        f'box-shadow:0 2px 12px rgba(45,58,71,0.08);margin-bottom:10px;">'

        # header
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'margin-bottom:14px;">'
        f'<span style="display:flex;align-items:center;gap:6px;font-size:12px;color:#8a8a85;">'
        f'&#9728; This week</span>'
        f'<span style="font-size:12px;color:#A9B7C6;">7 days</span>'
        f'</div>'

        f'<div style="text-align:center;font-size:15px;font-weight:500;line-height:1.5;'
        f'color:{P["midnight"]};padding:0 6px 14px;">{note}</div>'

        f'</div>',
        unsafe_allow_html=True)
