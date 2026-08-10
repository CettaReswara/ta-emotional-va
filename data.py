"""Static data: model list + seed entries. One diary = one fixed owner,
so there's no persona / user-picker concept here.
"""

# Subtask 1 models that can be selected + compared
MODELS = ["roberta", "deberta", "ensemble"]
DEFAULT_MODEL = "ensemble"


def model_label(m):
    return {"roberta": "RoBERTa", "deberta": "DeBERTa",
            "ensemble": "Ensemble (RoBERTa + DeBERTa)"}.get(m, m)


# Seed is used when entries.json doesn't exist yet. V/A left empty on purpose:
# computed & cached on first display.
SEED_ENTRIES = [
    {"id": "e1", "date": "2025-06-23", "day": "Monday",
     "text": "Deadlines piling up, hard to focus all day. I want everything done fast but my body is exhausted."},
    {"id": "e2", "date": "2025-06-22", "day": "Sunday",
     "text": "Morning walk then read a book, so peaceful."},
    {"id": "e3", "date": "2025-06-21", "day": "Saturday",
     "text": "Met an old friend, fun and lively!"},
    {"id": "e4", "date": "2025-06-20", "day": "Friday",
     "text": "Tired and a bit lonely, I just want to rest."},
    {"id": "e5", "date": "2025-06-19", "day": "Thursday",
     "text": "A flat day, nothing special."},
    {"id": "e6", "date": "2025-06-18", "day": "Wednesday",
     "text": "Pretty productive, relieved to finish my tasks."},
    {"id": "e7", "date": "2025-06-17", "day": "Tuesday",
     "text": "Nervous waiting for the announcement, couldn't sit still."},
]
