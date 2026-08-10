"""Visual layer
"""
import streamlit as st

import config


P = config.PALETTE


def inject_css():
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?'
        'family=Elms+Sans:wght@400;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True)
    st.markdown(f"""
    <style>
         #MainMenu, header, footer {{visibility: hidden;}}
        .block-container {{
            max-width: 380px;
            padding: 1.2rem 1rem 90px;
            background: rgba(255, 255, 255, 0.55);
            border-radius: 22px;
        }}
        .stApp {{
            background:
                radial-gradient(60% 55% at 22% 18%, rgba(247,200,211,0.55) 0%, rgba(247,200,211,0) 70%),
                radial-gradient(55% 50% at 82% 30%, rgba(169,183,198,0.40) 0%, rgba(169,183,198,0) 70%),
                radial-gradient(60% 55% at 60% 88%, rgba(168,181,138,0.32) 0%, rgba(168,181,138,0) 70%),
                radial-gradient(50% 45% at 40% 60%, rgba(255,247,230,0.60) 0%, rgba(255,247,230,0) 70%),
                #FCF8F4 !important;
            background-attachment: fixed !important;
        }}
        .mini {{font-size: 12px; color: {P['sky']};}}
        .h1 {{font-size: 20px; font-weight: 500; color: {P['midnight']}; margin: 2px 0;}}
        .sub {{font-size: 13px; color: {P['rosewood']};}}
        .card {{border-radius: 14px; padding: 12px; margin-bottom: 10px;}}
        .vanilla {{background: {P['vanilla']}; border: 0.5px solid rgba(180,106,114,0.25);}}
        .plain   {{background: {P['white']}; border: 0.5px solid rgba(45,58,71,0.14);}}
        .sage    {{background: {P['vanilla']}; border: 0.5px solid rgba(168,181,138,0.5);}}
        .entry-text {{font-size: 13px; color: {P['midnight']}; line-height: 1.45;
                        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}}
        .dot {{width: 10px; height: 10px; border-radius: 50%; display: inline-block;
                margin-right: 8px; vertical-align: middle;}}
        .chip {{display:inline-block; font-size: 12px; font-weight: 500;
                padding: 6px 12px; border-radius: 8px;}}
        .stTextArea textarea, .stTextInput input {{
          background-color: #FFFFFF !important; color: #2D3A47 !important;
          -webkit-text-fill-color: #2D3A47 !important; caret-color: #2D3A47 !important;
          border: none !important;
          border-radius: 14px !important;
          padding: 16px !important;
          box-shadow: 0 4px 20px rgba(45,58,71,0.08) !important;
          font-size: 15px !important;
          line-height: 1.6 !important;
        }}
        div[data-baseweb="textarea"], div[data-baseweb="base-input"] {{
            background-color: #FFFFFF !important;
            border: none !important;
            box-shadow: none !important;
        }}
        .stTextArea textarea::placeholder,
        .stTextInput input::placeholder {{
            color: #A9B7C6 !important;
            -webkit-text-fill-color: #A9B7C6 !important;
        }}
        div[data-baseweb="textarea"],
        div[data-baseweb="base-input"] {{
            background-color: #FFFFFF !important;
            border-color: rgba(45,58,71,0.2) !important;
        }}
        /* nav + open buttons */
        div[data-testid="stButton"] > button {{
            border-radius: 9px; border: 0.5px solid rgba(45,58,71,0.18);
            color: {P['midnight']}; background: {P['white']}; font-size: 13px;
        }}

        /* nav */
        .block-container {{ padding-bottom: 90px !important; }}
        div[data-testid="stHorizontalBlock"]:last-of-type:not(.st-key-headerrow *) {{
          position: fixed;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 100%;
          max-width: 380px;
          background: #FFFFFF;
          border-top: 0.5px solid rgba(45,58,71,0.12);
          padding: 6px 12px;
          z-index: 100;

          /* dropdown */
          div[data-baseweb="select"] > div {{
              background-color: #FFF7E6 !important;
              border: 0.5px solid rgba(180,106,114,0.25) !important;
              border-radius: 10px !important;
          }}
          div[data-baseweb="select"] * {{ color: #2D3A47 !important; }}

          /* label di atas dropdown */
          .stSelectbox label {{
              color: #2D3A47 !important;
              font-size: 12px !important;
              font-weight: 500 !important;
          }}

          /* tombol Simpan */
          div[data-testid="stButton"] > button {{
              background-color: #B46A72 !important;
              color: #FFFFFF !important;
              border: none !important;
              border-radius: 9px !important;
              font-weight: 500 !important;
          }}
      }}
      
      html, body, .stApp, .block-container, .stApp * {{
          font-family: 'Elms Sans', sans-serif !important;
      }}
      /* tombol "Lihat detail" -> link kecil */
      [class*="st-key-open_"] button {{
          background: transparent !important;
          color: #B46A72 !important;
          border: none !important;
          box-shadow: none !important;
          font-size: 8px !important;
          padding: 0 4px !important;
          margin-top: -8px !important;
          min-height: 0 !important;
      }}

      /* user switcher */
      .st-key-user_pick {{ position:absolute; top:12px; right:12px; width:46px !important; z-index:50; }}
      .st-key-user_pick div[data-baseweb="select"] > div {{ background:transparent !important; border:none !important; }}
      .st-key-user_pick div[data-baseweb="select"] > div > div:first-child {{ opacity:0 !important; }}
      .st-key-switcher_btn button p,
      .st-key-switcher_btn button div,
      .st-key-switcher_btn button span {{
          font-size: 10px !important;
      }}
      .st-key-switcher_btn {{ display:flex; justify-content:flex-start; margin-top:-10px; margin-bottom:6px; }}
      .st-key-switcher_btn button {{
          border-radius:16px !important;
          font-size:10px !important;
          font-weight:400 !important;
          padding:5px 10px !important;
          min-height:0 !important;
          line-height:1.2 !important;
          box-shadow:none !important;
          width:auto !important;
          background:transparent !important;
          color:#8a8a85 !important;
          border:0.5px solid rgba(45,58,71,0.18) !important;
      }}
    </style>
    """, unsafe_allow_html=True)


