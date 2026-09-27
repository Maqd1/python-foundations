# 📊 Word Frequency Analyzer

## Q6 — The Word Frequency Analyzer (Hard)

Write a program that analyzes text using **sets, dictionaries, comprehensions, string methods, sorting, and complex data manipulation**.

The program should examine a piece of text and produce useful statistics about its words and their frequencies.

---

# 📝 1. Input Text

The program should accept a long text input or read text from a file.

Example:

```python
text = """
Python is a programming language that lets you work quickly
and integrate systems more effectively. Python is powerful
and fast. Python plays well with others. Python runs everywhere.
"""
```

---

# ⚙️ 2. Required Functions

### `clean_text(text)`

Clean the input text by:

* Converting it to lowercase.
* Removing punctuation.

The function should return the cleaned text.

---

### `word_frequency(text)`

Count how many times each word appears.

Return a dictionary in the form:

```python
{
    "python": 4,
    "is": 3,
    "a": 1
}
```

---

### `unique_words(text)`

Return a **set** containing every unique word in the text.

---

### `most_common_words(text, n)`

Return the top `n` most frequently occurring words.

The results should be ordered from most common to least common.

---

### `words_by_length(text, min_len, max_len)`

Return a list of words whose lengths fall within the specified range.

---

### `frequency_percentages(word_freq)`

Convert word frequencies into percentages.

Return a dictionary such as:

```python
{
    "python": 14.3,
    "is": 10.7
}
```

---

### `word_pairs(text, n)`

Find the `n` most common pairs of consecutive words, also known as **bigrams**.

For example:

```text
Python is
is a
a programming
```

Count how many times each pair occurs and return the most common pairs.

---

# ⭐ 3. Extra Challenge 1 — Longest and Shortest Words

Find:

* The longest word.
* The shortest word.
* The length of each.

---

# ⭐ 4. Extra Challenge 2 — Words Appearing Once

Find every word that appears **exactly once** in the text.

These are sometimes called words with a frequency of one.

---

# ⭐ 5. Extra Challenge 3 — Text-Based Word Cloud

Create a simple text-based word cloud.

The frequency of a word should determine how many symbols are displayed beside it.

For example:

```text
Python    #### (4)
is        ###  (3)
works     ##   (2)
with      ##   (2)
a         #    (1)
```

---

# 🖥️ Sample Output

```text
📊 WORD FREQUENCY ANALYZER 📊

Original text length: 123 characters
Words: 28
Unique words: 18

📈 MOST COMMON WORDS:
1. Python (4 times) - 14.3%
2. is (3 times) - 10.7%
3. works (2 times) - 7.1%
4. with (2 times) - 7.1%

🔤 WORD STATISTICS:
Average word length: 6.2
Longest word: "everywhere" (10 characters)
Shortest word: "a" (1 character)

🏷️ WORDS APPEARING ONCE:
[programming, language, lets, work, quickly, integrate,
systems, effectively, powerful, fast, plays, well,
others, runs, everywhere]

🔗 TOP 3 WORD PAIRS:
1. "Python is" - 3 times
2. "works with" - 2 times
3. "with others" - 1 time

📊 FREQUENCY DISTRIBUTION:
Python    #### (4)
is        ###  (3)
works     ##   (2)
with      ##   (2)
a         #    (1)
```

---

# 🧠 Concepts Tested

This project focuses on:

* Sets
* Dictionaries
* List comprehensions
* String methods
* String cleaning
* Sorting
* Counting
* Frequency analysis
* Percentage calculations
* Bigram analysis
* Complex data manipulation
* Nested loops
