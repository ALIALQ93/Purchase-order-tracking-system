"""Arabic / mixed text normalization for material name matching."""

from __future__ import annotations

import re
import unicodedata

_ARABIC_DIACRITICS = re.compile(r"[\u0617-\u061A\u064B-\u0652\u0670\u0640]")
_NON_WORD = re.compile(r"[^\w\s]", flags=re.UNICODE)
_SPACES = re.compile(r"\s+")


def normalize_material_text(text: str) -> str:
    if not text:
        return ""
    s = str(text).strip()
    s = _ARABIC_DIACRITICS.sub("", s)
    s = unicodedata.normalize("NFKC", s)
    for ch in "أإآٱ":
        s = s.replace(ch, "ا")
    s = s.replace("ة", "ه")
    s = s.replace("ى", "ي")
    s = s.lower()
    s = _NON_WORD.sub(" ", s)
    s = _SPACES.sub(" ", s).strip()
    return s


def normalize_unit(unit: str) -> str:
    u = normalize_material_text(unit or "")
    aliases = {
        "pcs": "pcs",
        "piece": "pcs",
        "pieces": "pcs",
        "قطعه": "pcs",
        "قطع": "pcs",
        "bag": "bag",
        "bags": "bag",
        "كيس": "bag",
        "اكياس": "bag",
        "ton": "ton",
        "tons": "ton",
        "طن": "ton",
        "m": "m",
        "meter": "m",
        "meters": "m",
        "متر": "m",
        "m2": "m2",
        "m3": "m3",
        "kg": "kg",
        "kilo": "kg",
        "كغ": "kg",
        "كيلو": "kg",
    }
    return aliases.get(u, u or "—")
