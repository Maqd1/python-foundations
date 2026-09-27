# 🎯 Core Project: Student Management System

## The Academic Record System with Analytics 📊

Build a complete student management system that handles **student records, courses, grades, attendance, analytics, reports, searching, filtering, and data persistence**.

This project is designed to work with deeply nested data structures and progressively more advanced operations.

---

## 📊 Data Structure

The system uses nested dictionaries and lists to represent students, their courses, grades, attendance, and academic information.

```python
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
        "status": "Active"
    }
}
```

Possible student statuses include:

* `Active`
* `Suspended`
* `Graduated`

---

# 📋 Requirements

## 1. Core Functions

Implement the fundamental student-management operations.

### `add_student(name, age, email)`

Generate a unique student ID and add the student to the system.

### `enroll_course(student_id, course_code)`

Enroll an existing student in a course.

### `record_grade(student_id, course_code, grade)`

Record or update a student's grade for a course.

### `record_attendance(student_id, course_code, present)`

Add an attendance record for a course.

### `calculate_gpa(student_id)`

Calculate the student's GPA based on their courses.

---

# 📊 2. Advanced Analytics — HARD

The system should be able to analyze academic performance.

### `get_top_performers(n)`

Return the `n` students with the highest GPA.

### `get_course_statistics(course_code)`

Calculate statistics for a course, including:

* Minimum grade
* Maximum grade
* Average grade
* Median grade

### `get_attendance_report(student_id)`

Calculate attendance percentages for each course taken by the student.

### `get_at_risk_students()`

Find students who:

* Have a GPA below `2.0`, or
* Have failing courses

### `get_course_performance_ranking()`

Rank courses according to their average student grade.

---

# 📄 3. Report Generation — HARDER

Generate formatted academic reports.

### `generate_transcript(student_id)`

Generate a formatted transcript containing the student's academic information and course results.

### `generate_class_report(course_code)`

Generate a summary of the students taking a particular course.

### `generate_summary_report()`

Generate overall statistics such as:

* Total students
* Students by status
* Average GPA
* Passing rate
* Course performance
* Top performers
* At-risk students

---

# 🔎 4. Search and Filter — HARDEST

The system must support different ways of finding students.

### `search_students(query)`

Search students by:

* Name
* Email
* Student ID

### `filter_by_gpa(min_gpa, max_gpa)`

Return students whose GPA falls within a specified range.

### `filter_by_status(status)`

Filter students by status, such as:

* Active
* Suspended
* Graduated

---

# 💾 5. Data Persistence — SUPER HARD

The system must persist student data so information is not lost when the program closes.

Requirements:

* Save student data to CSV and/or JSON.
* Load saved data when the application starts.

---

# 🖥️ Sample Interface

```text
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
```

### Summary Report

```text
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
```

### Transcript

```text
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

---

# 🧠 Concepts Tested

This project tests the ability to work with:

* Nested dictionaries
* Lists
* Nested loops
* Dictionary and list comprehensions
* Functions with complex return values
* File I/O
* JSON/CSV persistence
* Sorting
* Searching
* Filtering
* Statistical calculations
* Data aggregation
* Complex data structures
* Report generation
* Real-world application logic
