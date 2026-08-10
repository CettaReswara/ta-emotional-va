"""Mood Diary

Run:  streamlit run app.py
"""
import streamlit as st

import config
import state
import ui
from pages_ui import diary, insight, detail

st.set_page_config(page_title="Demo TA 13521133", layout="centered")
ui.inject_css()
state.init()

page = st.session_state.page

if page == "diary":
    diary.render()
elif page == "insight":
    insight.render()
elif page == "detail":
    detail.render()

if page in ("diary", "insight"):
    ui.bottom_nav()
