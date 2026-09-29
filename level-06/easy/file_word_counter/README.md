# File Word Counter

## Difficulty

Easy

## Description

A command-line file analyzer that reads a text file and calculates basic statistics about its contents.

## Features

* Accepts a filename from the user
* Calculates file size in bytes
* Counts total lines
* Counts total words
* Counts total characters, including spaces
* Counts sentences using `.`, `!`, and `?`
* Counts unique words using a set
* Calculates average word length
* Finds the longest word
* Handles missing files gracefully
* Allows the user to save the analysis to a text file

## Example

```text
📁 FILE ANALYZER 📁

📊 ANALYSIS RESULTS:
File: sample.txt
Size: 119 bytes
Lines: 3
Words: 18
Characters: 119
Sentences: 3

📝 Word Statistics:
Unique words: 15
Average word length: 5.2 characters
Longest word: "programming" (11 chars)

Would you like to save results? (y/n): y
✅ Results saved to sample_analysis.txt
```

## Concepts

* File handling
* Reading and writing files
* `with open(...)`
* Exception handling
* `FileNotFoundError`
* String manipulation
* Lists
* Sets
* Loops
* Basic statistics
* User input
* Formatted strings
* `os.path`
