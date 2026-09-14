"""Shared constants, data loading, and small helpers."""

from __future__ import annotations

import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---- Built-in fallbacks so the package works without data files ----
DEFAULT_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "of", "to",
    "in", "on", "at", "by", "for", "with", "about", "as", "into", "like",
    "through", "after", "over", "between", "out", "against", "during",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those", "there", "here",
    "not", "no", "nor", "only", "own", "same", "too", "very",
}

DEFAULT_POSITIVE = {
    "good", "great", "excellent", "amazing", "wonderful", "fantastic",
    "happy", "joy", "love", "like", "best", "better", "awesome", "nice",
    "positive", "success", "successful", "win", "winning", "bright",
    "beautiful", "brilliant", "perfect", "enjoy", "enjoyed", "delight",
}

DEFAULT_NEGATIVE = {
    "bad", "terrible", "awful", "horrible", "hate", "dislike", "worst",
    "worse", "sad", "angry", "fear", "afraid", "negative", "failure",
    "fail", "failed", "lose", "losing", "loss", "ugly", "stupid",
    "problem", "problems", "error", "errors", "wrong", "broken",
}


def _load_wordlist(filename: str, fallback: set[str]) -> set[str]:
    path = DATA_DIR / filename
    if not path.exists():
        return set(fallback)
    words = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if line and not line.startswith("#"):
                words.add(line)
    return words or set(fallback)


def load_stopwords() -> set[str]:
    return _load_wordlist("stopwords.txt", DEFAULT_STOPWORDS)


def load_positive_words() -> set[str]:
    return _load_wordlist("positive_words.txt", DEFAULT_POSITIVE)


def load_negative_words() -> set[str]:
    return _load_wordlist("negative_words.txt", DEFAULT_NEGATIVE)


# ---- Simple helpers ----
_WORD_RE = re.compile(r"[A-Za-z']+")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
_PARAGRAPH_RE = re.compile(r"\n\s*\n")


def is_word(token: str) -> bool:
    return bool(_WORD_RE.fullmatch(token))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    return numerator / denominator if denominator else default


def syllable_count(word: str) -> int:
    """Approximate English syllable count."""
    word = word.lower()
    if not word:
        return 0
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_v = ch in vowels
        if is_v and not prev_vowel:
            count += 1
        prev_vowel = is_v
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)