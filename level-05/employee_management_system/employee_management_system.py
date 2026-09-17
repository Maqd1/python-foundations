from dataclasses import dataclass, field


@dataclass
class Employee:
    employee_id: int
    name: str
    salary: float
    department: str

    def calculate_salary(self):
        return self.salary

    def display_info(self):
        print(
            f"{self.__class__.__name__}: "
            f"{self.name} ({self.department}) - "
            f"Salary: ₦{self.calculate_salary():,.2f}"
        )


@dataclass
class Manager(Employee):
    team_size: int = 0

    def calculate_salary(self):
        return self.salary + (self.team_size * 1000)

    def display_info(self):
        bonus = self.team_size * 1000

        print(
            f"Manager: {self.name} ({self.department}) - "
            f"Salary: ₦{self.calculate_salary():,.2f}"
        )
        print(
            f"   Team Size: {self.team_size}, "
            f"Bonus: ₦{bonus:,.2f}"
        )


@dataclass
class Developer(Employee):
    programming_languages: list[str] = field(default_factory=list)
    projects: int = 0

    def calculate_salary(self):
        return self.salary + (self.projects * 2000)

    def display_info(self):
        languages = ", ".join(self.programming_languages)

        print(
            f"Developer: {self.name} ({self.department}) - "
            f"Salary: ₦{self.calculate_salary():,.2f}"
        )
        print(f"   Languages: {languages}")
        print(f"   Projects: {self.projects}")


@dataclass
class Designer(Employee):
    tools: list[str] = field(default_factory=list)
    portfolio_items: int = 0

    def calculate_salary(self):
        return self.salary + (self.portfolio_items * 1500)

    def display_info(self):
        tools = ", ".join(self.tools)

        print(
            f"Designer: {self.name} ({self.department}) - "
            f"Salary: ₦{self.calculate_salary():,.2f}"
        )
        print(f"   Tools: {tools}")
        print(f"   Portfolio Items: {self.portfolio_items}")


@dataclass
class Intern(Employee):
    supervisor: str = ""
    duration: int = 0

    def calculate_salary(self):
        return self.salary

    def display_info(self):
        print(
            f"Intern: {self.name} ({self.department}) - "
            f"Salary: ₦{self.calculate_salary():,.2f}"
        )
        print(f"   Supervisor: {self.supervisor}")
        print(f"   Duration: {self.duration} months")


class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        print(f"\n✅ {employee.__class__.__name__} added!")

    def remove_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                self.employees.remove(employee)
                print(
                    f"🗑️ Employee {employee.name} "
                    f"removed successfully."
                )
                return True

        print("❌ Employee not found.")
        return False

    def search_by_name(self, name):
        return [
            employee
            for employee in self.employees
            if name.lower() in employee.name.lower()
        ]

    def search_by_department(self, department):
        return [
            employee
            for employee in self.employees
            if department.lower() == employee.department.lower()
        ]

    def department_report(self, department):
        employees = self.search_by_department(department)

        if not employees:
            print(
                f"\n❌ No employees found in "
                f"{department} department."
            )
            return

        total_salary = sum(
            employee.calculate_salary()
            for employee in employees
        )

        average_salary = total_salary / len(employees)

        print(
            f"\n📊 {department.upper()} "
            f"DEPARTMENT REPORT"
        )
        print(f"Employees: {len(employees)}")
        print(f"Total Salary: ₦{total_salary:,.2f}")
        print(f"Average Salary: ₦{average_salary:,.2f}")

        print("\nEmployees:")

        for number, employee in enumerate(employees, start=1):
            print(
                f"{number}. "
                f"{employee.name} "
                f"({employee.__class__.__name__}): "
                f"₦{employee.calculate_salary():,.2f}"
            )

    def total_payroll(self):
        return sum(
            employee.calculate_salary()
            for employee in self.employees
        )

    def average_salary(self):
        if not self.employees:
            return 0

        return self.total_payroll() / len(self.employees)

    def display_all(self):
        if not self.employees:
            print("\n❌ No employees found.")
            return

        print(
            f"\n📋 ALL EMPLOYEES "
            f"({len(self.employees)}):"
        )

        for number, employee in enumerate(
            self.employees,
            start=1
        ):
            print(f"\n{number}. ", end="")
            employee.display_info()


