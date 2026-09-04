'''
Core 4

📝 HARD QUIZ APP

The Adaptive Learning Quiz with Timed Questions ⏱️

Create a quiz system that adapts to the user's performance and tracks progress!

Quiz Structure:

```python
questions = [
    {
        "category": "Python Basics",
        "difficulty": 1,  # 1-5
        "question": "What is the output of print(2**3)?",
        "options": ["6", "8", "9", "16"],
        "correct": 1,  # index of correct answer
        "explanation": "** is the exponent operator. 2^3 = 8"
    },
    # ... more questions
]
```

Features:

1. Question Management:
   · Load questions from a list/dict
   · Each question has: category, difficulty, question text, 4 options, correct answer index, explanation
   · At least 15 questions across different categories
2. Difficulty System (HARD):
   · Start with 3 easy questions
   · If user gets 2/3 correct → increase difficulty
   · If user gets 0/3 correct → decrease difficulty
   · If user gets 1/3 correct → stay same
   · Adaptive difficulty range: 1-5
3. Timed Questions (HARDER):
   · Easy: 30 seconds
   · Medium: 20 seconds
   · Hard: 10 seconds
   · If time runs out: automatic wrong answer
4. Power-ups (HARDEST):
   · 50/50: Remove 2 wrong answers (once per quiz)
   · Extra Time: Add 10 seconds (once per quiz)
   · Skip: Skip current question without penalty (once per quiz)
5. Detailed Results:
   · Overall score
   · Score per category
   · Time per question
   · Questions that were difficult
   · Percentage of correct answers per difficulty level
   · Graph/text visualization of performance

Sample Output:

```
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

Concepts Tested: Lists of dictionaries, nested loops, functions with multiple returns, while loops, for loops, conditional logic, range(), break, continue, pass, time tracking (using time module), complex data structures

---
'''


import random
import time

# ==========================================
# QUESTION BANK (15 Questions across 5 categories)
# ==========================================

QUESTIONS = [
    # Difficulty 1
    {
        "category": "Python Basics",
        "difficulty": 1,
        "question": "What is the output of print(2**3)?",
        "options": ["6", "8", "9", "16"],
        "correct": 1,
        "explanation": "** is the exponent operator. 2^3 = 8",
    },
    {
        "category": "Python Basics",
        "difficulty": 1,
        "question": "Which keyword is used to define a function in Python?",
        "options": ["func", "def", "function", "lambda"],
        "correct": 1,
        "explanation": "'def' is used to define standard functions in Python.",
    },
    {
        "category": "Data Types",
        "difficulty": 1,
        "question": "What is the data type of [1, 2, 3]?",
        "options": ["tuple", "set", "list", "dictionary"],
        "correct": 2,
        "explanation": "Square brackets [] denote a list.",
    },
    # Difficulty 2
    {
        "category": "Programming Logic",
        "difficulty": 2,
        "question": "What is the output of list(range(3))?",
        "options": ["[0, 1, 2]", "[1, 2, 3]", "[0, 1, 2, 3]", "[1, 2]"],
        "correct": 0,
        "explanation": "range(3) generates integers from 0 up to (but not including) 3.",
    },
    {
        "category": "Data Types",
        "difficulty": 2,
        "question": "How do you create an empty set in Python?",
        "options": ["{}", "set()", "[]", "()"],
        "correct": 1,
        "explanation": "{} creates an empty dictionary. set() creates an empty set.",
    },
    {
        "category": "Python Basics",
        "difficulty": 2,
        "question": "What is the output of 'a' + 'b' * 2?",
        "options": ["ab2", "abab", "abb", "aabb"],
        "correct": 2,
        "explanation": "String multiplication happens before addition: 'b'*2 = 'bb', then 'a'+'bb' = 'abb'.",
    },
    # Difficulty 3
    {
        "category": "Programming Logic",
        "difficulty": 3,
        "question": "What is the result of bool('False')?",
        "options": ["False", "True", "None", "Error"],
        "correct": 1,
        "explanation": "Any non-empty string evaluates to True in boolean context.",
    },
    {
        "category": "Functions",
        "difficulty": 3,
        "question": "What does *args do in a function definition?",
        "options": [
            "Passes keyword arguments",
            "Passes variable positional arguments",
            "Multiplies arguments",
            "Forces mandatory arguments",
        ],
        "correct": 1,
        "explanation": "*args collects additional positional arguments into a tuple.",
    },
    {
        "category": "Data Structures",
        "difficulty": 3,
        "question": "Which dictionary method returns a default value if a key is missing?",
        "options": ["fetch()", "get()", "pop()", "find()"],
        "correct": 1,
        "explanation": "dict.get(key, default) avoids KeyError when accessing keys.",
    },
    # Difficulty 4
    {
        "category": "Functions",
        "difficulty": 4,
        "question": "What is the output of (lambda x: x*2)(4)?",
        "options": ["8", "4", "16", "Error"],
        "correct": 0,
        "explanation": "Immediately invokes an anonymous function passing 4 as x.",
    },
    {
        "category": "Data Structures",
        "difficulty": 4,
        "question": "What is the time complexity of looking up a key in a Python dict?",
        "options": ["O(n)", "O(log n)", "O(1)", "O(n^2)"],
        "correct": 2,
        "explanation": "Python dicts use hash tables, giving average O(1) lookup time.",
    },
    {
        "category": "Programming Logic",
        "difficulty": 4,
        "question": "What does the 'is' keyword compare?",
        "options": [
            "Values",
            "Memory identity",
            "Data types",
            "String length",
        ],
        "correct": 1,
        "explanation": "'==' compares equality of values; 'is' checks if both variables refer to the same object in memory.",
    },
    # Difficulty 5
    {
        "category": "Functions",
        "difficulty": 5,
        "question": "What does a decorator return in Python?",
        "options": [
            "A string",
            "A boolean",
            "A callable object / function",
            "None",
        ],
        "correct": 2,
        "explanation": "Decorators wrap functions and return a new function or callable.",
    },
    {
        "category": "Data Structures",
        "difficulty": 5,
        "question": "Which module provides double-ended queues with O(1) appends?",
        "options": ["queue", "collections", "heapq", "array"],
        "correct": 1,
        "explanation": "collections.deque provides fast O(1) pops and appends from either side.",
    },
    {
        "category": "Programming Logic",
        "difficulty": 5,
        "question": "What is the value of [x for x in range(5) if x % 2 == 0]?",
        "options": ["[1, 3]", "[0, 2, 4]", "[0, 1, 2, 3, 4]", "[2, 4]"],
        "correct": 1,
        "explanation": "Filters range(5) for even numbers: 0, 2, 4.",
    },
]

