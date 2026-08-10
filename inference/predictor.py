"""Lapisan inferensi. Halaman cukup panggil predict_for_entry(entry, model).

Dua implementasi:
  - MockPredictor : palsu deterministik, tanpa dependensi model. Default.
  - RealPredictor : weighted ensemble RoBERTa + DeBERTa (post-processing di sini).

predict_for_entry() meng-CACHE hasil ke entries.json: model hanya jalan untuk
entri yang belum punya V/A pada model itu. Sisanya dibaca dari file.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass

import streamlit as st

import config


@dataclass
class Prediction:
    valence: float   # ternormalisasi [-1, 1]
    arousal: float   # ternormalisasi [-1, 1]

    @property
    def quadrant(self):
        return config.quadrant(self.valence, self.arousal)


def _clip(x):
    return max(-1.0, min(1.0, float(x)))


class MockPredictor:
    """Stand-in stabil dari hash teks + sedikit cue kata. BUKAN model asli;
    jangan pernah dipakai sebagai angka yang dilaporkan."""

    POS = ("seru", "lega", "produktif", "tenang", "senang", "baca")
    NEG = ("capek", "sepi", "susah", "numpuk", "sedih", "deadline", "pusing")
    HI = ("deadline", "deg-degan", "susah", "rame", "numpuk", "pusing")
    LO = ("tenang", "istirahat", "lega", "baca", "datar", "biasa")

    def predict(self, text, model=None):
        h = hashlib.sha256((text or "").encode("utf-8")).digest()
        v = (h[0] / 255) * 2 - 1
        a = (h[1] / 255) * 2 - 1
        low = (text or "").lower()
        if any(w in low for w in self.POS): v = abs(v) * 0.7 + 0.15
        if any(w in low for w in self.NEG): v = -abs(v) * 0.7 - 0.15
        if any(w in low for w in self.HI): a = abs(a) * 0.7 + 0.20
        if any(w in low for w in self.LO): a = -abs(a) * 0.7 - 0.10
        return Prediction(round(_clip(v), 2), round(_clip(a), 2))


class RealPredictor:
    """Weighted ensemble RoBERTa + DeBERTa. Post-processing (denorm, fusion,
    isotonic) terjadi DI SINI -- harus sama persis dengan notebook."""

    def predict(self, text, model="ensemble"):
        from inference.model_loader import infer_single, apply_isotonic

        if model == "ensemble":
            vr, ar = infer_single("roberta", text)   # sudah ter-denorm ke [-1,1]
            vd, ad = infer_single("deberta", text)
            w = config.ENSEMBLE_WEIGHTS
            v = w["roberta"] * vr + w["deberta"] * vd  # FUSION
            a = w["roberta"] * ar + w["deberta"] * ad
        else:
            v, a = infer_single(model, text)

        if config.USE_ISOTONIC:                        # ISOTONIC (kalau ada)
            v, a = apply_isotonic(v, a)

        return Prediction(round(_clip(v), 2), round(_clip(a), 2))


@st.cache_resource(show_spinner=False)
def get_predictor():
    return MockPredictor() if config.USE_MOCK else RealPredictor()


def predict_for_entry(entry, model):
    """Ambil hasil tersimpan kalau ada; kalau belum, hitung sekali lalu cache.
    Caching ke file hanya saat model asli (mock tak perlu di-persist)."""
    cached = (entry.get("subtask1") or {}).get(model)
    if cached:
        return Prediction(cached["valence"], cached["arousal"])

    pred = get_predictor().predict(entry["text"], model)

    if not config.USE_MOCK:
        entry.setdefault("subtask1", {})[model] = {
            "valence": pred.valence, "arousal": pred.arousal}
        import state
        state.save()
    return pred