def get_employee_id():
    try:
        return int(input("Employee ID: "))
    except ValueError:
        print("❌ Employee ID must be a number.")
        return None


def get_float(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("❌ Please enter a valid number.")
        return None


def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("❌ Please enter a valid whole number.")
        return None


def get_list(prompt):
    value = input(prompt)

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def create_employee(manager, next_employee_id):
    print("\n1. Manager")
    print("2. Developer")
    print("3. Designer")
    print("4. Intern")

    employee_type = input("Type: ")

    name = input("Name: ")

    salary = get_float("Base Salary: ₦")

    if salary is None:
        return next_employee_id

    department = input("Department: ")

    employee_id = next_employee_id

    if employee_type == "1":
        team_size = get_int("Team Size: ")

        if team_size is None:
            return next_employee_id

        employee = Manager(
            employee_id,
            name,
            salary,
            department,
            team_size
        )

    elif employee_type == "2":
        languages = get_list(
            "Programming Languages "
            "(comma-separated): "
        )

        projects = get_int("Number of Projects: ")

        if projects is None:
            return next_employee_id

        employee = Developer(
            employee_id,
            name,
            salary,
            department,
            languages,
            projects
        )

    elif employee_type == "3":
        tools = get_list(
            "Tools (comma-separated): "
        )

        portfolio_items = get_int(
            "Number of Portfolio Items: "
        )

        if portfolio_items is None:
            return next_employee_id

        employee = Designer(
            employee_id,
            name,
            salary,
            department,
            tools,
            portfolio_items
        )

    elif employee_type == "4":
        supervisor = input("Supervisor: ")

        duration = get_int("Duration (months): ")

        if duration is None:
            return next_employee_id

        employee = Intern(
            employee_id,
            name,
            salary,
            department,
            supervisor,
            duration
        )

    else:
        print("❌ Invalid employee type.")
        return next_employee_id

    manager.add_employee(employee)

    print(f"Employee ID: {employee_id}")

    return next_employee_id + 1


def search_employees(manager):
    print("\n1. Search by name")
    print("2. Search by department")

    choice = input("Choice: ")

    if choice == "1":
        name = input("Name: ")
        results = manager.search_by_name(name)

    elif choice == "2":
        department = input("Department: ")
        results = manager.search_by_department(
            department
        )

    else:
        print("❌ Invalid choice.")
        return

    if not results:
        print("❌ No employees found.")
        return

    print(f"\n🔍 Found {len(results)} employee(s):")

    for employee in results:
        employee.display_info()


def main():
    manager = EmployeeManager()

    # Sample employees
    manager.add_employee(
        Manager(
            1001,
            "Alice",
            80000,
            "Sales",
            5
        )
    )

    manager.add_employee(
        Developer(
            1002,
            "Damilola",
            50000,
            "Engineering",
            ["Python", "Java", "C++"],
            3
        )
    )

    manager.add_employee(
        Designer(
            1003,
            "John",
            34000,
            "Design",
            ["Figma", "Photoshop"],
            12
        )
    )

    next_employee_id = 1004

    print("\n👔 EMPLOYEE MANAGEMENT SYSTEM 👔")

    while True:
        print("\n1. Add Employee")
        print("2. Remove Employee")
        print("3. View All Employees")
        print("4. Department Report")
        print("5. Total Payroll")
        print("6. Search")
        print("7. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            next_employee_id = create_employee(
                manager,
                next_employee_id
            )

        elif choice == "2":
            employee_id = get_employee_id()

            if employee_id is not None:
                manager.remove_employee(employee_id)

        elif choice == "3":
            manager.display_all()

        elif choice == "4":
            department = input("Department: ")
            manager.department_report(department)

        elif choice == "5":
            total = manager.total_payroll()
            average = manager.average_salary()

            print(
                f"\n💰 Total Payroll: "
                f"₦{total:,.2f}"
            )
            print(
                f"Average Salary: "
                f"₦{average:,.2f}"
            )

        elif choice == "6":
            search_employees(manager)

        elif choice == "7":
            print(
                "\nThank you for using the "
                "Employee Management System! 👋"
            )
            break

        else:
            print("❌ Invalid choice. Please select 1–7.")


if __name__ == "__main__":
    main()