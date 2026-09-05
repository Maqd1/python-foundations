'''
🎯 HARD PROJECTS USING DATA STRUCTURES
1️⃣ 🎓 HARD STUDENT MANAGEMENT SYSTEM
The Academic Record System with Analytics 📊
Create a complete student management system that handles grades, attendance, and generates reports.
Data Structure:
python

```
students = {
    "STU001": {
        "name": "Damilola Ogunleye",
        "age": 20,
        "email": "dami@student.edu",
        "courses": {
            "CSC101": {
                "grade": 85,
                "attendance": [True, True, False, True, True],
                "assignments": [90, 85, 88, 92],
                "midterm": 78,
                "final": 88
            },
            "MAT102": {
                "grade": 92,
                "attendance": [True, True, True, True, True],
                "assignments": [95, 90, 88, 94],
                "midterm": 85,
                "final": 95
            }
        },
        "total_credits": 60,
        "gpa": 3.8,
        "status": "Active"  # Active, Suspended, Graduated
    },
    # More students...
}
```

Requirements:

1. Core Functions:
   * `add_student(name, age, email)` → Generate unique ID, add to system
   * `enroll_course(student_id, course_code)` → Add course to student
   * `record_grade(student_id, course_code, grade)` → Update grade
   * `record_attendance(student_id, course_code, present)` → Add attendance record
   * `calculate_gpa(student_id)` → Compute GPA for all courses
2. Advanced Analytics (HARD):
   * `get_top_performers(n)` → Return n students with highest GPA
   * `get_course_statistics(course_code)` → Returns min, max, average, median
   * `get_attendance_report(student_id)` → Percentage per course
   * `get_at_risk_students()` → Students with GPA < 2.0 or failing courses
   * `get_course_performance_ranking()` → Rank courses by average grade
3. Report Generation (HARDER):
   * `generate_transcript(student_id)` → Print formatted transcript
   * `generate_class_report(course_code)` → Summary of entire class
   * `generate_summary_report()` → Overall statistics (avg GPA, passing rate, etc.)
4. Search and Filter (HARDEST):
   * `search_students(query)` → Search by name, email, or ID
   * `filter_by_gpa(min_gpa, max_gpa)` → Filter students by GPA range
   * `filter_by_status(status)` → Filter by Active, Suspended, etc.
5. Data Persistence (SUPER HARD):
   * Save to CSV/JSON file
   * Load from file on startup

Sample Output:
text

```
🎓 STUDENT MANAGEMENT SYSTEM 🎓

1. Add Student
2. Enroll in Course
3. Record Grade
4. Record Attendance
5. View Student
6. Generate Reports
7. Search Students
8. Analytics
9. Exit

Choice: 6

📊 REPORT MENU:
1. Transcript
2. Class Report
3. Summary Report
4. At-Risk Students
5. Top Performers

Choice: 3

📈 SUMMARY REPORT (2026-2027)
Total Students: 45
Active: 42
Suspended: 2
Graduated: 1

Average GPA: 3.45
Passing Rate: 89%

📊 COURSE PERFORMANCE:
CSC101 - Avg: 82.5 (Range: 65-95)
MAT102 - Avg: 88.3 (Range: 70-98)
PHY103 - Avg: 76.8 (Range: 55-90)

🏆 TOP PERFORMERS:
1. Damilola Ogunleye (3.89)
2. John Smith (3.85)
3. Alice Johnson (3.80)

⚠️ AT-RISK STUDENTS (GPA < 2.0):
1. Bob Williams (1.87) - 2 courses failing
2. Charlie Brown (1.95) - 1 course failing

Choice: 5
Enter student ID: STU001

📄 TRANSCRIPT FOR DAMILOLA OGUNLEYE
====================================
Student ID: STU001
Email: dami@student.edu
Program: Computer Science
Total Credits: 60
GPA: 3.82

COURSES:
CSC101:
  Grade: 85 (B+)
  Assignments: 90, 85, 88, 92
  Midterm: 78
  Final: 88
  Attendance: 80%
  
MAT102:
  Grade: 92 (A)
  Assignments: 95, 90, 88, 94
  Midterm: 85
  Final: 95
  Attendance: 100%

====================================
STATUS: Active | Honors Student
```

Concepts Tested: Nested dictionaries, lists, nested loops, comprehensions, functions with complex returns, file I/O, sorting, searching, statistical calculations
'''

import json
import os
import statistics

STUDENTS_FILE = "students.json"

students = {}

# --- GRADE SCALE ---
# The spec never states a letter-grade scale, but its own transcript sample
# shows "85 -> B+" and "92 -> A". Working backward from those two data
# points, this scale is the one that reproduces them exactly.
GRADE_SCALE = [
    (90, "A", 4.0),
    (85, "B+", 3.3),
    (80, "B", 3.0),
    (75, "C+", 2.3),
    (70, "C", 2.0),
    (60, "D", 1.0),
    (0, "F", 0.0),
]


