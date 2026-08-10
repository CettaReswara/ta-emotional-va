"""
Mock = True  -> app run no model.
Mock = False -> load local checkpoint (inference/model_loader.py).
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# MODE
# ---------------------------------------------------------------------------
USE_MOCK = False   

# ---------------------------------------------------------------------------
#  .pt in assets/
# ---------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"

ROBERTA = {"base": "roberta-large",
           "ckpt": ASSETS_DIR / "rich_roberta_seed456.pt"}    
DEBERTA = {"base": "microsoft/deberta-v3-large",
           "ckpt": ASSETS_DIR / "seeds_deberta_seed456.pt"}   

# Ensemble
ENSEMBLE_WEIGHTS = {"roberta": 0.89, "deberta": 0.11}             

# Isotonic calibration
USE_ISOTONIC = False
ISO_V_PATH = ASSETS_DIR / "iso_v.pkl"
ISO_A_PATH = ASSETS_DIR / "iso_a.pkl"

# ---------------------------------------------------------------------------
# SKALA V & A
# ---------------------------------------------------------------------------
VAL_MIN, VAL_MAX = -2.0, 2.0      
ARO_MIN, ARO_MAX = 0.0, 2.0      
SHOW_NORMALIZED = False    

# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
PALETTE = {
    "vanilla":  "#FFF7E6",
    "blush":    "#F7C8D3",
    "rosewood": "#B46A72",
    "sage":     "#A8B58A",
    "sky":      "#A9B7C6",
    "sky_deep": "#8FA1B3",
    "midnight": "#2D3A47",
    "white":    "#FFFFFF",
}
VALENCE_COLOR = PALETTE["sky_deep"]
AROUSAL_COLOR = PALETTE["rosewood"]

QUADRANTS = {
    ("pos", "hi"): ("Excited", "blush"),
    ("neg", "hi"): ("Tense",   "rosewood"),
    ("neg", "lo"): ("Sad",     "sky"),
    ("pos", "lo"): ("Calm",    "sage"),
}


def quadrant(valence: float, arousal: float):
    vk = "pos" if valence >= 0 else "neg"
    ak = "hi" if arousal >= 0 else "lo"
    return QUADRANTS[(vk, ak)]


def _denorm(x, lo, hi):
    return lo + (x + 1) / 2 * (hi - lo)


def fmt_v(x: float) -> str:        
    if SHOW_NORMALIZED:
        return f"{x:+.2f}"
    return f"{_denorm(x, VAL_MIN, VAL_MAX):+.1f}"


def fmt_a(x: float) -> str:       
    if SHOW_NORMALIZED:
        return f"{x:+.2f}"
    return f"{_denorm(x, ARO_MIN, ARO_MAX):.1f}"


def fmt(x: float) -> str:           
    return fmt_v(x)
