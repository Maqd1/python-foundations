"""Tokenization and text cleaning."""

from __future__ import annotations

import re
import string

from .utils import _WORD_RE, _SENTENCE_RE, load_stopwords


def clean_text(text: str, lowercase: bool = True) -> str:
    """Normalize whitespace and remove stray control characters."""
    if lowercase:
        text = text.lower()
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_tokenize(text: str, lowercase: bool = True) -> list[str]:
    """Split text into words, keeping apostrophes."""
    if lowercase:
        text = text.lower()
    return _WORD_RE.findall(text)


def sentence_tokenize(text: str) -> list[str]:
    """Split text into sentences."""
    text = text.strip()
    if not text:
        return []
    parts = _SENTENCE_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def remove_stopwords(text: str, language: str = "english") -> str:
    """Remove stopwords, preserving the rest of the text roughly intact."""
    # (language param exists for API compatibility; only english is loaded)
    stops = load_stopwords()
    tokens = word_tokenize(text, lowercase=False)
    kept = [t for t in tokens if t.lower() not in stops]
    return " ".join(kept)


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))