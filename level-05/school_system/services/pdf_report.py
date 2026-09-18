from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from school_system.users.student import Student


class PDFReportService:

    def generate_student_pdf(
        self,
        student: Student,
        filename: str
    ) -> None:

        pdf = canvas.Canvas(
            filename,
            pagesize=A4
        )

        width, height = A4

        y = height - 50

        pdf.setFont(
            "Helvetica-Bold",
            16
        )

        pdf.drawString(
            50,
            y,
            "STUDENT ACADEMIC REPORT"
        )

        y -= 30

        pdf.setFont(
            "Helvetica",
            11
        )

        details = [
            f"Student ID: {student.student_id}",
            f"Name: {student.name}",
            f"Program: {student.program}",
            f"Level: {student.level}",
        ]

        for detail in details:
            pdf.drawString(
                50,
                y,
                detail
            )
            y -= 18

        y -= 15

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            50,
            y,
            "ACADEMIC RECORD"
        )

        y -= 25

        pdf.setFont(
            "Helvetica",
            10
        )

        for entry in student.transcript.entries:

            text = (
                f"{entry.course_code} | "
                f"{entry.course_title} | "
                f"{entry.credits} credits | "
                f"{entry.grade.letter_grade} | "
                f"{entry.grade_point:.2f}"
            )

            pdf.drawString(
                50,
                y,
                text
            )

            y -= 18

            if y < 50:
                pdf.showPage()
                y = height - 50
                pdf.setFont(
                    "Helvetica",
                    10
                )

        y -= 15

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.drawString(
            50,
            y,
            f"Total Credits: "
            f"{student.transcript.total_credits}"
        )

        y -= 18

        pdf.drawString(
            50,
            y,
            f"Cumulative GPA: "
            f"{student.transcript.cumulative_gpa:.2f}"
        )

        pdf.save()
