"""Load checkpoint lokal
"""
import torch
import torch.nn as nn
import streamlit as st
from transformers import (RobertaModel, DebertaV2Model,
                          RobertaTokenizer, DebertaV2Tokenizer)
from peft import LoraConfig, get_peft_model

import config

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ========================= class model =========================
class MeanPooling(nn.Module):
    def forward(self, hidden, mask):
        m = mask.unsqueeze(-1).float()
        return torch.sum(hidden * m, 1) / m.sum(1).clamp(min=1e-9)


class TemporalEncoder(nn.Module):
    def __init__(self, phase_emb_dim=8, n_phases=8, out_dim=32):
        super().__init__()
        self.phase_emb = nn.Embedding(n_phases, phase_emb_dim, padding_idx=0)
        self.mlp = nn.Sequential(nn.Linear(5 + phase_emb_dim, out_dim), nn.ReLU(),
                                 nn.Linear(out_dim, out_dim))

    def forward(self, prev_v, prev_a, log_delta, is_words, is_first, phase_idx):
        p = self.phase_emb(phase_idx)
        s = torch.stack([prev_v, prev_a, log_delta, is_words, is_first], dim=1)
        return self.mlp(torch.cat([s, p], dim=1))


def _heads(hid):
    fusion = nn.Sequential(
        nn.Linear(hid + 64 + 32, 512), nn.GELU(), nn.LayerNorm(512), nn.Dropout(0.15),
        nn.Linear(512, 256), nn.GELU(), nn.LayerNorm(256), nn.Dropout(0.10))
    val = nn.Sequential(nn.Linear(256, 64), nn.GELU(), nn.Linear(64, 1))
    aro = nn.Sequential(nn.Linear(256, 64), nn.GELU(), nn.Linear(64, 1))
    return fusion, val, aro


class RobertaVAModel(nn.Module):
    def __init__(self, n_users, checkpoint="roberta-large"):
        super().__init__()
        base = RobertaModel.from_pretrained(checkpoint).to(torch.float32)
        cfg = LoraConfig(r=16, lora_alpha=32, target_modules=["query", "key", "value"],
                         lora_dropout=0.1, bias="none")
        self.encoder = get_peft_model(base, cfg)
        hid = self.encoder.config.hidden_size
        self.user_emb = nn.Embedding(n_users + 1, 64, padding_idx=0)
        self.temporal_enc = TemporalEncoder()
        self.pooling = MeanPooling()
        self.fusion, self.val_head, self.aro_head = _heads(hid)

    def forward(self, input_ids, attention_mask, user_idx,
                prev_v, prev_a, log_delta, is_words_f, is_first, phase_idx):
        enc = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        h = self.pooling(enc.last_hidden_state, attention_mask)
        e = self.user_emb(user_idx)
        c = self.temporal_enc(prev_v, prev_a, log_delta, is_words_f, is_first, phase_idx)
        f = self.fusion(torch.cat([h, e, c], dim=1))
        return self.val_head(f).squeeze(-1), self.aro_head(f).squeeze(-1)


class VAModel(nn.Module):
    def __init__(self, n_users, checkpoint="microsoft/deberta-v3-large"):
        super().__init__()
        base = DebertaV2Model.from_pretrained(checkpoint).to(torch.float32)
        cfg = LoraConfig(r=16, lora_alpha=32,
                         target_modules=["query_proj", "key_proj", "value_proj", "pos_proj"],
                         lora_dropout=0.1, bias="none")
        self.encoder = get_peft_model(base, cfg)
        hid = self.encoder.config.hidden_size
        self.user_emb = nn.Embedding(n_users + 1, 64, padding_idx=0)
        self.temporal_enc = TemporalEncoder()
        self.pooling = MeanPooling()
        self.fusion, self.val_head, self.aro_head = _heads(hid)

    def forward(self, input_ids, attention_mask, token_type_ids, user_idx,
                prev_v, prev_a, log_delta, is_words_f, is_first, phase_idx):
        enc = self.encoder(input_ids=input_ids, attention_mask=attention_mask,
                           token_type_ids=token_type_ids)
        h = self.pooling(enc.last_hidden_state, attention_mask)
        e = self.user_emb(user_idx)
        c = self.temporal_enc(prev_v, prev_a, log_delta, is_words_f, is_first, phase_idx)
        f = self.fusion(torch.cat([h, e, c], dim=1))
        return self.val_head(f).squeeze(-1), self.aro_head(f).squeeze(-1)


# ================================ load + infer ================================
@st.cache_resource(show_spinner="Loading model...")
def _load(model_id):
    spec = config.ROBERTA if model_id == "roberta" else config.DEBERTA
    ck = torch.load(spec["ckpt"], map_location=DEVICE, weights_only=False)
    n_users = ck.get("n_users") or max(ck["uid2idx"].values())
    if model_id == "roberta":
        model = RobertaVAModel(n_users, checkpoint=spec["base"])
        tok = RobertaTokenizer.from_pretrained(spec["base"])
    else:
        model = VAModel(n_users, checkpoint=spec["base"])
        tok = DebertaV2Tokenizer.from_pretrained(spec["base"])
    model.load_state_dict(ck["model_state"])
    model.to(DEVICE).eval()
    return model, tok


@torch.no_grad()
def infer_single(model_id, text):
    """Jalankan satu model pada teks baru (cold-start) -> (valence, arousal)."""
    model, tok = _load(model_id)
    enc = tok(text, truncation=True, padding="max_length", max_length=128,
              return_tensors="pt").to(DEVICE)
    z = lambda v: torch.tensor([float(v)], device=DEVICE)
    user_idx = torch.tensor([0], device=DEVICE)          # cold-start: user tak dikenal
    phase_idx = torch.tensor([0], device=DEVICE)
    # urutan sesuai forward: prev_v, prev_a, log_delta, is_words_f, is_first, phase_idx
    temporal = (z(0.0), z(0.0), z(0.0), z(0.0), z(1.0), phase_idx)
    if model_id == "roberta":
        v, a = model(enc["input_ids"], enc["attention_mask"], user_idx, *temporal)
    else:
        ttid = enc.get("token_type_ids", torch.zeros_like(enc["input_ids"]))
        v, a = model(enc["input_ids"], enc["attention_mask"], ttid, user_idx, *temporal)
    return float(v.squeeze()), float(a.squeeze())


def apply_isotonic(v, a):
    if not config.USE_ISOTONIC:
        return v, a
    iso_v = _load_iso(config.ISO_V_PATH)
    iso_a = _load_iso(config.ISO_A_PATH)
    return float(iso_v.predict([v])[0]), float(iso_a.predict([a])[0])


@st.cache_resource(show_spinner=False)
def _load_iso(path):
    import pickle
    return pickle.load(open(path, "rb"))