def header(date_label: str, title: str, sub: str = ""):
    sub_html = f'<div class="sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div style="padding:6px 2px 4px;"><div class="mini">{date_label}</div>'
        f'<div class="h1">{title}</div>{sub_html}</div>',
        unsafe_allow_html=True)


def mood_dot(palette_key: str) -> str:
    return f'<span class="dot" style="background:{P[palette_key]}"></span>'


def entry_row_html(entry: dict, quad_label: str, palette_key: str) -> str:
    P = config.PALETTE
    # ikon mood per kuadran
    ICONS = {"Excited": "&#9728;", "Calm": "&#127807;",   # matahari / daun
             "Tense": "&#9889;", "Sad": "&#9729;"}          # petir / awan
    icon = ICONS.get(quad_label, "&#9829;")
    tint = P[palette_key]
    # tanggal pendek: ambil dari entry["date"] (YYYY-MM-DD -> DD/MM)
    d = entry.get("date", "")
    short = f'{d[8:]}/{d[5:7]}' if len(d) >= 10 else entry.get("day", "")
    return (
        '<div style="display:flex;align-items:center;gap:12px;background:#FFFFFF;'
        'border-radius:16px;padding:12px 14px;margin-bottom:10px;'
        'box-shadow:0 1px 8px rgba(45,58,71,0.06);">'

        # ikon mood (kotak warna)
        f'<div style="width:44px;height:44px;border-radius:12px;flex-shrink:0;'
        f'background:{tint};display:flex;align-items:center;justify-content:center;'
        f'font-size:20px;">{icon}</div>'

        # teks: judul (mood) + cuplikan entri
        '<div style="flex:1;min-width:0;">'
        f'<div style="font-size:14px;font-weight:500;color:{P["midnight"]};'
        'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
        f'{entry["text"]}</div>'
        f'<div style="font-size:11px;color:#A9B7C6;margin-top:2px;">{quad_label}</div>'
        '</div>'

        # kanan: garis pemisah + tanggal/hari
        '<div style="display:flex;align-items:center;gap:10px;flex-shrink:0;'
        'border-left:0.5px solid rgba(45,58,71,0.10);padding-left:12px;">'
        f'<div style="text-align:right;"><div style="font-size:13px;color:#5f5e5a;">'
        f'{short}</div><div style="font-size:10px;color:#A9B7C6;">'
        f'{entry.get("day","")}</div></div></div>'

        '</div>'
    )

