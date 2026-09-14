"""Classic readability formulas."""

from __future__ import annotations

from .tokenizer import word_tokenize, sentence_tokenize
from .utils import syllable_count, safe_divide


def _counts(text: str):
    words = word_tokenize(text)
    sentences = sentence_tokenize(text)
    syllables = sum(syllable_count(w) for w in words)
    complex_words = sum(1 for w in words if syllable_count(w) >= 3)
    return words, sentences, syllables, complex_words


def flesch_reading_ease(text: str) -> float:
    words, sentences, syllables, _ = _counts(text)
    if not words or not sentences:
        return 0.0
    asl = len(words) / len(sentences)
    asw = syllables / len(words)
    return round(206.835 - 1.015 * asl - 84.6 * asw, 2)


def flesch_kincaid_grade(text: str) -> float:
    words, sentences, syllables, _ = _counts(text)
    if not words or not sentences:
        return 0.0
    asl = len(words) / len(sentences)
    asw = syllables / len(words)
    return round(0.39 * asl + 11.8 * asw - 15.59, 2)


def gunning_fog_index(text: str) -> float:
    words, sentences, _, complex_words = _counts(text)
    if not words or not sentences:
        return 0.0
    asl = len(words) / len(sentences)
    pct_complex = complex_words / len(words)
    return round(0.4 * (asl + 100 * pct_complex), 2)


def coleman_liau_index(text: str) -> float:
    words, sentences, _, _ = _counts(text)
    if not words:
        return 0.0
    letters = sum(len(w) for w in words)
    L = letters / len(words) * 100
    S = len(sentences) / len(words) * 100
    return round(0.0588 * L - 0.296 * S - 15.8, 2)


def _fre_label(score: float) -> str:
    if score >= 90: return "Very Easy"
    if score >= 80: return "Easy"
    if score >= 70: return "Fairly Easy"
    if score >= 60: return "Plain English"
    if score >= 50: return "Fairly Difficult"
    if score >= 30: return "Difficult"
    return "Very Confusing"


def get_readability_summary(text: str) -> dict:
    fre = flesch_reading_ease(text)
    fk = flesch_kincaid_grade(text)
    gf = gunning_fog_index(text)
    cl = coleman_liau_index(text)
    return {
        "flesch_reading_ease": fre,
        "flesch_reading_ease_label": _fre_label(fre),
        "flesch_kincaid_grade": fk,
        "gunning_fog_index": gf,
        "coleman_liau_index": cl,
    }