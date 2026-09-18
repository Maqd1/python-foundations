from datetime import date

from school_system.users.student import Student
from school_system.academics.course import Course
from school_system.academics.grade import Grade


def create_student() -> Student:
    return Student(
        name="Test Student",
        date_of_birth=date(2000, 1, 1),
        contact="08000000000",
        address="Lagos",
        student_id="STU001",
        program="Computer Science",
        level=400
    )


def test_student_creation():
    student = create_student()

    assert student.student_id == "STU001"
    assert student.program == "Computer Science"
    assert student.level == 400
    assert student.status == "ACTIVE"


def test_student_can_enroll_in_course():
    student = create_student()

    student.enroll_course("CSC301")

    assert "CSC301" in student.enrolled_courses


def test_student_can_drop_course():
    student = create_student()

    student.enroll_course("CSC301")
    student.drop_course("CSC301")

    assert "CSC301" not in student.enrolled_courses


def test_student_can_add_grade():
    student = create_student()

    student.add_grade("CSC301", 75)

    assert student.grades["CSC301"] == 75


def test_grade_letter():
    grade = Grade(
        student_id="STU001",
        course_code="CSC301",
        score=75
    )

    assert grade.letter_grade == "A"


def test_course_creation():
    course = Course(
        course_code="CSC301",
        title="Database Systems",
        description="Database fundamentals",
        credits=3,
        department="Computer Science"
    )

    assert course.course_code == "CSC301"
    assert course.credits == 3