# 📝 Hard Quiz App

## The Adaptive Learning Quiz with Timed Questions ⏱️

Create a quiz system that adapts to the user's performance and tracks progress.

## Quiz Structure

Questions should be stored using a list of dictionaries.

Example:

```python
questions = [
    {
        "category": "Python Basics",
        "difficulty": 1,
        "question": "What is the output of print(2**3)?",
        "options": ["6", "8", "9", "16"],
        "correct": 1,
        "explanation": "** is the exponent operator. 2^3 = 8"
    }
]
```

Each question should contain:

* Category
* Difficulty
* Question text
* Four answer options
* Correct answer index
* Explanation

## Features

### 1. Question Management

* Load questions from a list/dictionary structure.
* Include at least **15 questions**.
* Questions should cover different categories.

### 2. Adaptive Difficulty — Hard

Start with **3 easy questions**.

After every group of 3 questions:

* **2/3 correct** → increase difficulty.
* **0/3 correct** → decrease difficulty.
* **1/3 correct** → keep the same difficulty.

The adaptive difficulty should remain within:

```text
1–5
```

### 3. Timed Questions — Harder

Each difficulty level has a time limit:

| Difficulty |       Time |
| ---------- | ---------: |
| Easy       | 30 seconds |
| Medium     | 20 seconds |
| Hard       | 10 seconds |

If the time runs out, the question is automatically marked **wrong**.

### 4. Power-Ups — Hardest

The player has access to three power-ups.

#### 50/50

Remove two incorrect answers.

Available **once per quiz**.

#### Extra Time

Add **10 seconds** to the current question.

Available **once per quiz**.

#### Skip

Skip the current question without receiving a penalty.

Available **once per quiz**.

### 5. Detailed Results

At the end of the quiz, display:

* Overall score
* Score per category
* Time spent on each question
* Questions that were difficult
* Percentage of correct answers for each difficulty level
* Graph/text visualization of performance

## Sample Output

```text
📚 ADAPTIVE QUIZ CHALLENGE 📚
Welcome Damilola!

Category: Python Basics (Difficulty: 1)

Question 1/10:
What is the output of print(2**3)?
Options:
A) 6
B) 8
C) 9
D) 16

Your answer: B
⏱️ Time taken: 5.3 seconds

✅ CORRECT!
Explanation: ** is the exponent operator. 2^3 = 8

Power-ups available:
1. 50/50 (remove 2 wrong answers)
2. Extra Time (+10 seconds)
3. Skip

Would you like to use a power-up? (y/n): n

Score: 10 | Streak: 1 | Difficulty: 2 (increased!)

---

Question 2/10:
Category: Programming Logic
Difficulty: 2

What is the output of for i in range(3): print(i, end=' ')?
Options:
A) 0 1 2
B) 1 2 3
C) 0 1 2 3
D) 0 0 0

⏰ Time remaining: 15 seconds...

Your answer: A
⏱️ Time taken: 8.2 seconds

✅ CORRECT!

📊 FINAL RESULTS 📊
Score: 8/10 (80%)

Performance by Category:
- Python Basics: 2/2 (100%)
- Programming Logic: 3/4 (75%)
- Data Types: 1/2 (50%)
- Functions: 2/2 (100%)

Time Analysis:
- Average time: 12.5 seconds
- Fastest: 5.3 seconds (Question 1)
- Slowest: 22.1 seconds (Question 7)

Difficult Questions:
1. Question 7 (Data Types): You answered incorrectly
2. Question 4 (Programming Logic): You took 22.1 seconds

Would you like to review your answers? (y/n): y
```

## Concepts Tested

* Lists of dictionaries
* Nested loops
* Functions with multiple return values
* `while` loops
* `for` loops
* Conditional logic
* `range()`
* `break`
* `continue`
* `pass`
* Time tracking using the `time` module
* Complex data structures
* Performance tracking
