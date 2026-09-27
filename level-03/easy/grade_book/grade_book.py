


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