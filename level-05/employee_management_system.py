'''
Q4: The Employee Management System (Mid)

Create an OOP system for managing different types of employees.

Requirements:

    Create a base Employee class with:

        Attributes: employee_id, name, salary, department

        Methods: calculate_salary(), display_info()

    Create subclasses:

        Manager: Bonus, team size

        Developer: Programming languages, projects

        Designer: Tools, portfolio items

        Intern: Supervisor, duration

    Polymorphism: Each subclass calculates salary differently:

        Manager: Base + (team_size * 1000)

        Developer: Base + (projects * 2000)

        Designer: Base + (portfolio_items * 1500)

    Create an EmployeeManager class that:

        Adds/removes employees

        Searches by name/department

        Generates department reports

        Calculates total payroll

    Use dataclasses for data objects

Sample Output:
text

👔 EMPLOYEE MANAGEMENT SYSTEM 👔

1. Add Employee
2. Remove Employee
3. View All Employees
4. Department Report
5. Total Payroll
6. Search
7. Exit

Choice: 1
Type: (1) Manager (2) Developer (3) Designer (4) Intern: 2
Name: Damilola
Base Salary: 50000
Department: Engineering
Programming Languages (comma-separated): Python, Java, C++
Number of Projects: 3

✅ Developer added!

Choice: 3

📋 ALL EMPLOYEES (3):
1. Manager: Alice (Sales) - Salary: ₦85,000.00
   Team Size: 5, Bonus: ₦15,000.00

2. Developer: Damilola (Engineering) - Salary: ₦56,000.00
   Languages: Python, Java, C++
   Projects: 3

3. Designer: John (Design) - Salary: ₦52,000.00
   Tools: Figma, Photoshop
   Portfolio Items: 12

Choice: 4
Department: Engineering

📊 ENGINEERING DEPARTMENT REPORT
Employees: 2
Total Salary: ₦116,000.00
Average Salary: ₦58,000.00

Employees:
1. Damilola (Developer): ₦56,000.00
2. Bob (Manager): ₦60,000.00

Choice: 5
💰 Total Payroll: ₦218,000.00
Average Salary: ₦54,500.00

Concepts: Inheritance, polymorphism, encapsulation, dataclasses, collections, method overriding\
'''