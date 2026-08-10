"""
entries.json = list entri (atau dict {entries, forecast_2a})
"""
import json
import re
from pathlib import Path

import streamlit as st

import data

APP_DIR = Path(__file__).parent
STORE = APP_DIR / "entries.json"


# --------------------------------------------------------------------------
# MULTI-USER
# --------------------------------------------------------------------------
def list_users():
    """Semua file entries*.json di folder app -> daftar user buat switcher."""
    users = []
    for f in sorted(APP_DIR.glob("entries*.json")):
        m = re.search(r"user(\d+)", f.stem)
        if m:
            label = f"User {m.group(1)}"
        elif f.stem == "entries":
            label = "Chaerish"
        else:
            label = f.stem.replace("entries_", "").replace("_", " ").strip() or f.stem
        users.append({"key": f.stem, "label": label, "path": f})
    return users


def load_user(path):
    """Muat 1 file user ke session (dukung format list & dict)."""
    path = Path(path)
    d = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(d, dict):
        st.session_state.forecast_2a = d.get("forecast_2a")
        st.session_state.entries = d.get("entries", [])
    else:
        st.session_state.forecast_2a = None
        st.session_state.entries = d
    st.session_state.current_user = path.stem
    st.session_state.selected = None


def import_user_file(uploaded):
    """Simpan file JSON yang di-upload ke folder app, lalu muat sbg user aktif.
    Nama dipaksa diawali 'entries' biar kebaca list_users()."""
    content = uploaded.read().decode("utf-8")
    json.loads(content)                       # validasi (lempar error kalau bukan JSON)
    stem = re.sub(r"[^A-Za-z0-9_]", "_", Path(uploaded.name).stem)
    if not stem.startswith("entries"):
        stem = "entries_" + stem
    target = APP_DIR / f"{stem}.json"
    target.write_text(content, encoding="utf-8")
    load_user(target)
    return target.stem


# --------------------------------------------------------------------------
# INIT (satu fungsi saja -- perbaikan bug init ganda)
# --------------------------------------------------------------------------
def _load_entries():
    if STORE.exists():
        try:
            return json.loads(STORE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return [dict(e) for e in data.SEED_ENTRIES]


def init():
    ss = st.session_state
    ss.setdefault("page", "diary")
    ss.setdefault("model", data.DEFAULT_MODEL)
    ss.setdefault("selected", None)
    ss.setdefault("current_user", "entries")
    ss.setdefault("forecast_2a", None)
    if "entries" not in ss:                    # startup: tetap muat entries.json (settled)
        if STORE.exists():
            load_user(STORE)
        else:
            ss.entries = [dict(e) for e in data.SEED_ENTRIES]


def save():
    """Tulis entri user AKTIF ke file-nya (bukan selalu entries.json)."""
    cur = st.session_state.get("current_user", "entries")
    target = APP_DIR / f"{cur}.json"
    # jaga format: kalau file aslinya dict (punya forecast_2a), pertahankan
    if st.session_state.get("forecast_2a") is not None:
        payload = {"entries": st.session_state.entries,
                   "forecast_2a": st.session_state.forecast_2a}
    else:
        payload = st.session_state.entries
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                      encoding="utf-8")


def go(page):
    st.session_state.page = page
    st.rerun()


def open_entry(entry_id):
    st.session_state.selected = entry_id
    st.session_state.page = "detail"
    st.rerun()


def add_entry(text):
    ss = st.session_state
    new = {"id": f"new{len(ss.entries)}", "date": "2025-06-24",
           "day": "Tuesday", "text": text.strip()}
    ss.entries.insert(0, new)
    save()


def selected_entry():
    ss = st.session_state
    return next((e for e in ss.entries if e["id"] == ss.selected), None)
