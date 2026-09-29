import os


filename = input("Enter filename: ")

try:
    with open(filename, "r") as file:
        text = file.read()

except FileNotFoundError:
    print(f"❌ File not found: {filename}")

else:
    file_size = os.path.getsize(filename)

    characters = len(text)

    lines = text.splitlines()
    total_lines = len(lines)

    words = text.split()
    total_words = len(words)

    sentences = (
        text.count(".")
        + text.count("!")
        + text.count("?")
    )

    unique_words = set(words)
    unique_count = len(unique_words)

    total_word_characters = sum(len(word) for word in words)

    average_word_length = (
        total_word_characters / total_words
        if total_words
        else 0
    )

    longest_word = max(words, key=len) if words else ""

    results = f"""

📁 FILE ANALYZER 📁

📊 ANALYSIS RESULTS:
File: {filename}
Size: {file_size} bytes
Lines: {total_lines}
Words: {total_words}
Characters: {characters}
Sentences: {sentences}

📝 Word Statistics:
Unique words: {unique_count}
Average word length: {average_word_length:.1f} characters
Longest word: "{longest_word}" ({len(longest_word)} chars)
""".strip()

    print(results)

    save = input("\nWould you like to save results? (y/n): ").strip().lower()

    if save == "y":
        output_filename = f"{os.path.splitext(filename)[0]}_analysis.txt"

        with open(output_filename, "w") as file:
            file.write(results)

        print(f"✅ Results saved to {output_filename}")