"""Extractive summarization, keywords, n-grams."""

from __future__ import annotations

import math
from collections import Counter

from .tokenizer import word_tokenize, sentence_tokenize
from .utils import load_stopwords, safe_divide

_STOPS = load_stopwords()


def keyword_extraction(text: str, n: int = 10) -> list[str]:
    """Top content words by frequency, weighted by length."""
    words = [w for w in word_tokenize(text) if w not in _STOPS and len(w) > 2]
    if not words:
        return []
    counts = Counter(words)
    scored = [(w, c * (1 + math.log(len(w)))) for w, c in counts.items()]
    scored.sort(key=lambda x: -x[1])
    return [w for w, _ in scored[:n]]


def get_ngrams(text: str, n: int = 2, top: int = 10) -> list[tuple[tuple[str, ...], int]]:
    """Return top-n most frequent n-grams as (tuple, count)."""
    words = word_tokenize(text)
    if len(words) < n:
        return []
    grams = [tuple(words[i:i + n]) for i in range(len(words) - n + 1)]
    return Counter(grams).most_common(top)


def _sentence_scores(sentences: list[str]) -> list[float]:
    """Score sentences by content-word frequency (TextRank-lite)."""
    word_freq: Counter = Counter()
    for s in sentences:
        for w in word_tokenize(s):
            if w not in _STOPS and len(w) > 2:
                word_freq[w] += 1

    if not word_freq:
        return [0.0] * len(sentences)

    max_freq = max(word_freq.values())
    for w in word_freq:
        word_freq[w] /= max_freq

    scores = []
    for s in sentences:
        words = [w for w in word_tokenize(s) if w not in _STOPS and len(w) > 2]
        if not words:
            scores.append(0.0)
            continue
        score = sum(word_freq[w] for w in words) / len(words)
        # Bonus for early position
        scores.append(score)
    return scores


def get_sentence_importance(text: str) -> list[dict]:
    """Return every sentence with its importance score, sorted desc."""
    sentences = sentence_tokenize(text)
    scores = _sentence_scores(sentences)
    out = [
        {"sentence": s, "score": round(sc, 4), "index": i}
        for i, (s, sc) in enumerate(zip(sentences, scores))
    ]
    out.sort(key=lambda x: -x["score"])
    return out


def extractive_summarize(text: str, ratio: float = 0.3) -> dict:
    """Return top-N sentences (preserving original order) as the summary."""
    sentences = sentence_tokenize(text)
    if not sentences:
        return {"summary": "", "sentences": [], "original_word_count": 0, "summary_word_count": 0}

    ranked = get_sentence_importance(text)
    k = max(1, int(round(len(sentences) * max(0.05, min(ratio, 1.0)))))

    chosen_indices = sorted(item["index"] for item in ranked[:k])
    chosen = [sentences[i] for i in chosen_indices]

    return {
        "summary": " ".join(chosen),
        "sentences": chosen,
        "original_word_count": len(word_tokenize(text)),
        "summary_word_count": len(word_tokenize(" ".join(chosen))),
        "compression": round(safe_divide(len(chosen), len(sentences)), 3),
    }