def grade_to_letter_and_points(grade):
    for threshold, letter, points in GRADE_SCALE:
        if grade >= threshold:
            return letter, points
    return "F", 0.0


# --- PERSISTENCE ---

def load_students():
    global students
    if os.path.exists(STUDENTS_FILE):
        try:
            with open(STUDENTS_FILE, "r") as f:
                students = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("\u26a0\ufe0f  Could not read students.json \u2014 starting with an empty roster.")


def save_students():
    with open(STUDENTS_FILE, "w") as f:
        json.dump(students, f, indent=2)


# --- CORE FUNCTIONS ---

def generate_student_id():
    existing_nums = [int(sid[3:]) for sid in students if sid.startswith("STU") and sid[3:].isdigit()]
    next_num = max(existing_nums, default=0) + 1
    return f"STU{next_num:03d}"


def add_student(name, age, email):
    student_id = generate_student_id()
    students[student_id] = {
        "name": name,
        "age": age,
        "email": email,
        "courses": {},
        "total_credits": 0,
        "gpa": 0.0,
        "status": "Active",
    }
    save_students()
    return student_id


def enroll_course(student_id, course_code, credits=3):
    if student_id not in students:
        return f"\u274c Student '{student_id}' not found."
    if course_code in students[student_id]["courses"]:
        return f"\u274c Already enrolled in {course_code}."

    students[student_id]["courses"][course_code] = {
        "grade": None,
        "attendance": [],
        "assignments": [],
        "midterm": None,
        "final": None,
        "credits": credits,
    }
    students[student_id]["total_credits"] += credits
    save_students()
    return f"\u2705 Enrolled {student_id} in {course_code}."


def record_grade(student_id, course_code, grade):
    if student_id not in students or course_code not in students[student_id]["courses"]:
        return f"\u274c Student or course not found."

    students[student_id]["courses"][course_code]["grade"] = grade
    calculate_gpa(student_id)  # keep GPA in sync automatically
    save_students()
    return f"\u2705 Recorded grade {grade} for {student_id} in {course_code}."


def record_attendance(student_id, course_code, present):
    if student_id not in students or course_code not in students[student_id]["courses"]:
        return f"\u274c Student or course not found."

    students[student_id]["courses"][course_code]["attendance"].append(present)
    save_students()
    return f"\u2705 Attendance recorded for {student_id} in {course_code}."


def calculate_gpa(student_id):
    if student_id not in students:
        return None

    courses = students[student_id]["courses"]
    graded = [c["grade"] for c in courses.values() if c["grade"] is not None]

    if not graded:
        gpa = 0.0
    else:
        points = [grade_to_letter_and_points(g)[1] for g in graded]
        gpa = sum(points) / len(points)

    students[student_id]["gpa"] = round(gpa, 2)
    return students[student_id]["gpa"]


# --- ADVANCED ANALYTICS ---

def get_top_performers(n):
    ranked = sorted(students.items(), key=lambda item: item[1]["gpa"], reverse=True)
    return [(sid, info["name"], info["gpa"]) for sid, info in ranked[:n]]


def get_course_statistics(course_code):
    grades = [
        info["courses"][course_code]["grade"]
        for info in students.values()
        if course_code in info["courses"] and info["courses"][course_code]["grade"] is not None
    ]
    if not grades:
        return None
    return {
        "min": min(grades),
        "max": max(grades),
        "average": sum(grades) / len(grades),
        "median": statistics.median(grades),
        "count": len(grades),
    }


def get_attendance_report(student_id):
    if student_id not in students:
        return None
    report = {}
    for code, course in students[student_id]["courses"].items():
        att = course["attendance"]
        report[code] = (sum(att) / len(att) * 100) if att else None
    return report


def get_at_risk_students():
    at_risk = []
    for sid, info in students.items():
        failing = [code for code, c in info["courses"].items() if c["grade"] is not None and c["grade"] < 60]
        if info["gpa"] < 2.0 or failing:
            at_risk.append({"id": sid, "name": info["name"], "gpa": info["gpa"], "failing_courses": failing})
    return at_risk


def get_course_performance_ranking():
    all_course_codes = {code for info in students.values() for code in info["courses"]}
    stats_by_course = {code: get_course_statistics(code) for code in all_course_codes}
    scored = [(code, s) for code, s in stats_by_course.items() if s is not None]
    return sorted(scored, key=lambda item: item[1]["average"], reverse=True)


# --- SEARCH AND FILTER ---

def search_students(query):
    q = query.lower()
    return {
        sid: info for sid, info in students.items()
        if q in sid.lower() or q in info["name"].lower() or q in info["email"].lower()
    }


