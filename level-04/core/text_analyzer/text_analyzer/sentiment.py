"""Lexicon-based sentiment and emotion analysis."""

from __future__ import annotations

from collections import Counter

from .tokenizer import word_tokenize, sentence_tokenize
from .utils import (
    load_positive_words, load_negative_words,
    safe_divide, DEFAULT_POSITIVE, DEFAULT_NEGATIVE,
)

_POS = load_positive_words()
_NEG = load_negative_words()

# Negation words flip polarity for the next few tokens
_NEGATORS = {"not", "no", "never", "without", "n't", "cannot", "can't", "don't", "doesn't", "didn't"}

# Simple emotion lexicons
_EMOTION_LEXICON = {
    "joy":     {"happy", "joy", "delight", "love", "wonderful", "great", "excited", "smile", "laugh"},
    "trust":   {"trust", "reliable", "safe", "secure", "honest", "faith", "believe", "confident"},
    "anticipation": {"soon", "will", "expect", "hope", "future", "plan", "prepare", "looking"},
    "sadness": {"sad", "unhappy", "cry", "tears", "loss", "miss", "alone", "sorrow", "grief"},
    "anger":   {"angry", "mad", "furious", "rage", "hate", "annoyed", "irritated", "upset"},
    "fear":    {"fear", "afraid", "scared", "terrified", "worried", "anxious", "panic", "dread"},
    "surprise": {"surprise", "sudden", "unexpected", "amazed", "astonished", "shocked", "wow"},
    "disgust": {"disgust", "gross", "nasty", "awful", "horrible", "repulsive", "yuck"},
}


def _score_tokens(tokens: list[str]) -> tuple[int, int]:
    """Return (pos, neg) counts, honoring simple negation."""
    pos = neg = 0
    for i, tok in enumerate(tokens):
        # Look back up to 3 tokens for a negator
        window = tokens[max(0, i - 3):i]
        negated = any(w in _NEGATORS for w in window)

        if tok in _POS:
            if negated:
                neg += 1
            else:
                pos += 1
        elif tok in _NEG:
            if negated:
                pos += 1
            else:
                neg += 1
    return pos, neg


def calculate_sentiment_score(text: str) -> float:
    """Score in [-1, 1]."""
    tokens = word_tokenize(text)
    if not tokens:
        return 0.0
    pos, neg = _score_tokens(tokens)
    total = pos + neg
    if total == 0:
        return 0.0
    return round((pos - neg) / total, 3)


def analyze_sentiment(text: str) -> dict:
    score = calculate_sentiment_score(text)
    tokens = word_tokenize(text)
    pos, neg = _score_tokens(tokens)
    total = pos + neg

    if total == 0:
        label = "NEUTRAL"
        confidence = 0.0
    elif score > 0.05:
        label = "POSITIVE"
        confidence = round(min(1.0, 0.5 + abs(score) * 0.6), 2)
    elif score < -0.05:
        label = "NEGATIVE"
        confidence = round(min(1.0, 0.5 + abs(score) * 0.6), 2)
    else:
        label = "NEUTRAL"
        confidence = 0.5

    return {
        "label": label,
        "score": score,
        "confidence": confidence,
        "positive_hits": pos,
        "negative_hits": neg,
    }


def get_sentiment_breakdown(text: str) -> dict:
    """Per-sentence sentiment timeline (useful for charts)."""
    sentences = sentence_tokenize(text)
    return {
        "overall_score": calculate_sentiment_score(text),
        "sentences": [
            {"text": s, "score": calculate_sentiment_score(s)}
            for s in sentences
        ],
    }


def analyze_emotions(text: str) -> dict[str, float]:
    """Return normalized scores (0-1) for each emotion."""
    tokens = word_tokenize(text)
    if not tokens:
        return {e: 0.0 for e in _EMOTION_LEXICON}

    counts = {e: 0 for e in _EMOTION_LEXICON}
    for tok in tokens:
        for emotion, words in _EMOTION_LEXICON.items():
            if tok in words:
                counts[emotion] += 1

    total = sum(counts.values()) or 1
    # Bias toward 0 so small samples don't look extreme
    return {e: round(c / total, 3) for e, c in counts.items()}