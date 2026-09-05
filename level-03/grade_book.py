'''
🟢 Easy Level (2 Questions)
Q1: The Grade Book Manager (Easy)

Create a program that manages student grades using a dictionary.

Requirements:

    Create a dictionary with 5 student names as keys and their grades as values
    python

    grades = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78,
        "Diana": 95,
        "Eve": 88
    }

    Print the entire grade book

    Ask user: "Enter student name to check grade: "

    If student exists, print their grade

    If not, print "Student not found!"

    Ask: "Add new student? (y/n): "

        If 'y', ask for name and grade, add to dictionary

    Calculate and print:

        Average grade

        Highest grade (and who got it)

        Lowest grade (and who got it)

    Extra challenge: Ask for a minimum grade and print all students above it

Concepts: Dictionaries, membership, loops, string methods

'''



# Initialize grade book
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95, "Eve": 88}

# 1. Print entire grade book
print(f"{'=' * 30}\n"
      "    CURRENT GRADE BOOK\n"
      f"{'=' * 30}"
      )


for name, grade in grades.items():
    print(f"• {name}: {grade}")
print()

# 2. Check student grade
search_name = input("Enter student name to check grade: ").strip().capitalize()
if search_name in grades:
    print(f"✅ {search_name}'s grade is {grades[search_name]}")
else:
    print("❌ Student not found!")

# 3. Add new student
add_choice = input("\nAdd new student? (y/n): ").strip().lower()
if add_choice == "y":
    new_name = input("Enter student name: ").strip().capitalize()
    new_grade = int(input("Enter student grade: "))
    grades[new_name] = new_grade
    print(f"Added {new_name} with grade {new_grade}.")

# 4. Calculate stats
total_grades = sum(grades.values())
avg_grade = total_grades / len(grades)

top_student = max(grades, key=grades.get)
lowest_student = min(grades, key=grades.get)

print("\n=== CLASS STATISTICS ===")
print(f"Average Grade: {avg_grade:.1f}")
print(f"Highest Grade: {top_student} ({grades[top_student]})")
print(f"Lowest Grade : {lowest_student} ({grades[lowest_student]})")

# 5. Extra challenge: Filter above minimum grade
print("\n=== FILTER STUDENTS ===")
min_threshold = int(
    input("Enter minimum grade threshold to see top performers: ")
)
top_performers = {
    name: gr for name, gr in grades.items() if gr >= min_threshold
}

if top_performers:
    print(f"Students scoring {min_threshold} or higher:")
    for name, gr in top_performers.items():
        print(f"• {name}: {gr}")
else:
    print(f"No students scored {min_threshold} or higher.")