def filter_by_gpa(min_gpa, max_gpa):
    return {sid: info for sid, info in students.items() if min_gpa <= info["gpa"] <= max_gpa}


def filter_by_status(status):
    return {sid: info for sid, info in students.items() if info["status"].lower() == status.lower()}


# --- REPORTS ---

def generate_transcript(student_id):
    if student_id not in students:
        print(f"\u274c Student '{student_id}' not found.")
        return

    info = students[student_id]
    print(f"\n\U0001f4c4 TRANSCRIPT FOR {info['name'].upper()}")
    print("=" * 40)
    print(f"Student ID: {student_id}")
    print(f"Email: {info['email']}")
    print(f"Total Credits: {info['total_credits']}")
    print(f"GPA: {info['gpa']:.2f}")

    print("\nCOURSES:")
    for code, course in info["courses"].items():
        print(f"{code}:")
        if course["grade"] is not None:
            letter, _ = grade_to_letter_and_points(course["grade"])
            print(f"  Grade: {course['grade']} ({letter})")
        else:
            print("  Grade: Not yet graded")

        if course["assignments"]:
            print(f"  Assignments: {', '.join(str(a) for a in course['assignments'])}")
        if course["midterm"] is not None:
            print(f"  Midterm: {course['midterm']}")
        if course["final"] is not None:
            print(f"  Final: {course['final']}")

        att = course["attendance"]
        if att:
            pct = sum(att) / len(att) * 100
            print(f"  Attendance: {pct:.0f}%")
        print()

    print("=" * 40)
    honors = " | Honors Student" if info["gpa"] >= 3.7 else ""
    print(f"STATUS: {info['status']}{honors}")


def generate_class_report(course_code):
    stats = get_course_statistics(course_code)
    print(f"\n\U0001f4ca CLASS REPORT: {course_code}")
    if stats is None:
        print("No grades recorded yet for this course.")
        return

    print(f"Students graded: {stats['count']}")
    print(f"Average: {stats['average']:.1f} | Median: {stats['median']:.1f} | Range: {stats['min']}-{stats['max']}")

    print("\nRoster:")
    for sid, info in students.items():
        if course_code in info["courses"] and info["courses"][course_code]["grade"] is not None:
            grade = info["courses"][course_code]["grade"]
            letter, _ = grade_to_letter_and_points(grade)
            print(f"  {info['name']} - {grade} ({letter})")


def generate_summary_report():
    total = len(students)
    if total == 0:
        print("\nNo students in the system yet.")
        return

    status_counts = {}
    for info in students.values():
        status_counts[info["status"]] = status_counts.get(info["status"], 0) + 1

    gpas = [info["gpa"] for info in students.values()]
    avg_gpa = sum(gpas) / len(gpas)
    passing = sum(1 for gpa in gpas if gpa >= 2.0)
    passing_rate = passing / total * 100

    print("\n\U0001f4c8 SUMMARY REPORT")
    print(f"Total Students: {total}")
    for status, count in status_counts.items():
        print(f"{status}: {count}")

    print(f"\nAverage GPA: {avg_gpa:.2f}")
    print(f"Passing Rate: {passing_rate:.0f}%")

    ranking = get_course_performance_ranking()
    if ranking:
        print("\n\U0001f4ca COURSE PERFORMANCE:")
        for code, stats in ranking:
            print(f"{code} - Avg: {stats['average']:.1f} (Range: {stats['min']}-{stats['max']})")


def print_top_performers(n=3):
    performers = get_top_performers(n)
    print(f"\n\U0001f3c6 TOP PERFORMERS:")
    if not performers:
        print("No students to rank yet.")
        return
    for i, (sid, name, gpa) in enumerate(performers, start=1):
        print(f"{i}. {name} ({gpa:.2f})")


def print_at_risk_students():
    at_risk = get_at_risk_students()
    print(f"\n\u26a0\ufe0f AT-RISK STUDENTS (GPA < 2.0 or failing a course):")
    if not at_risk:
        print("No at-risk students right now.")
        return
    for i, student in enumerate(at_risk, start=1):
        fail_note = f" - {len(student['failing_courses'])} course(s) failing" if student["failing_courses"] else ""
        print(f"{i}. {student['name']} ({student['gpa']:.2f}){fail_note}")


# --- MENUS ---

def handle_add_student():
    name = input("Name: ").strip()
    try:
        age = int(input("Age: ").strip())
    except ValueError:
        print("\u274c Age must be a number.")
        return
    email = input("Email: ").strip()
    student_id = add_student(name, age, email)
    print(f"\u2705 Added student '{name}' with ID {student_id}.")


def handle_enroll():
    student_id = input("Student ID: ").strip()
    course_code = input("Course code: ").strip().upper()
    print(enroll_course(student_id, course_code))


