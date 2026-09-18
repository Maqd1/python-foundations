from datetime import date

from school_system.users.student import Student
from school_system.database.repository import StudentRepository
from school_system.services.reporting import ReportingService


class SchoolCLI:

    def __init__(self):
        self.student_repository = StudentRepository()
        self.reporting_service = ReportingService()

    def add_student(self) -> None:
        print("\nADD STUDENT")
        print("-" * 30)

        student_id = input("Student ID: ")
        name = input("Name: ")
        program = input("Program: ")
        level = int(input("Level: "))
        contact = input("Contact: ")
        address = input("Address: ")

        student = Student(
            name=name,
            date_of_birth=date(2000, 1, 1),
            contact=contact,
            address=address,
            student_id=student_id,
            program=program,
            level=level
        )

        self.student_repository.add(student)

        print("\nStudent added successfully.")

    def find_student(self) -> Student | None:
        student_id = input("Student ID: ")

        student = self.student_repository.get(
            student_id
        )

        if student is None:
            print("Student not found.")
            return None

        return student

    def view_student(self) -> None:
        print("\nVIEW STUDENT")
        print("-" * 30)

        student = self.find_student()

        if student is None:
            return

        student.display_info()

    def view_report(self) -> None:
        print("\nSTUDENT REPORT")
        print("-" * 30)

        student = self.find_student()

        if student is None:
            return

        report = (
            self.reporting_service
            .generate_student_report(student)
        )

        print()
        print(report)

    def list_students(self) -> None:
        print("\nSTUDENTS")
        print("-" * 30)

        students = self.student_repository.all()

        if not students:
            print("No students registered.")
            return

        for student in students:
            print(
                f"{student.student_id} | "
                f"{student.name} | "
                f"{student.program} | "
                f"Level {student.level}"
            )

    def run(self) -> None:
        while True:
            print("\n")
            print("=" * 40)
            print("SCHOOL MANAGEMENT SYSTEM")
            print("=" * 40)
            print("1. Add student")
            print("2. View student")
            print("3. List students")
            print("4. View student report")
            print("5. Exit")

            choice = input("\nChoose an option: ")

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_student()

            elif choice == "3":
                self.list_students()

            elif choice == "4":
                self.view_report()

            elif choice == "5":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")


if __name__ == "__main__":
    cli = SchoolCLI()
    cli.run()