def chip(text: str, palette_key: str) -> str:
    bg = {"rosewood": "rgba(180,106,114,0.16)", "sage": "rgba(168,181,138,0.18)",
          "sky": "rgba(169,183,198,0.22)", "blush": "rgba(247,200,211,0.3)"}.get(
              palette_key, "rgba(180,106,114,0.16)")
    fg = {"rosewood": "#8a4b51", "sage": "#5f7042", "sky": "#5b6b7a",
          "blush": "#9c5a6e"}.get(palette_key, "#8a4b51")
    return f'<span class="chip" style="background:{bg}; color:{fg};">{text}</span>'


def va_chips(pred) -> str:
    return (
        f'<div style="display:flex; gap:8px;">'
        f'<div class="card plain" style="flex:1; margin:0; padding:8px 10px;">'
        f'<div style="font-size:10px;color:{config.VALENCE_COLOR};">'
        f'<span class="dot" style="width:7px;height:7px;background:{config.VALENCE_COLOR}"></span>valence</div>'
        f'<div style="font-size:18px;font-weight:500;color:{P["midnight"]};">{config.fmt_v(pred.valence)}</div></div>'
        f'<div class="card plain" style="flex:1; margin:0; padding:8px 10px;">'
        f'<div style="font-size:10px;color:{config.AROUSAL_COLOR};">'
        f'<span class="dot" style="width:7px;height:7px;background:{config.AROUSAL_COLOR}"></span>arousal</div>'
        f'<div style="font-size:18px;font-weight:500;color:{P["midnight"]};">{config.fmt_a(pred.arousal)}</div></div>'
        f'</div>'
    )


def bottom_nav():
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    page = st.session_state.page
    with c1:
        if st.button("\u25CB Diary" if page != "diary" else "\u25CF Diary",
                     use_container_width=True, key="nav_diary"):
            st.session_state.page = "diary"
            st.rerun()
    with c2:
        if st.button("\u25CB Insight" if page != "insight" else "\u25CF Insight",
                     use_container_width=True, key="nav_insight"):
            st.session_state.page = "insight"
            st.rerun()

# ---- multi-user switcher (IG-style, pakai st.dialog) ----
def _switcher_body():
    import state
    users = state.list_users()
    cur = st.session_state.get("current_user")
    st.markdown('<div style="font-size:11px;color:#A9B7C6;margin:0 0 8px;">'
                'Pick a user to view their diary</div>', unsafe_allow_html=True)
    for u in users:
        active = (u["key"] == cur)
        mark = "\u2713 " if active else ""
        if st.button(f"{mark}{u['label']}", key=f"pick_{u['key']}",
                     use_container_width=True):
            state.load_user(u["path"])
            st.session_state.page = "diary"
            st.rerun()
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    up = st.file_uploader("Add user \u2014 import a JSON file",
                          type=["json"], key="add_user_up")
    if up is not None:
        try:
            state.import_user_file(up)
            st.session_state.page = "diary"
            st.rerun()
        except Exception as e:
            st.error(f"Not a valid user JSON: {e}")


if hasattr(st, "dialog"):
    @st.dialog("Switch user")
    def _switcher_dialog():
        _switcher_body()


def user_switcher():
    """Trigger di atas halaman: nama user aktif + panah -> buka switcher."""
    import state
    users = state.list_users()
    if not users:
        return
    cur = st.session_state.get("current_user")
    label = next((u["label"] for u in users if u["key"] == cur), users[0]["label"])
    if st.button(f"Switch user", key="switcher_btn"):
        if hasattr(st, "dialog"):
            _switcher_dialog()
        else:
            st.session_state._switch_open = not st.session_state.get("_switch_open", False)
            st.rerun()
    if not hasattr(st, "dialog") and st.session_state.get("_switch_open"):
        _switcher_body()
