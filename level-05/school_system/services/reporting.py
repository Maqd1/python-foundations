from school_system.users.student import Student
from school_system.administration.semester import Semester


class ReportingService:

    def generate_student_report(
        self,
        student: Student
    ) -> str:

        transcript = student.get_transcript()

        lines = [
            "STUDENT ACADEMIC REPORT",
            "=" * 40,
            f"Student ID: {student.student_id}",
            f"Name: {student.name}",
            f"Program: {student.program}",
            f"Level: {student.level}",
            "",
            "ACADEMIC RECORD",
            "-" * 40,
        ]

        if not transcript.entries:
            lines.append("No academic records available.")

        else:
            for entry in transcript.entries:
                lines.append(
                    f"{entry.course_code} | "
                    f"{entry.course_title} | "
                    f"{entry.credits} credits | "
                    f"{entry.grade.letter_grade} | "
                    f"{entry.grade_point:.2f}"
                )

        lines.extend([
            "",
            "SUMMARY",
            "-" * 40,
            f"Total Credits: {transcript.total_credits}",
            f"Cumulative GPA: "
            f"{transcript.cumulative_gpa:.2f}",
        ])

        return "\n".join(lines)

    def generate_semester_report(
        self,
        semester: Semester
    ) -> str:

        lines = [
            "SEMESTER REPORT",
            "=" * 40,
            f"Semester: {semester}",
            f"Courses Offered: "
            f"{len(semester.courses_offered)}",
            f"Enrollments: "
            f"{len(semester.enrollments)}",
            "",
            "COURSES",
            "-" * 40,
        ]

        for course in semester.courses_offered:
            lines.append(
                f"{course.course_code} | "
                f"{course.title} | "
                f"{course.credits} credits"
            )

        return "\n".join(lines)