# ==========================================
# STATE & TIMING LOGIC
# ==========================================

power_ups = {"5050": True, "extra_time": True, "skip": True}


def get_time_limit(difficulty):
    if difficulty <= 2:
        return 30
    elif difficulty <= 3:
        return 20
    else:
        return 10


def select_question(current_diff, asked_indices):
    # Try exact match
    eligible = [
        i
        for i, q in enumerate(QUESTIONS)
        if q["difficulty"] == current_diff and i not in asked_indices
    ]

    # Fallback to nearest difficulty if exact match exhaust
    if not eligible:
        eligible = [i for i in range(len(QUESTIONS)) if i not in asked_indices]

    if not eligible:
        return None, None

    chosen_idx = random.choice(eligible)
    asked_indices.add(chosen_idx)
    return chosen_idx, QUESTIONS[chosen_idx]


def get_user_input_timed(time_limit):
    start_time = time.time()
    user_input = input("\nYour answer / option: ").strip().upper()
    end_time = time.time()

    elapsed = end_time - start_time
    if elapsed > time_limit:
        return None, elapsed, True  # Timeout
    return user_input, elapsed, False


# ==========================================
# MAIN QUIZ RUNNER
# ==========================================


def main():
    name = input("Enter your name: ").strip() or "Player"
    print(f"\n📚 ADAPTIVE QUIZ CHALLENGE 📚")
    print(f"Welcome {name}!\n")

    current_difficulty = 1
    score = 0
    total_questions = 10
    asked_indices = set()
    performance_log = []

    # Difficulty adjustment window state
    window_results = []

    for q_num in range(1, total_questions + 1):
        q_idx, q_data = select_question(current_difficulty, asked_indices)
        if q_data is None:
            print("No more questions available!")
            break

        time_limit = get_time_limit(current_difficulty)
        time_added = False
        skipped = False

        print(f"\n{'=' * 40}")
        print(
            f"Question {q_num}/{total_questions} | Category: {q_data['category']}"
        )
        print(
            f"Difficulty: {q_data['difficulty']} | Time limit: {time_limit}s"
        )
        print(f"{'=' * 40}")
        print(q_data["question"])

        # Display options
        opts = list(q_data["options"])
        hidden_indices = set()

        def print_options():
            labels = ["A", "B", "C", "D"]
            for idx, opt in enumerate(opts):
                if idx in hidden_indices:
                    print(f"  {labels[idx]}) [REMOVED]")
                else:
                    print(f"  {labels[idx]}) {opt}")

        print_options()

        # Power-up menu check
        if any(power_ups.values()):
            print("\nPower-ups available:")
            if power_ups["5050"]:
                print("  1. 50/50 (remove 2 wrong answers)")
            if power_ups["extra_time"]:
                print("  2. Extra Time (+10 seconds)")
            if power_ups["skip"]:
                print("  3. Skip (no penalty)")

            use_p = (
                input("\nWould you like to use a power-up? (y/n): ")
                .strip()
                .lower()
            )
            if use_p == "y":
                p_choice = input("Select power-up (1/2/3): ").strip()
                if p_choice == "1" and power_ups["5050"]:
                    power_ups["5050"] = False
                    wrong_idxs = [
                        i
                        for i in range(len(opts))
                        if i != q_data["correct"]
                    ]
                    hidden_indices = set(random.sample(wrong_idxs, 2))
                    print("\n--- Options updated ---")
                    print_options()
                elif p_choice == "2" and power_ups["extra_time"]:
                    power_ups["extra_time"] = False
                    time_limit += 10
                    print(f"⏱️ +10 seconds added! New limit: {time_limit}s")
                elif p_choice == "3" and power_ups["skip"]:
                    power_ups["skip"] = False
                    skipped = True
                    print("⏭️ Question skipped without penalty.")

        if skipped:
            continue

        # Get answer with timer
        user_ans, elapsed, timed_out = get_user_input_timed(time_limit)

        labels = ["A", "B", "C", "D"]
        correct_letter = labels[q_data["correct"]]

        is_correct = False
        if timed_out:
            print(f"\n⏰ TIME OUT! (Took {elapsed:.1f}s / {time_limit}s limit)")
            print(
                f"❌ INCORRECT! Correct answer was {correct_letter}) {opts[q_data['correct']]}"
            )
        elif user_ans == correct_letter:
            is_correct = True
            score += 1
            print(f"\n✅ CORRECT! (Time taken: {elapsed:.1f}s)")
        else:
            print(f"\n⏱️ Time taken: {elapsed:.1f}s")
            print(
                f"❌ INCORRECT! Correct answer was {correct_letter}) {opts[q_data['correct']]}"
            )

        print(f"Explanation: {q_data['explanation']}")

        # Track log for results
        performance_log.append(
            {
                "question_num": q_num,
                "category": q_data["category"],
                "difficulty": q_data["difficulty"],
                "is_correct": is_correct,
                "time_taken": elapsed,
                "timed_out": timed_out,
                "question_text": q_data["question"],
            }
        )

        # Adaptive difficulty adjustment window (evaluates every 3 questions)
        window_results.append(is_correct)
        if len(window_results) == 3:
            correct_in_window = sum(window_results)
            if correct_in_window >= 2 and current_difficulty < 5:
                current_difficulty += 1
                print(
                    f"\n📈 Difficulty INCREASED to level {current_difficulty}!"
                )
            elif correct_in_window == 0 and current_difficulty > 1:
                current_difficulty -= 1
                print(
                    f"\n📉 Difficulty DECREASED to level {current_difficulty}."
                )
            else:
                print(
                    f"\n➡️ Difficulty maintained at level {current_difficulty}."
                )
            window_results = []  # Reset window

    # ==========================================
    # DETAILED RESULTS & STATS
    # ==========================================
    display_results(score, total_questions, performance_log)


