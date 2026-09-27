
import string

SAMPLE_TEXT = """
Python is a programming language that lets you work quickly
and integrate systems more effectively. Python is powerful
and fast. Python plays well with others. Python runs everywhere.
"""


def clean_text(text):
    """Lowercases and strips punctuation using string.translate — a string method,
    not a manual loop — so punctuation-stuck words like 'fast.' become 'fast'."""
    lowered = text.lower()
    return lowered.translate(str.maketrans("", "", string.punctuation))


def get_words(text):
    """Shared helper: cleaned text split into a list of words (order & duplicates kept)."""
    return clean_text(text).split()


def word_frequency(text):
    words = get_words(text)
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def unique_words(text):
    return set(get_words(text))


def most_common_words(text, n):
    """Returns the n most frequent (word, count) pairs, most frequent first."""
    freq = word_frequency(text)
    return sorted(freq.items(), key=lambda item: item[1], reverse=True)[:n]


def words_by_length(text, min_len, max_len):
    return [word for word in get_words(text) if min_len <= len(word) <= max_len]


def frequency_percentages(word_freq):
    total = sum(word_freq.values())
    if total == 0:
        return {}
    return {word: (count / total) * 100 for word, count in word_freq.items()}


def word_pairs(text, n):
    """Returns the n most common adjacent word pairs (bigrams)."""
    words = get_words(text)
    pairs = [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]

    pair_freq = {}
    for pair in pairs:
        pair_freq[pair] = pair_freq.get(pair, 0) + 1

    return sorted(pair_freq.items(), key=lambda item: item[1], reverse=True)[:n]


def longest_and_shortest_word(text):
    """Extra Challenge 1."""
    words = get_words(text)
    if not words:
        return None, None
    return max(words, key=len), min(words, key=len)


def words_appearing_once(word_freq):
    """Extra Challenge 2."""
    return [word for word, count in word_freq.items() if count == 1]


def print_word_cloud(word_freq, top_n=10):
    """Extra Challenge 3 — text-based bar chart, most frequent words first."""
    top_items = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:top_n]
    if not top_items:
        print("(no words to show)")
        return
    label_width = max(len(word) for word, _ in top_items)
    for word, count in top_items:
        bar = "#" * count
        print(f"{word.ljust(label_width)}  {bar} ({count})")


def analyze(text):
    words = get_words(text)
    freq = word_frequency(text)
    unique = unique_words(text)

    print("\n\U0001f4ca WORD FREQUENCY ANALYZER \U0001f4ca")
    print(f"\nOriginal text length: {len(text)} characters")
    print(f"Words: {len(words)}")
    print(f"Unique words: {len(unique)}")

    if not words:
        print("\nNo words to analyze.")
        return

    pct = frequency_percentages(freq)
    top_words = most_common_words(text, 4)
    print("\n\U0001f4c8 MOST COMMON WORDS:")
    for i, (word, count) in enumerate(top_words, start=1):
        print(f"{i}. {word} ({count} times) - {pct[word]:.1f}%")

    avg_len = sum(len(w) for w in words) / len(words)
    longest, shortest = longest_and_shortest_word(text)
    print("\n\U0001f524 WORD STATISTICS:")
    print(f"Average word length: {avg_len:.1f}")
    print(f"Longest word: \"{longest}\" ({len(longest)} characters)")
    plural = "s" if len(shortest) != 1 else ""
    print(f"Shortest word: \"{shortest}\" ({len(shortest)} character{plural})")

    once = words_appearing_once(freq)
    print("\n\U0001f3f7\ufe0f  WORDS APPEARING ONCE:")
    print(f"[{', '.join(once)}]" if once else "(none)")

    pairs = word_pairs(text, 3)
    print("\n\U0001f517 TOP 3 WORD PAIRS:")
    for i, (pair, count) in enumerate(pairs, start=1):
        label = "time" if count == 1 else "times"
        print(f"{i}. \"{pair}\" - {count} {label}")

    print("\n\U0001f4ca FREQUENCY DISTRIBUTION:")
    print_word_cloud(freq, top_n=5)


def get_input_text():
    print("1. Use sample text")
    print("2. Type your own text")
    print("3. Load from a file")
    choice = input("Choice: ").strip()

    if choice == "2":
        return input("Enter your text: ")
    elif choice == "3":
        path = input("Enter file path: ").strip()
        try:
            with open(path, "r") as f:
                return f.read()
        except OSError as e:
            print(f"\u274c Could not read file: {e}")
            return None
    else:
        return SAMPLE_TEXT


def main():
    text = get_input_text()
    if text is None or not text.strip():
        print("No text to analyze.")
        return
    analyze(text)


if __name__ == "__main__":
    main()