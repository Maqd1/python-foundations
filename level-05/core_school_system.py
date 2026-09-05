'''
2️⃣ 🏫 VERY HARD SCHOOL SYSTEM
The Complete School Management System 📚

Build a comprehensive school system with students, teachers, courses, grades, and attendance!

Package Structure:
text

school_system/
    __init__.py
    users/
        __init__.py
        person.py
        student.py
        teacher.py
        staff.py
    academics/
        __init__.py
        course.py
        grade.py
        schedule.py
        attendance.py
    administration/
        __init__.py
        department.py
        semester.py
        fee.py
    services/
        __init__.py
        registration.py
        grading.py
        reporting.py
    database/
        __init__.py
        repository.py
    exceptions/
        __init__.py
        school_exceptions.py
    tests/
        __init__.py
        test_students.py
    main.py
    cli.py
    setup.py

Requirements:

    User Hierarchy (Inheritance):

        Person: Name, DOB, contact, address

        Student: Student ID, enrolled courses, grades, attendance, transcript

        Teacher: Employee ID, department, assigned courses, office hours

        AdminStaff: Employee ID, role, access level

    Academic System (Composition):

        Course: Course code, title, description, credits, department

        Schedule: Time, day, room, instructor

        Grade: Student, course, score, letter grade, GPA weight

        Attendance: Student, course, date, status (PRESENT/ABSENT/LATE)

    Semester System:

        Semester: Period (Fall/Spring/Summer), courses offered, registration

        Enrollment: Student, course, status, date

        Transcript: Student, courses taken, grades, cumulative GPA

    GPA Calculation System (Strategy Pattern):

        Different grading scales: 4.0, 5.0, percentage

        Weighted vs unweighted GPA

        Grade point calculation strategies

    Registration System (HARD):

        Course registration with prerequisites

        Waitlist management

        Override approval workflow

        Schedule conflict detection

    Reporting System (HARDEST):

        Student transcripts (PDF)

        Class rosters

        Grade distributions

        Attendance reports

        Semester summaries

    Notification System (Observer Pattern):

        Email alerts for registration

        Grade change notifications

        Attendance alerts

        Academic warnings

Sample Output:
text

🏫 UNIVERSITY MANAGEMENT SYSTEM v5.0 🏫

📊 SESSION 2026/2027 | SEMESTER: FALL

👨‍🎓 STUDENT PROFILE
Name: Damilola Ogunleye
Student ID: 2024/12345
Program: Computer Science (B.Sc.)
Level: 400
Status: ACTIVE
Cumulative GPA: 3.82 (Class Rank: 5/245)

📋 CURRENT COURSES (Fall 2026):
1. CSC401 - Advanced Algorithms (3 Credits)
   Lecturer: Prof. John Smith
   Schedule: Mon/Wed 10:00-11:30
   Room: CLT-201
   Grade: -
   Attendance: 85%

2. CSC402 - Database Systems (3 Credits)
   Lecturer: Dr. Mary Johnson
   Schedule: Tue/Thu 12:00-13:30
   Room: CLT-305
   Grade: -
   Attendance: 92%

3. CSC403 - Software Engineering (3 Credits)
   Lecturer: Dr. Adaobi Okonkwo
   Schedule: Tue/Thu 14:00-15:30
   Room: CLT-108
   Grade: -
   Attendance: 78%

=====================================
📋 TRANSCRIPT (All Semesters)
Semester: Fall 2025
CSC301 - Data Structures: A (4.0)
CSC302 - Operating Systems: B+ (3.5)
MAT201 - Linear Algebra: A (4.0)
STA301 - Probability: A- (3.7)
Total Credits: 16
Semester GPA: 3.81

Semester: Spring 2026
CSC303 - Programming Languages: A (4.0)
CSC304 - Computer Networks: B (3.0)
PHY202 - Physics II: B+ (3.5)
TOTAL: 12 Credits, GPA: 3.50

=====================================
📊 PROGRAM PROGRESS
Total Credits Completed: 85/120
Core Courses: 45/48 (93%)
Electives: 40/60 (67%)
Research Project: IN PROGRESS

Remaining Courses:
1. CSC405 - Machine Learning
2. CSC406 - Cryptography
3. CSC407 - Web Security

Expected Graduation: May 2027 (2 semesters left)

=====================================
📝 REGISTRATION PORTAL
Available Courses (Fall 2026):
1. CSC401 - Advanced Algorithms (Prereq: CSC301)
   ✅ Completed: CSC301 - A

2. CSC405 - Machine Learning (Prereq: STA301)
   ✅ Completed: STA301 - A-

3. CSC406 - Cryptography (Prereq: CSC304)
   ✅ Completed: CSC304 - B

Select courses to register:
>> 1, 3

⚠️ Schedule Conflict!
CSC406 (Tue/Thu 10:00-11:30) conflicts with PHY301 (Tue/Thu 10:00-11:30)
Override? (y/n): n

Registration completed!
Registered: CSC401, CSC405
Total Credits: 6
Remaining Credits Available: 15

=====================================
📊 GRADE REPORT (Mid-Semester)
Course: CSC401 - Advanced Algorithms
Assignments: 7/10 (70%)
Midterm: 42/50 (84%)
Quiz 1: 8/10 (80%)
Quiz 2: 9/10 (90%)
Project: 45/50 (90%)
Current Grade: 84% (B+)

⚠️ Improvement Opportunity:
Score 90%+ on Final to achieve A

=====================================
📊 ATTENDANCE REPORT
Course: CSC401
Total Classes: 24
Present: 20
Absent: 2
Late: 2
Attendance Rate: 83%

Attendance Warning! (Below 80%)
You are at risk of being barred from the exam.

=====================================
💳 FINANCE
Student: Damilola Ogunleye
Tuition Fee (Fall 2026): ₦250,000.00
Paid: ₦250,000.00
Balance: ₦0.00

Previous Balance: ₦0.00
Semester: 8th
Total Paid to Date: ₦2,000,000.00

=====================================
🔔 NOTIFICATIONS
1. 📧 Grade posted: CSC401 - Assignment 3
   Score: 8/10 (Good work!)

2. 📧 Exam schedule available:
   CSC401: Dec 15, 2026 @ 9:00 AM

3. ⚠️ Academic Warning:
   Attendance below 80% in CSC403

4. 📧 Event: Career Fair 2026
   Date: Dec 10, 2026
   Location: Main Hall

=====================================
📊 LIBRARY SYSTEM
Books Borrowed: 3
1. "Introduction to Algorithms" (Due: Dec 20)
2. "Database Systems" (Due: Jan 15)
3. "Clean Code" (Due: Dec 25)

Overdue Books: 0
Total Fines: ₦0.00

Concepts Tested: Advanced inheritance, composition, strategy pattern, observer pattern, dataclasses, property decorators, validation, complex business logic, reporting, PDF generation, notification system
'''