def handle_record_grade():
    student_id = input("Student ID: ").strip()
    course_code = input("Course code: ").strip().upper()
    try:
        grade = float(input("Grade: ").strip())
    except ValueError:
        print("\u274c Grade must be a number.")
        return
    print(record_grade(student_id, course_code, grade))


def handle_record_attendance():
    student_id = input("Student ID: ").strip()
    course_code = input("Course code: ").strip().upper()
    present = input("Present? (y/n): ").strip().lower() == "y"
    print(record_attendance(student_id, course_code, present))


def handle_view_student():
    student_id = input("Student ID: ").strip()
    if student_id not in students:
        print(f"\u274c Student '{student_id}' not found.")
        return
    generate_transcript(student_id)


def handle_reports_menu():
    while True:
        print("\n\U0001f4ca REPORT MENU:")
        print("1. Transcript")
        print("2. Class Report")
        print("3. Summary Report")
        print("4. At-Risk Students")
        print("5. Top Performers")
        print("6. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            generate_transcript(student_id)
        elif choice == "2":
            course_code = input("Enter course code: ").strip().upper()
            generate_class_report(course_code)
        elif choice == "3":
            generate_summary_report()
        elif choice == "4":
            print_at_risk_students()
        elif choice == "5":
            try:
                n = int(input("How many? ").strip())
            except ValueError:
                n = 3
            print_top_performers(n)
        elif choice == "6":
            break
        else:
            print("\u274c Invalid choice.")
            continue


def handle_search():
    query = input("Search by name, email, or ID: ").strip()
    results = search_students(query)
    if not results:
        print("No matches found.")
        return
    print(f"\n\U0001f50d {len(results)} match(es):")
    for sid, info in results.items():
        print(f"  {sid} - {info['name']} ({info['email']}) - GPA: {info['gpa']:.2f}")


def handle_analytics_menu():
    while True:
        print("\n\U0001f4c8 ANALYTICS MENU:")
        print("1. Course Statistics")
        print("2. Attendance Report")
        print("3. Course Performance Ranking")
        print("4. Filter by GPA Range")
        print("5. Filter by Status")
        print("6. Back")
        choice = input("Choice: ").strip()

        if choice == "1":
            course_code = input("Course code: ").strip().upper()
            stats = get_course_statistics(course_code)
            if stats is None:
                print("No grades recorded for this course.")
            else:
                print(f"Min: {stats['min']} | Max: {stats['max']} | "
                      f"Average: {stats['average']:.1f} | Median: {stats['median']:.1f}")
        elif choice == "2":
            student_id = input("Student ID: ").strip()
            report = get_attendance_report(student_id)
            if report is None:
                print(f"\u274c Student '{student_id}' not found.")
            else:
                for code, pct in report.items():
                    pct_display = f"{pct:.0f}%" if pct is not None else "No records"
                    print(f"{code}: {pct_display}")
        elif choice == "3":
            ranking = get_course_performance_ranking()
            for code, stats in ranking:
                print(f"{code} - Avg: {stats['average']:.1f} (Range: {stats['min']}-{stats['max']})")
        elif choice == "4":
            try:
                min_gpa = float(input("Min GPA: ").strip())
                max_gpa = float(input("Max GPA: ").strip())
            except ValueError:
                print("\u274c GPA values must be numbers.")
                continue
            for sid, info in filter_by_gpa(min_gpa, max_gpa).items():
                print(f"  {sid} - {info['name']} - GPA: {info['gpa']:.2f}")
        elif choice == "5":
            status = input("Status (Active/Suspended/Graduated): ").strip()
            for sid, info in filter_by_status(status).items():
                print(f"  {sid} - {info['name']} - {info['status']}")
        elif choice == "6":
            break
        else:
            print("\u274c Invalid choice.")
            continue


def print_menu():
    print("\n\U0001f393 STUDENT MANAGEMENT SYSTEM \U0001f393")
    print("1. Add Student")
    print("2. Enroll in Course")
    print("3. Record Grade")
    print("4. Record Attendance")
    print("5. View Student")
    print("6. Generate Reports")
    print("7. Search Students")
    print("8. Analytics")
    print("9. Exit")


def main():
    load_students()
    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            handle_add_student()
        elif choice == "2":
            handle_enroll()
        elif choice == "3":
            handle_record_grade()
        elif choice == "4":
            handle_record_attendance()
        elif choice == "5":
            handle_view_student()
        elif choice == "6":
            handle_reports_menu()
        elif choice == "7":
            handle_search()
        elif choice == "8":
            handle_analytics_menu()
        elif choice == "9":
            print("Goodbye! \U0001f44b")
            break
        else:
            print("\u274c Invalid choice.")
            continue


if __name__ == "__main__":
    main()