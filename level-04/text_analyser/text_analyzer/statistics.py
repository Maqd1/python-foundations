"""Statistical analysis of text."""

from __future__ import annotations

from collections import Counter

from .tokenizer import word_tokenize, sentence_tokenize
from .utils import safe_divide


def get_character_count(text: str, include_spaces: bool = True) -> int:
    return len(text) if include_spaces else len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def get_word_count(text: str) -> int:
    return len(word_tokenize(text))


def get_avg_word_length(text: str) -> float:
    words = word_tokenize(text)
    if not words:
        return 0.0
    return safe_divide(sum(len(w) for w in words), len(words))


def get_avg_sentence_length(text: str) -> float:
    sentences = sentence_tokenize(text)
    if not sentences:
        return 0.0
    return safe_divide(get_word_count(text), len(sentences))


def get_lexical_diversity(text: str) -> float:
    words = word_tokenize(text)
    if not words:
        return 0.0
    return safe_divide(len(set(words)), len(words))


def get_word_length_distribution(text: str) -> dict[str, int]:
    """Buckets: 1-3, 4-6, 7-10, 10+."""
    buckets = {"1-3": 0, "4-6": 0, "7-10": 0, "10+": 0}
    for w in word_tokenize(text):
        n = len(w)
        if n <= 3:
            buckets["1-3"] += 1
        elif n <= 6:
            buckets["4-6"] += 1
        elif n <= 10:
            buckets["7-10"] += 1
        else:
            buckets["10+"] += 1
    return buckets


def get_letter_frequency(text: str) -> dict[str, int]:
    counts = Counter(ch.lower() for ch in text if ch.isalpha())
    return dict(sorted(counts.items(), key=lambda x: -x[1]))