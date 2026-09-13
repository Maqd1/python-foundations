'''
2️⃣ 📝 HARD TEXT ANALYZER
The Smart Text Analysis Package 🔍

Build a comprehensive text analysis package with NLP-like features!

Package Structure:
text

text_analyzer/
    __init__.py
    analyzer.py
    statistics.py
    sentiment.py
    readability.py
    summarizer.py
    tokenizer.py
    utils.py
    cli.py
    web_app.py
data/
    stopwords.txt
    positive_words.txt
    negative_words.txt
tests/
    test_analyzer.py
README.md
setup.py

Requirements:

    Core Analysis (analyzer.py):

        analyze(text) → Returns comprehensive analysis

        get_word_frequency(text) → Count word occurrences

        get_sentence_count(text) → Count sentences

        get_paragraph_count(text) → Count paragraphs

        get_longest_words(text, n=5) → Longest words

        get_most_common_words(text, n=10) → Most frequent words

    Advanced Statistics (statistics.py):

        get_character_count(text) → Including/excluding spaces

        get_avg_word_length(text) → Average characters per word

        get_avg_sentence_length(text) → Average words per sentence

        get_lexical_diversity(text) → Unique words / total words

        get_word_length_distribution(text) → Distribution of word lengths

        get_letter_frequency(text) → Letter frequency analysis

    Sentiment Analysis (sentiment.py):

        analyze_sentiment(text) → Positive/Neutral/Negative

        calculate_sentiment_score(text) → Score between -1 and 1

        get_sentiment_breakdown(text) → Detailed analysis

        analyze_emotions(text) → Joy, Sadness, Anger, Fear, etc.

    Readability Scoring (readability.py):

        flesch_reading_ease(text) → 0-100 scale

        flesch_kincaid_grade(text) → US grade level

        gunning_fog_index(text) → Reading difficulty

        coleman_liau_index(text) → Text complexity

        get_readability_summary(text) → All scores

    Text Summarization (summarizer.py) - HARD:

        extractive_summarize(text, ratio=0.3) → Extract key sentences

        keyword_extraction(text, n=10) → Extract keywords

        get_sentence_importance(text) → Rank sentences by importance

        get_ngrams(text, n=2) → Get n-grams (bigrams, trigrams)

    Text Tokenization (tokenizer.py):

        word_tokenize(text) → Split into words

        sentence_tokenize(text) → Split into sentences

        clean_text(text) → Remove special characters, normalize

        remove_stopwords(text, language='english') → Remove stopwords

    Visualization (HARDEST):

        word_cloud(text, output_file) → Generate word cloud

        create_word_frequency_chart(text) → Frequency bar chart

        create_readability_chart(text) → Visual readability scores

        create_sentiment_timeline(text) → Sentiment over text

    CLI Interface (cli.py):
    python

    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('file', help='Text file to analyze')
        parser.add_argument('--sentiment', action='store_true')
        parser.add_argument('--readability', action='store_true')
        parser.add_argument('--summary', action='store_true')
        parser.add_argument('--export', help='Export to JSON')
        args = parser.parse_args()
        
        with open(args.file, 'r') as f:
            text = f.read()
        
        analyzer = TextAnalyzer()
        results = analyzer.analyze(text)
        print_results(results)

Sample Output:
text

📊 TEXT ANALYZER v1.0 📊

File: sample.txt
Length: 1,247 words | 89 sentences | 12 paragraphs

📈 STATISTICS:
Total characters: 6,245 (5,182 without spaces)
Average word length: 4.15 characters
Average sentence length: 14.0 words
Lexical diversity: 0.47 (587 unique words)

📊 WORD LENGTH DISTRIBUTION:
1-3 chars: ██████████ 35%
4-6 chars: ██████████████ 42%
7-10 chars: ███████ 20%
10+ chars: ██ 3%

📝 MOST COMMON WORDS:
1. "Python" (45 times)
2. "programming" (32 times)
3. "code" (28 times)
4. "function" (22 times)
5. "data" (19 times)

🧠 SENTIMENT ANALYSIS:
Sentiment: POSITIVE (+0.32)
Confidence: 0.87
Emotional breakdown:
  Joy: 0.45
  Trust: 0.38
  Anticipation: 0.29
  Sadness: 0.12

📖 READABILITY SCORES:
Flesch Reading Ease: 65.2 (Plain English)
Flesch-Kincaid Grade: 8.5 (8th-9th grade)
Gunning Fog Index: 10.3 (10th grade)
Coleman-Liau Index: 9.2 (9th grade)

📝 TEXT SUMMARY (30% compression):
Original: 1,247 words
Summary: 374 words
Key points:
1. Python is a powerful programming language...
2. Functions are reusable blocks of code...
3. Data structures help organize information...

🏷️ KEYWORDS (Top 10):
Python, programming, function, data, code, module,
package, syntax, error, debugging

☁️ Word Cloud generated: word_cloud.png

Export to JSON? (y/n): y
✅ Results saved to analysis.json

Web report generated: report.html

Concepts Tested: Advanced functions, text processing, NLP algorithms, sentiment analysis, readability formulas, file I/O, visualization, CLI with argparse, JSON serialization
'''