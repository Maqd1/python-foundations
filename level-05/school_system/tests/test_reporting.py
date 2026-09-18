from datetime import date

from school_system.users.student import Student
from school_system.services.reporting import ReportingService


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


def test_student_report_contains_student_information():
    student = create_student()

    service = ReportingService()
    report = service.generate_student_report(student)

    assert "STUDENT ACADEMIC REPORT" in report
    assert "STU001" in report
    assert "Test Student" in report
    assert "Computer Science" in report


def test_student_report_contains_academic_record():
    student = create_student()

    student.add_transcript_entry(
        semester="FALL 2026",
        course_code="CSC301",
        course_title="Database Systems",
        credits=3,
        score=75
    )

    service = ReportingService()
    report = service.generate_student_report(student)

    assert "CSC301" in report
    assert "Database Systems" in report
    assert "3 credits" in report
    assert "A" in report


def test_student_report_contains_gpa():
    student = create_student()

    student.add_transcript_entry(
        semester="FALL 2026",
        course_code="CSC301",
        course_title="Database Systems",
        credits=3,
        score=75
    )

    service = ReportingService()
    report = service.generate_student_report(student)

    assert "Cumulative GPA: 4.00" in report
