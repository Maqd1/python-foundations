from datetime import date

from school_system.users.student import Student
from school_system.services.pdf_report import PDFReportService


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


def test_student_pdf_is_generated(tmp_path):
    student = create_student()

    student.add_transcript_entry(
        semester="FALL 2026",
        course_code="CSC301",
        course_title="Database Systems",
        credits=3,
        score=75
    )

    filename = tmp_path / "student_report.pdf"

    service = PDFReportService()

    service.generate_student_pdf(
        student,
        str(filename)
    )

    assert filename.exists()
    assert filename.stat().st_size > 0