def display_results(score, total_questions, log):
    print("\n" + "=" * 40)
    print("📊 FINAL RESULTS 📊")
    print("=" * 40)

    pct = (score / total_questions) * 100 if total_questions > 0 else 0
    print(f"Overall Score: {score}/{total_questions} ({pct:.1f}%)\n")

    # Score per category
    categories = {}
    difficulties = {}
    times = []

    for entry in log:
        cat = entry["category"]
        diff = entry["difficulty"]
        correct = 1 if entry["is_correct"] else 0
        t = entry["time_taken"]

        times.append(t)

        # Category mapping
        if cat not in categories:
            categories[cat] = {"correct": 0, "total": 0}
        categories[cat]["correct"] += correct
        categories[cat]["total"] += 1

        # Difficulty mapping
        if diff not in difficulties:
            difficulties[diff] = {"correct": 0, "total": 0}
        difficulties[diff]["correct"] += correct
        difficulties[diff]["total"] += 1

    print("Performance by Category:")
    for cat, data in categories.items():
        cat_pct = (data["correct"] / data["total"]) * 100
        print(f"- {cat}: {data['correct']}/{data['total']} ({cat_pct:.0f}%)")

    print("\nPerformance by Difficulty:")
    for diff in sorted(difficulties.keys()):
        data = difficulties[diff]
        diff_pct = (data["correct"] / data["total"]) * 100
        print(
            f"- Level {diff}: {data['correct']}/{data['total']} ({diff_pct:.0f}%)"
        )

    if times:
        avg_time = sum(times) / len(times)
        fastest = min(log, key=lambda x: x["time_taken"])
        slowest = max(log, key=lambda x: x["time_taken"])

        print("\nTime Analysis:")
        print(f"- Average time: {avg_time:.1f} seconds")
        print(
            f"- Fastest: {fastest['time_taken']:.1f}s (Q{fastest['question_num']})"
        )
        print(
            f"- Slowest: {slowest['time_taken']:.1f}s (Q{slowest['question_num']})"
        )

    # Difficult Questions Identification
    difficult_qs = [
        q for q in log if not q["is_correct"] or q["time_taken"] > 15
    ]
    if difficult_qs:
        print("\nDifficult Questions:")
        for q in difficult_qs:
            reason = (
                "Answered incorrectly"
                if not q["is_correct"]
                else f"Took {q['time_taken']:.1f}s"
            )
            print(f"- Q{q['question_num']} ({q['category']}): {reason}")

    # Visual Text Graph
    print("\nPerformance Bar Chart:")
    for entry in log:
        bar = "🟩" if entry["is_correct"] else "🟥"
        print(
            f"Q{entry['question_num']} [Lvl {entry['difficulty']}] | {bar} ({entry['time_taken']:.1f}s)"
        )


if __name__ == "__main__":
    main()