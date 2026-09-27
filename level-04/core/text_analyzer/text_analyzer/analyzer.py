"""High-level TextAnalyzer that ties everything together."""

from __future__ import annotations

from collections import Counter

from . import statistics as stats
from .tokenizer import word_tokenize, sentence_tokenize, clean_text
from .utils import _PARAGRAPH_RE, load_stopwords
from .sentiment import analyze_sentiment, calculate_sentiment_score, get_sentiment_breakdown, analyze_emotions
from .readability import get_readability_summary
from .summarizer import extractive_summarize, keyword_extraction, get_ngrams


class TextAnalyzer:
    def __init__(self, stopwords: set[str] | None = None):
        self.stopwords = stopwords if stopwords is not None else load_stopwords()

    # ----- Core -----
    def analyze(self, text: str) -> dict:
        return {
            "characters": {
                "with_spaces": stats.get_character_count(text, True),
                "without_spaces": stats.get_character_count(text, False),
            },
            "counts": {
                "words": stats.get_word_count(text),
                "sentences": self.get_sentence_count(text),
                "paragraphs": self.get_paragraph_count(text),
                "unique_words": len(set(word_tokenize(text))),
            },
            "averages": {
                "word_length": round(stats.get_avg_word_length(text), 2),
                "sentence_length": round(stats.get_avg_sentence_length(text), 2),
            },
            "lexical_diversity": round(stats.get_lexical_diversity(text), 3),
            "word_length_distribution": stats.get_word_length_distribution(text),
            "letter_frequency": stats.get_letter_frequency(text),
            "most_common_words": self.get_most_common_words(text, 10),
            "longest_words": self.get_longest_words(text, 5),
            "sentiment": analyze_sentiment(text),
            "sentiment_score": calculate_sentiment_score(text),
            "sentiment_breakdown": get_sentiment_breakdown(text),
            "emotions": analyze_emotions(text),
            "readability": get_readability_summary(text),
            "summary": extractive_summarize(text, ratio=0.3),
            "keywords": keyword_extraction(text, 10),
            "bigrams": get_ngrams(text, 2, top=10),
        }

    def get_word_frequency(self, text: str) -> dict[str, int]:
        words = word_tokenize(text)
        return dict(Counter(words).most_common())

    def get_sentence_count(self, text: str) -> int:
        return len(sentence_tokenize(text))

    def get_paragraph_count(self, text: str) -> int:
        blocks = [b for b in _PARAGRAPH_RE.split(text.strip()) if b.strip()]
        return len(blocks) if blocks else (1 if text.strip() else 0)

    def get_longest_words(self, text: str, n: int = 5) -> list[str]:
        words = {w for w in word_tokenize(text) if w not in self.stopwords}
        return sorted(words, key=lambda w: (-len(w), w))[:n]

    def get_most_common_words(self, text: str, n: int = 10) -> list[tuple[str, int]]:
        words = [w for w in word_tokenize(text) if w not in self.stopwords]
        return Counter(words).most_common(n)


def analyze(text: str) -> dict:
    """Convenience function."""
    return TextAnalyzer().analyze(text)