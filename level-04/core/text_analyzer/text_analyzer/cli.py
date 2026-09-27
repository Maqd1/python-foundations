"""Command-line interface for the text analyzer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import TextAnalyzer
from .utils import safe_divide


# ---- Optional visualization (skipped gracefully if matplotlib missing) ----
def _try_import_matplotlib():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except Exception:
        return None


def _bar(label: str, pct: float, width: int = 20) -> str:
    filled = int(round(pct / 100 * width))
    return "█" * filled


def print_results(result: dict, file_name: str) -> None:
    print("\n📊 TEXT ANALYZER v1.0 📊\n")
    print(f"File: {file_name}")
    counts = result["counts"]
    print(f"Length: {counts['words']:,} words | "
          f"{counts['sentences']} sentences | "
          f"{counts['paragraphs']} paragraphs\n")

    # ---- Statistics ----
    print("📈 STATISTICS:")
    print(f"Total characters: {result['characters']['with_spaces']:,} "
          f"({result['characters']['without_spaces']:,} without spaces)")
    print(f"Average word length: {result['averages']['word_length']} characters")
    print(f"Average sentence length: {result['averages']['sentence_length']} words")
    print(f"Lexical diversity: {result['lexical_diversity']} "
          f"({counts['unique_words']} unique words)\n")

    # ---- Word length distribution ----
    print("📊 WORD LENGTH DISTRIBUTION:")
    dist = result["word_length_distribution"]
    total = sum(dist.values()) or 1
    for bucket in ("1-3", "4-6", "7-10", "10+"):
        n = dist.get(bucket, 0)
        pct = n / total * 100
        print(f"{bucket:>5} chars: {_bar(bucket, pct)} {pct:.0f}%")
    print()

    # ---- Most common words ----
    print("📝 MOST COMMON WORDS:")
    for i, (word, cnt) in enumerate(result["most_common_words"], 1):
        print(f'{i}. "{word}" ({cnt} times)')
    print()

    # ---- Sentiment ----
    s = result["sentiment"]
    print("🧠 SENTIMENT ANALYSIS:")
    sign = "+" if s["score"] >= 0 else ""
    print(f"Sentiment: {s['label']} ({sign}{s['score']})")
    print(f"Confidence: {s['confidence']:.2f}")
    print("Emotional breakdown:")
    for emotion, val in sorted(result["emotions"].items(), key=lambda x: -x[1]):
        if val > 0:
            print(f"  {emotion.capitalize()}: {val:.2f}")
    print()

    # ---- Readability ----
    r = result["readability"]
    print("📖 READABILITY SCORES:")
    print(f"Flesch Reading Ease: {r['flesch_reading_ease']} ({r['flesch_reading_ease_label']})")
    print(f"Flesch-Kincaid Grade: {r['flesch_kincaid_grade']}")
    print(f"Gunning Fog Index: {r['gunning_fog_index']}")
    print(f"Coleman-Liau Index: {r['coleman_liau_index']}\n")

    # ---- Summary ----
    summ = result["summary"]
    print(f"📝 TEXT SUMMARY ({int(summ['compression']*100)}% compression):")
    print(f"Original: {summ['original_word_count']} words")
    print(f"Summary: {summ['summary_word_count']} words")
    print("Key points:")
    for i, s in enumerate(summ["sentences"][:3], 1):
        snippet = (s[:80] + "...") if len(s) > 80 else s
        print(f"{i}. {snippet}")
    print()

    # ---- Keywords ----
    print(f"🏷️ KEYWORDS (Top {len(result['keywords'])}):")
    print(", ".join(result["keywords"]))
    print()


def create_charts(result: dict, out_dir: Path) -> dict:
    """Generate PNG charts if matplotlib is available. Returns {name: path}."""
    plt = _try_import_matplotlib()
    if plt is None:
        return {}

    out_dir.mkdir(parents=True, exist_ok=True)
    files = {}

    # Word length distribution
    fig, ax = plt.subplots(figsize=(6, 4))
    dist = result["word_length_distribution"]
    ax.bar(list(dist.keys()), list(dist.values()), color="#4C72B0")
    ax.set_title("Word Length Distribution")
    ax.set_ylabel("Count")
    p = out_dir / "word_length_distribution.png"
    fig.tight_layout(); fig.savefig(p); plt.close(fig)
    files["word_length_distribution"] = str(p)

    # Top 10 common words
    top = result["most_common_words"][:10]
    if top:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh([w for w, _ in top][::-1], [c for _, c in top][::-1], color="#55A868")
        ax.set_title("Top 10 Words")
        p = out_dir / "top_words.png"
        fig.tight_layout(); fig.savefig(p); plt.close(fig)
        files["top_words"] = str(p)

    # Readability radar-ish bar
    r = result["readability"]
    labels = ["Flesch\nEase", "F-K\nGrade", "Gunning\nFog", "Coleman\nLiau"]
    vals = [r["flesch_reading_ease"], r["flesch_kincaid_grade"],
            r["gunning_fog_index"], r["coleman_liau_index"]]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, vals, color="#C44E52")
    ax.set_title("Readability Scores")
    p = out_dir / "readability.png"
    fig.tight_layout(); fig.savefig(p); plt.close(fig)
    files["readability"] = str(p)

    # Sentiment timeline
    timeline = result["sentiment_breakdown"]["sentences"]
    if timeline:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(range(1, len(timeline) + 1), [t["score"] for t in timeline],
                marker="o", color="#8172B2")
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.set_xlabel("Sentence #")
        ax.set_ylabel("Sentiment")
        ax.set_title("Sentiment Over Text")
        p = out_dir / "sentiment_timeline.png"
        fig.tight_layout(); fig.savefig(p); plt.close(fig)
        files["sentiment_timeline"] = str(p)

    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="text-analyzer",
        description="Analyze a text file: statistics, sentiment, readability, summary.",
    )
    parser.add_argument("file", help="Text file to analyze")
    parser.add_argument("--sentiment", action="store_true", help="Only show sentiment")
    parser.add_argument("--readability", action="store_true", help="Only show readability")
    parser.add_argument("--summary", action="store_true", help="Only show summary")
    parser.add_argument("--export", metavar="OUT.json", help="Export full results to JSON")
    parser.add_argument("--charts", metavar="DIR", help="Generate PNG charts into DIR")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if not path.exists():
        print(f"❌ File not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    analyzer = TextAnalyzer()
    result = analyzer.analyze(text)

    if args.sentiment:
        print(json.dumps(result["sentiment"], indent=2))
    elif args.readability:
        print(json.dumps(result["readability"], indent=2))
    elif args.summary:
        print(result["summary"]["summary"])
    else:
        print_results(result, path.name)

    if args.charts:
        charts = create_charts(result, Path(args.charts))
        if charts:
            print("☁️ Charts generated:")
            for name, p in charts.items():
                print(f"  {name}: {p}")
        else:
            print("⚠️  matplotlib not installed; skipping charts.")

    if args.export:
        Path(args.export).write_text(
            json.dumps(result, indent=2, default=str), encoding="utf-8"
        )
        print(f"✅ Results saved to {args.export}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())