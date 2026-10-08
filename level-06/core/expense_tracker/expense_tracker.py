import json
import os
import shutil
from datetime import datetime
import calendar
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


DATA_FILE = "expenses.json"

CURRENCY_RATES = {
    "NGN": 1.0,
    "USD": 0.00065,
    "EUR": 0.00060,
}


users = [
    {
        "id": 1,
        "name": "MAQD"
    }
]


expenses = []


budgets = []


def save_data():
    data = {
        "users": users,
        "expenses": expenses,
        "budgets": budgets
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    create_backup()


def create_backup():
    backup_directory = os.path.join(
        os.path.dirname(DATA_FILE),
        "backups"
    )

    os.makedirs(
        backup_directory,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    backup_file = os.path.join(
        backup_directory,
        f"expenses_backup_{timestamp}.json"
    )

    shutil.copy2(
        DATA_FILE,
        backup_file
    )

    backups = sorted(
        [
            os.path.join(
                backup_directory,
                filename
            )
            for filename in os.listdir(
                backup_directory
            )
            if filename.endswith(".json")
        ]
    )

    while len(backups) > 5:
        oldest_backup = backups.pop(0)

        try:
            os.remove(oldest_backup)
        except OSError:
            pass


def load_data():
    global users
    global expenses
    global budgets

    if not os.path.exists(DATA_FILE):
        save_data()
        return

    try:
        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            expenses = data

            users = [
                {
                    "id": 1,
                    "name": "MAQD"
                }
            ]

            budgets = []

        elif isinstance(data, dict):
            users = data.get(
                "users",
                []
            )

            expenses = data.get(
                "expenses",
                []
            )

            budgets = data.get(
                "budgets",
                []
            )

        else:
            print(
                "❌ Invalid data format."
            )
            return

        # Migrate old expenses
        if not users:
            users = [
                {
                    "id": 1,
                    "name": "MAQD"
                }
            ]

        next_expense_id = 1

        existing_ids = [
            expense["id"]
            for expense in expenses
            if isinstance(expense, dict)
            and isinstance(
                expense.get("id"),
                int
            )
        ]

        if existing_ids:
            next_expense_id = max(
                existing_ids
            ) + 1

        for expense in expenses:

            if "id" not in expense:
                expense["id"] = next_expense_id
                next_expense_id += 1

            if "user_id" not in expense:
                expense["user_id"] = users[0]["id"]

        save_data()

    except (
        json.JSONDecodeError,
        OSError
    ):
        print(
            "❌ Could not load saved data."
        )


def get_next_user_id():
    if not users:
        return 1

    return max(user["id"] for user in users) + 1


def get_next_expense_id():
    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1


def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user

    return None


def get_user_expenses(user_id):
    return [
        expense
        for expense in expenses
        if expense["user_id"] == user_id
    ]


def get_expense_by_id(expense_id, user_id):
    for expense in expenses:
        if (
            expense["id"] == expense_id
            and expense["user_id"] == user_id
        ):
            return expense

    return None


def get_user_budgets(user_id):
    return [
        budget
        for budget in budgets
        if budget["user_id"] == user_id
    ]


def get_budget(user_id, category):
    for budget in budgets:
        if (
            budget["user_id"] == user_id
            and budget["category"].lower() == category.lower()
        ):
            return budget

    return None


def create_user():
    print("\n👤 CREATE USER")

    name = input("Enter your name: ").strip()

    if not name:
        print("❌ Name cannot be empty.")
        return None

    for user in users:
        if user["name"].lower() == name.lower():
            print("❌ User already exists.")
            return user

    user = {
        "id": get_next_user_id(),
        "name": name
    }

    users.append(user)
    save_data()

    print("\n✅ User created successfully!")

    return user


def select_user():
    print("\n👤 USERS")

    if not users:
        print("No users found.")
        return None

    for user in users:
        print(
            f'{user["id"]}. {user["name"]}'
        )

    try:
        user_id = int(
            input("\nSelect user ID: ")
        )

    except ValueError:
        print("❌ Invalid user ID.")
        return None

    user = get_user_by_id(user_id)

    if user is None:
        print("❌ User not found.")
        return None

    return user


def get_date():
    while True:
        date = input(
            "Date (YYYY-MM-DD): "
        ).strip()

        try:
            datetime.strptime(
                date,
                "%Y-%m-%d"
            )

            return date

        except ValueError:
            print(
                "❌ Invalid date. Use YYYY-MM-DD."
            )


def get_amount():
    while True:
        try:
            amount = float(
                input("Amount: ")
            )

            if amount <= 0:
                print(
                    "❌ Amount must be greater than zero."
                )

                continue

            return amount

        except ValueError:
            print(
                "❌ Enter a valid amount."
            )


def add_expense(user):
    print("\n➕ ADD EXPENSE")

    expense = {
        "id": get_next_expense_id(),
        "user_id": user["id"],
        "date": get_date(),
        "amount": get_amount(),
        "category": input(
            "Category: "
        ).strip(),
        "description": input(
            "Description: "
        ).strip(),
        "payment_method": input(
            "Payment method: "
        ).strip()
    }

    expenses.append(expense)

    save_data()

    print(
        "\n✅ Expense added successfully!"
    )

    print("💾 Changes saved.")

    check_budget_alert(user)


def display_expense(expense):
    print(
        f'ID: {expense["id"]} | '
        f'Date: {expense["date"]} | '
        f'₦{expense["amount"]:,.2f} | '
        f'{expense["category"]} | '
        f'{expense["description"]} | '
        f'{expense["payment_method"]}'
    )


def view_expenses(user):
    print(
        f'\n📋 {user["name"].upper()}\'S EXPENSES'
    )

    user_expenses = get_user_expenses(
        user["id"]
    )

    if not user_expenses:
        print(
            "No expenses found."
        )

        return

    for expense in user_expenses:
        display_expense(expense)


def filter_by_category(user):
    print("\n🔎 FILTER BY CATEGORY")

    user_expenses = get_user_expenses(
        user["id"]
    )

    if not user_expenses:
        print(
            "No expenses found."
        )

        return

    categories = sorted(
        {
            expense["category"]
            for expense in user_expenses
        }
    )

    print("\nAvailable categories:")

    for category in categories:
        print(
            f"- {category}"
        )

    category = input(
        "\nEnter category: "
    ).strip()

    filtered_expenses = [
        expense
        for expense in user_expenses
        if expense["category"].lower()
        == category.lower()
    ]

    if not filtered_expenses:
        print(
            "\n❌ No expenses found for that category."
        )

        return

    print(
        f'\n📋 EXPENSES — {category.upper()}'
    )

    for expense in filtered_expenses:
        display_expense(expense)


def filter_by_date_range(user):
    print("\n📅 FILTER BY DATE RANGE")

    user_expenses = get_user_expenses(
        user["id"]
    )

    if not user_expenses:
        print(
            "No expenses found."
        )

        return

    print(
        "\nEnter the date range."
    )

    start_date = get_date()
    end_date = get_date()

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    if start > end:
        print(
            "\n❌ Start date cannot be after end date."
        )

        return

    filtered_expenses = []

    for expense in user_expenses:
        expense_date = datetime.strptime(
            expense["date"],
            "%Y-%m-%d"
        )

        if start <= expense_date <= end:
            filtered_expenses.append(
                expense
            )

    if not filtered_expenses:
        print(
            "\n❌ No expenses found in this date range."
        )

        return

    print(
        f"\n📅 EXPENSES FROM {start_date} TO {end_date}"
    )

    for expense in filtered_expenses:
        display_expense(expense)

    total = sum(
        expense["amount"]
        for expense in filtered_expenses
    )

    print(
        f"\nTotal: ₦{total:,.2f}"
    )


def filter_expenses(user):
    while True:
        print("\n🔎 FILTER EXPENSES")
        print("1. By Category")
        print("2. By Date Range")
        print("3. Back")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            filter_by_category(user)

        elif choice == "2":
            filter_by_date_range(user)

        elif choice == "3":
            break

        else:
            print(
                "\n❌ Invalid option. Please choose 1–3."
            )


def monthly_expenses(user, year, month):
    result = []

    for expense in get_user_expenses(
        user["id"]
    ):
        expense_date = datetime.strptime(
            expense["date"],
            "%Y-%m-%d"
        )

        if (
            expense_date.year == year
            and expense_date.month == month
        ):
            result.append(expense)

    return result


def monthly_summary(user):
    print("\n📊 MONTHLY SUMMARY")

    current_date = datetime.now()

    year_input = input(
        f"Year [{current_date.year}]: "
    ).strip()

    month_input = input(
        f"Month [1-12] [{current_date.month}]: "
    ).strip()

    try:
        year = (
            int(year_input)
            if year_input
            else current_date.year
        )

        month = (
            int(month_input)
            if month_input
            else current_date.month
        )

        if month < 1 or month > 12:
            raise ValueError

    except ValueError:
        print(
            "❌ Invalid year or month."
        )

        return

    month_expenses = monthly_expenses(
        user,
        year,
        month
    )

    month_name = datetime(
        year,
        month,
        1
    ).strftime("%B")

    print(
        f"\n📊 MONTHLY SUMMARY ({month_name} {year})"
    )

    if not month_expenses:
        print(
            "No expenses found for this month."
        )

        return

    total = sum(
        expense["amount"]
        for expense in month_expenses
    )

    transactions = len(
        month_expenses
    )

    days_in_month = (
        datetime(
            year + (month == 12),
            1 if month == 12 else month + 1,
            1
        )
        - datetime(
            year,
            month,
            1
        )
    ).days

    average_daily = total / days_in_month

    print(
        f"Total Spent: ₦{total:,.2f}"
    )

    print(
        f"Average Daily: ₦{average_daily:,.2f}"
    )

    print(
        f"Transactions: {transactions}"
    )

    category_totals = {}

    for expense in month_expenses:
        category = expense["category"].strip().lower()

        category_totals[category] = (
            category_totals.get(
                category,
                0
            )
            + expense["amount"]
        )

    print(
        "\n📈 SPENDING BY CATEGORY:"
    )

    for category, amount in sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):
        percentage = (
            amount / total
        ) * 100

        bar_length = round(
            percentage / 5
        )

        bar = "█" * bar_length

        print(
            f"{category}: "
            f"₦{amount:,.2f} "
            f"({percentage:.1f}%) "
            f"{bar}"
        )


def set_budget(user):
    print("\n💰 SET CATEGORY BUDGET")

    category = input(
        "Category: "
    ).strip()

    if not category:
        print(
            "❌ Category cannot be empty."
        )

        return

    try:
        amount = float(
            input("Budget amount: ")
        )

        if amount <= 0:
            print(
                "❌ Budget must be greater than zero."
            )

            return

    except ValueError:
        print(
            "❌ Enter a valid amount."
        )

        return

    existing_budget = get_budget(
        user["id"],
        category
    )

    if existing_budget:
        existing_budget["amount"] = amount

        print(
            "\n✅ Budget updated successfully!"
        )

    else:
        budgets.append(
            {
                "user_id": user["id"],
                "category": category,
                "amount": amount
            }
        )

        print(
            "\n✅ Budget created successfully!"
        )

    save_data()

    print("💾 Changes saved.")


def get_category_spending(user, year, month):
    expenses = monthly_expenses(user, year, month)

    category_totals = {}

    for expense in expenses:
        category = expense["category"].strip().lower()
        amount = expense["amount"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount

    return category_totals


def category_breakdown(user):
    print("\n📊 CATEGORY BREAKDOWN")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("❌ Invalid month.")
            return

    except ValueError:
        print("❌ Invalid date.")
        return

    category_totals = get_category_spending(
        user,
        year,
        month
    )

    if not category_totals:
        print("\nNo expenses found.")
        return

    total = sum(category_totals.values())

    print(
        f"\n📊 SPENDING BY CATEGORY "
        f"({year}-{month:02d})"
    )

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for category, amount in sorted_categories:
        percentage = (amount / total) * 100

        bar_length = int(percentage / 5)

        bar = "█" * bar_length

        print(
            f"{category}: "
            f"₦{amount:,.2f} "
            f"({percentage:.1f}%) "
            f"{bar}"
        )


def top_spending_categories(user):
    print("\n🏆 TOP SPENDING CATEGORIES")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("❌ Invalid month.")
            return

    except ValueError:
        print("❌ Invalid date.")
        return

    category_totals = get_category_spending(
        user,
        year,
        month
    )

    if not category_totals:
        print("\nNo expenses found.")
        return

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print(
        f"\n🏆 TOP SPENDING CATEGORIES "
        f"({year}-{month:02d})"
    )

    for position, (category, amount) in enumerate(
        sorted_categories[:5],
        start=1
    ):
        print(
            f"{position}. "
            f"{category} → "
            f"₦{amount:,.2f}"
        )


def daily_average_spending(user):
    print("\n📅 DAILY AVERAGE SPENDING")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("❌ Invalid month.")
            return

    except ValueError:
        print("❌ Invalid date.")
        return

    expenses = monthly_expenses(
        user,
        year,
        month
    )

    if not expenses:
        print("\nNo expenses found.")
        return

    total = sum(
        expense["amount"]
        for expense in expenses
    )

    days_in_month = calendar.monthrange(
        year,
        month
    )[1]

    average = total / days_in_month

    print(
        f"\n📅 DAILY AVERAGE ({year}-{month:02d})"
    )

    print(
        f"Total Spent: ₦{total:,.2f}"
    )

    print(
        f"Days in Month: {days_in_month}"
    )

    print(
        f"Average Daily: ₦{average:,.2f}"
    )


def budget_tracking(user):
    print("\n📊 BUDGET TRACKING")

    user_budgets = get_user_budgets(
        user["id"]
    )

    if not user_budgets:
        print(
            "No budgets have been created."
        )

        return

    current_date = datetime.now()

    year_input = input(
        f"Year [{current_date.year}]: "
    ).strip()

    month_input = input(
        f"Month [1-12] [{current_date.month}]: "
    ).strip()

    try:
        year = (
            int(year_input)
            if year_input
            else current_date.year
        )

        month = (
            int(month_input)
            if month_input
            else current_date.month
        )

    except ValueError:
        print(
            "❌ Invalid year or month."
        )

        return

    if year < 1 or year > 9999:
        print(
            "❌ Year must be between 1 and 9999."
        )

        return

    if month < 1 or month > 12:
        print(
            "❌ Month must be between 1 and 12."
        )

        return

    print(
        f"\n📊 BUDGET TRACKING — "
        f"{datetime(year, month, 1).strftime('%B')} {year}"
    )

    category_totals = get_category_spending(
        user,
        year,
        month
    )

    for budget in user_budgets:
        category = budget["category"].strip().lower()
        budget_amount = budget["amount"]

        spent = category_totals.get(
            category,
            0
        )

        percentage = (
            spent / budget_amount
        ) * 100

        if percentage >= 100:
            status = "🚨 OVER BUDGET"

        elif percentage >= 90:
            status = "⚠️ ALERT"

        elif percentage >= 80:
            status = "⚠️ WARNING"

        else:
            status = "✅"

        print(
            f"{category}: "
            f"₦{budget_amount:,.2f} budget → "
            f"₦{spent:,.2f} used "
            f"({percentage:.0f}%) "
            f"{status}"
        )


def check_budget_alert(user):
    print("\n🚨 BUDGET ALERTS")

    current_date = datetime.now()

    year_input = input(
        f"Year [{current_date.year}]: "
    ).strip()

    month_input = input(
        f"Month [1-12] [{current_date.month}]: "
    ).strip()

    try:
        year = (
            int(year_input)
            if year_input
            else current_date.year
        )

        month = (
            int(month_input)
            if month_input
            else current_date.month
        )

    except ValueError:
        print(
            "❌ Invalid year or month."
        )
        return

    if year < 1 or year > 9999:
        print(
            "❌ Year must be between 1 and 9999."
        )
        return

    if month < 1 or month > 12:
        print(
            "❌ Month must be between 1 and 12."
        )
        return

    print(
        f"\n🚨 BUDGET ALERTS — "
        f"{datetime(year, month, 1).strftime('%B')} {year}"
    )

    category_totals = get_category_spending(
        user,
        year,
        month
    )

    user_budgets = [
        budget
        for budget in budgets
        if budget["user_id"] == user["id"]
    ]

    if not user_budgets:
        print(
            "❌ No budgets have been set."
        )
        return

    alerts_found = False

    for budget in user_budgets:
        category = (
            budget["category"]
            .strip()
            .lower()
        )

        budget_amount = float(
            budget["amount"]
        )

        spent = category_totals.get(
            category,
            0
        )

        if budget_amount <= 0:
            continue

        percentage = (
            spent / budget_amount
        ) * 100

        if percentage >= 100:
            alerts_found = True

            print(
                f"\n🔴 OVER BUDGET: "
                f"{category.title()}"
            )

            print(
                f"Budget: ₦{budget_amount:,.2f}"
            )

            print(
                f"Spent: ₦{spent:,.2f}"
            )

            print(
                f"Usage: {percentage:.0f}%"
            )

            print(
                f"⚠️ You have exceeded your "
                f"{category.title()} budget."
            )

        elif percentage >= 80:
            alerts_found = True

            remaining = (
                budget_amount - spent
            )

            print(
                f"\n🟡 BUDGET WARNING: "
                f"{category.title()}"
            )

            print(
                f"Budget: ₦{budget_amount:,.2f}"
            )

            print(
                f"Spent: ₦{spent:,.2f}"
            )

            print(
                f"Usage: {percentage:.0f}%"
            )

            print(
                f"Remaining: ₦{remaining:,.2f}"
            )

            print(
                f"⚠️ You are approaching "
                f"your {category.title()} budget."
            )

    if not alerts_found:
        print(
            "\n✅ No budget alerts."
        )

def delete_budget(user):
    print("\n🗑️ DELETE BUDGET")

    user_budgets = get_user_budgets(
        user["id"]
    )

    if not user_budgets:
        print("No budgets found.")
        return

    print("\nYour budgets:")

    for index, budget in enumerate(
        user_budgets,
        start=1
    ):
        print(
            f'{index}. '
            f'{budget["category"]} → '
            f'₦{budget["amount"]:,.2f}'
        )

    try:
        choice = int(
            input("\nSelect budget number to delete: ")
        )

    except ValueError:
        print("❌ Invalid choice.")
        return

    if choice < 1 or choice > len(user_budgets):
        print("❌ Budget not found.")
        return

    budget = user_budgets[choice - 1]

    print(
        f'\nCategory: {budget["category"]}'
    )

    print(
        f'Budget: ₦{budget["amount"]:,.2f}'
    )

    confirmation = input(
        "\nAre you sure you want to delete this budget? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        budgets.remove(budget)
        save_data()

        print("\n✅ Budget deleted successfully!")
        print("💾 Changes saved.")

    else:
        print("\n❌ Delete cancelled.")


def budget_menu(user):
    while True:
        print("\n💰 BUDGET MANAGEMENT")
        print("1. Set Budget")
        print("2. View Budget Tracking")
        print("3. Delete Budget")
        print("4. Check Budget Alerts")
        print("5. Back")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            set_budget(user)

        elif choice == "2":
            budget_tracking(user)

        elif choice == "3":
            delete_budget(user)

        elif choice == "4":
            check_budget_alert(user)

        elif choice == "5":
            break

        else:
            print(
                "\n❌ Invalid option. Please choose 1–4."
            )


def edit_expense(user):
    print("\n✏️ EDIT EXPENSE")

    user_expenses = get_user_expenses(
        user["id"]
    )

    if not user_expenses:
        print(
            "No expenses found."
        )

        return

    view_expenses(user)

    try:
        expense_id = int(
            input(
                "\nEnter expense ID to edit: "
            )
        )

    except ValueError:
        print(
            "❌ Invalid ID."
        )

        return

    expense = get_expense_by_id(
        expense_id,
        user["id"]
    )

    if expense is None:
        print(
            "❌ Expense not found."
        )

        return

    print(
        "\nPress Enter to keep the current value."
    )

    date = input(
        f'Date [{expense["date"]}]: '
    ).strip()

    amount = input(
        f'Amount [{expense["amount"]}]: '
    ).strip()

    category = input(
        f'Category [{expense["category"]}]: '
    ).strip()

    description = input(
        f'Description [{expense["description"]}]: '
    ).strip()

    payment_method = input(
        f'Payment method [{expense["payment_method"]}]: '
    ).strip()

    if date:
        try:
            datetime.strptime(
                date,
                "%Y-%m-%d"
            )

            expense["date"] = date

        except ValueError:
            print(
                "❌ Invalid date. Keeping old date."
            )

    if amount:
        try:
            amount_value = float(amount)

            if amount_value > 0:
                expense["amount"] = amount_value

            else:
                print(
                    "❌ Amount must be greater than zero."
                )

        except ValueError:
            print(
                "❌ Invalid amount. Keeping old amount."
            )

    if category:
        expense["category"] = category

    if description:
        expense["description"] = description

    if payment_method:
        expense["payment_method"] = payment_method

    save_data()

    print(
        "\n✅ Expense updated successfully!"
    )

    print("💾 Changes saved.")


def delete_expense(user):
    print("\n🗑️ DELETE EXPENSE")

    user_expenses = get_user_expenses(
        user["id"]
    )

    if not user_expenses:
        print(
            "No expenses found."
        )

        return

    view_expenses(user)

    try:
        expense_id = int(
            input(
                "\nEnter expense ID to delete: "
            )
        )

    except ValueError:
        print(
            "❌ Invalid ID."
        )

        return

    expense = get_expense_by_id(
        expense_id,
        user["id"]
    )

    if expense is None:
        print(
            "❌ Expense not found."
        )

        return

    display_expense(expense)

    confirmation = input(
        "\nAre you sure you want to delete "
        "this expense? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        expenses.remove(expense)

        save_data()

        print(
            "\n✅ Expense deleted successfully!"
        )

        print(
            "💾 Changes saved."
        )

    else:
        print(
            "\n❌ Delete cancelled."
        )


def export_report_pdf(user):
    print("\n📄 EXPORT PDF REPORT")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("❌ Invalid month.")
            return

    except ValueError:
        print("❌ Invalid date.")
        return

    expenses = monthly_expenses(
        user,
        year,
        month
    )

    if not expenses:
        print("\n❌ No expenses found for this month.")
        return

    filename = input(
        "\nEnter PDF filename: "
    ).strip()

    if not filename:
        filename = (
            f"expense_report_{year}_{month:02d}.pdf"
        )

    if not filename.endswith(".pdf"):
        filename += ".pdf"

    total = sum(
        expense["amount"]
        for expense in expenses
    )

    days_in_month = calendar.monthrange(
        year,
        month
    )[1]

    daily_average = total / days_in_month

    category_totals = {}

    for expense in expenses:
        category = expense["category"].strip().lower()

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense["amount"]
        )

    try:
        pdf = canvas.Canvas(
            filename,
            pagesize=A4
        )

        width, height = A4

        y = height - 50

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawString(
            50,
            y,
            "SMART EXPENSE TRACKER"
        )

        y -= 30

        pdf.setFont(
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            50,
            y,
            f"Monthly Report: {year}-{month:02d}"
        )

        y -= 35

        pdf.setFont(
            "Helvetica",
            11
        )

        pdf.drawString(
            50,
            y,
            f"User: {user['name']}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Total Spent: ₦{total:,.2f}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Average Daily: ₦{daily_average:,.2f}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Transactions: {len(expenses)}"
        )

        y -= 35

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.drawString(
            50,
            y,
            "SPENDING BY CATEGORY"
        )

        y -= 25

        pdf.setFont(
            "Helvetica",
            10
        )

        sorted_categories = sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for category, amount in sorted_categories:

            percentage = (
                amount / total
            ) * 100

            pdf.drawString(
                50,
                y,
                f"{category}: ₦{amount:,.2f} "
                f"({percentage:.1f}%)"
            )

            y -= 18

            if y < 70:
                pdf.showPage()
                y = height - 50

                pdf.setFont(
                    "Helvetica",
                    10
                )

        y -= 15

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.drawString(
            50,
            y,
            "TRANSACTIONS"
        )

        y -= 25

        pdf.setFont(
            "Helvetica",
            9
        )

        for expense in expenses:

            line = (
                f"{expense['date']} | "
                f"{expense['category']} | "
                f"₦{expense['amount']:,.2f} | "
                f"{expense['description']} | "
                f"{expense['payment_method']}"
            )

            pdf.drawString(
                50,
                y,
                line[:115]
            )

            y -= 15

            if y < 50:
                pdf.showPage()
                y = height - 50

                pdf.setFont(
                    "Helvetica",
                    9
                )

        pdf.save()

        print(
            f"\n✅ Report exported successfully."
        )

        print(
            f"📄 File: {filename}"
        )

    except Exception as error:
        print(
            f"\n❌ PDF export failed: {error}"
        )


def export_backup(user):
    print("\n💾 EXPORT BACKUP")

    filename = input(
        "Enter backup filename [expense_tracker_backup.json]: "
    ).strip()

    if not filename:
        filename = "expense_tracker_backup.json"

    if not filename.endswith(".json"):
        filename += ".json"

    data = {
        "users": users,
        "expenses": expenses,
        "budgets": budgets
    }

    try:
        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

        print(
            f"\n✅ Backup exported successfully."
        )

        print(
            f"📄 File: {filename}"
        )

    except OSError as error:
        print(
            f"\n❌ Backup export failed: {error}"
        )


def import_backup(user):
    global users
    global expenses
    global budgets

    print("\n📥 IMPORT BACKUP")

    filename = input(
        "Enter backup filename: "
    ).strip()

    if not filename:
        print("❌ Filename cannot be empty.")
        return

    try:
        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print(
                "❌ Invalid backup format."
            )
            return

        imported_users = data.get(
            "users",
            []
        )

        imported_expenses = data.get(
            "expenses",
            []
        )

        imported_budgets = data.get(
            "budgets",
            []
        )

        if not isinstance(imported_users, list):
            print("❌ Invalid users data.")
            return

        if not isinstance(
            imported_expenses,
            list
        ):
            print("❌ Invalid expenses data.")
            return

        if not isinstance(
            imported_budgets,
            list
        ):
            print("❌ Invalid budgets data.")
            return

        confirm = input(
            "\n⚠️ This will replace current data. "
            "Continue? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("❌ Backup import cancelled.")
            return

        users = imported_users
        expenses = imported_expenses
        budgets = imported_budgets

        save_data()

        print(
            "\n✅ Backup imported successfully."
        )

        print(
            f"👤 Users: {len(users)}"
        )

        print(
            f"💸 Expenses: {len(expenses)}"
        )

        print(
            f"💰 Budgets: {len(budgets)}"
        )

    except FileNotFoundError:
        print(
            "\n❌ Backup file not found."
        )

    except json.JSONDecodeError:
        print(
            "\n❌ Invalid JSON backup file."
        )

    except OSError as error:
        print(
            f"\n❌ Backup import failed: {error}"
        )


def import_export_menu(user):
    while True:
        print("\n📁 IMPORT / EXPORT")
        print("1. Export Expenses to CSV")
        print("2. Import Expenses from CSV")
        print("3. Import Bank Statement")
        print("4. Export PDF Report")
        print("5. Export Backup")
        print("6. Import Backup")
        print("7. Back")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            export_expenses_csv(user)

        elif choice == "2":
            import_expenses_csv(user)

        elif choice == "3":
            import_bank_statement(user)

        elif choice == "4":
            export_report_pdf(user)

        elif choice == "5":
            export_backup(user)

        elif choice == "6":
            import_backup(user)

        elif choice == "7":
            break

        else:
            print(
                "\n❌ Invalid option. Please choose 1–7."
            )


def user_menu(user):
    while True:
        print(
            f'\n💸 SMART EXPENSE TRACKER — '
            f'{user["name"]} 💸'
        )

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Filter Expenses")
        print("6. Monthly Summary")
        print("7. Budget Management")
        print("8. Analytics")
        print("9. Import / Export")
        print("10. Switch User")
        print("11. Convert Currency")
        print("12. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            add_expense(user)

        elif choice == "2":
            view_expenses(user)

        elif choice == "3":
            edit_expense(user)

        elif choice == "4":
            delete_expense(user)

        elif choice == "5":
            filter_expenses(user)

        elif choice == "6":
            monthly_summary(user)

        elif choice == "7":
            budget_menu(user)

        elif choice == "8":
            analytics_menu(user)

        elif choice == "9":
            import_export_menu(user)

        elif choice == "10":
            user = select_user()
        
        elif choice == "11":
            convert_currency()

        elif choice == "12":
            print("\n👋 Goodbye!")
            break


        else:
            print(
                "\n❌ Invalid option. "
                "Please choose 1–9."
            )


def user_expenses(user):
    return get_user_expenses(user["id"])


def monthly_spending_trends(user):
    print("\n📈 MONTHLY SPENDING TRENDS")

    try:
        year = int(input("Enter year: "))

    except ValueError:
        print("❌ Invalid year.")
        return

    monthly_totals = {}

    for month in range(1, 13):
        expenses = monthly_expenses(
            user,
            year,
            month
        )

        total = sum(
            expense["amount"]
            for expense in expenses
        )

        monthly_totals[month] = total

    print(f"\n📈 SPENDING TRENDS FOR {year}")

    for month, total in monthly_totals.items():
        month_name = calendar.month_name[month]

        if total > 0:
            bar_length = min(
                30,
                max(
                    1,
                    int(total / 5000)
                )
            )

            bar = "█" * bar_length
        else:
            bar = ""

        print(
            f"{month_name:<10} "
            f"₦{total:>12,.2f} "
            f"{bar}"
        )

    total_year = sum(monthly_totals.values())

    print(
        f"\n💰 Total Spending: "
        f"₦{total_year:,.2f}"
    )


def year_over_year_comparison(user):
    print("\n📊 YEAR-OVER-YEAR COMPARISON")

    try:
        current_year = int(
            input("Enter year to compare: ")
        )

    except ValueError:
        print("❌ Invalid year.")
        return

    previous_year = current_year - 1

    user_expense_list = get_user_expenses(
        user["id"]
    )

    current_total = 0
    previous_total = 0

    for expense in user_expense_list:
        try:
            expense_year = datetime.strptime(
                expense["date"],
                "%Y-%m-%d"
            ).year

        except ValueError:
            continue

        if expense_year == current_year:
            current_total += expense["amount"]

        elif expense_year == previous_year:
            previous_total += expense["amount"]

    print(
        f"\n📊 {previous_year} vs {current_year}"
    )

    print(
        f"{previous_year} Spending: "
        f"₦{previous_total:,.2f}"
    )

    print(
        f"{current_year} Spending: "
        f"₦{current_total:,.2f}"
    )

    difference = current_total - previous_total

    if previous_total > 0:

        percentage_change = (
            difference / previous_total
        ) * 100

        if difference > 0:
            print(
                f"📈 Increase: "
                f"₦{difference:,.2f}"
            )

            print(
                f"📊 Percentage Change: "
                f"{percentage_change:.2f}%"
            )

        elif difference < 0:
            print(
                f"📉 Decrease: "
                f"₦{abs(difference):,.2f}"
            )

            print(
                f"📊 Percentage Change: "
                f"{abs(percentage_change):.2f}%"
            )

        else:
            print(
                "➡️ Spending remained the same."
            )

    elif current_total > 0:

        print(
            f"📈 Increase: "
            f"₦{difference:,.2f}"
        )

        print(
            "📊 Percentage Change: "
            "N/A (no previous-year spending)"
        )

    else:

        print(
            "➡️ Spending remained the same."
        )


def analytics_menu(user):
    while True:
        print("\n📈 ANALYTICS")
        print("1. Category Breakdown")
        print("2. Top Spending Categories")
        print("3. Daily Average Spending")
        print("4. Monthly Spending Trends")
        print("5. Year-over-Year Comparison")
        print("6. Detect Recurring Expenses")
        print("7. Back")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            category_breakdown(user)

        elif choice == "2":
            top_spending_categories(user)

        elif choice == "3":
            daily_average_spending(user)

        elif choice == "4":
            monthly_spending_trends(user)

        elif choice == "5":
            year_over_year_comparison(user)

        elif choice == "6":
            detect_recurring_expenses(user)

        elif choice == "7":
            break

        else:
            print(
                "\n❌ Invalid option. Please choose 1–6."
            )


def export_expenses_csv(user):
    print("\n📤 EXPORT EXPENSES TO CSV")

    filename = input(
        "Enter filename (example: expenses.csv): "
    ).strip()

    if not filename:
        print("❌ Filename cannot be empty.")
        return

    if not filename.endswith(".csv"):
        filename += ".csv"

    expenses = user_expenses(user)

    if not expenses:
        print("\n❌ No expenses to export.")
        return

    fields = [
        "id",
        "date",
        "amount",
        "category",
        "description",
        "payment_method"
    ]

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()

            for expense in expenses:
                writer.writerow({
                    "id": expense["id"],
                    "date": expense["date"],
                    "amount": expense["amount"],
                    "category": expense["category"],
                    "description": expense["description"],
                    "payment_method": expense["payment_method"]
                })

        print(
            f"\n✅ {len(expenses)} expenses exported."
        )

        print(
            f"📄 File: {filename}"
        )

    except OSError as error:
        print(
            f"\n❌ Export failed: {error}"
        )


def import_expenses_csv(user):
    print("\n📥 IMPORT EXPENSES FROM CSV")

    filename = input(
        "Enter CSV filename: "
    ).strip()

    if not filename:
        print("❌ Filename cannot be empty.")
        return

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            required_fields = [
                "date",
                "amount",
                "category",
                "description",
                "payment_method"
            ]

            if not reader.fieldnames:
                print("❌ CSV file is empty.")
                return

            missing_fields = [
                field
                for field in required_fields
                if field not in reader.fieldnames
            ]

            if missing_fields:
                print(
                    "\n❌ Missing required columns:"
                )

                for field in missing_fields:
                    print(f"- {field}")

                return

            imported = 0
            skipped = 0

            for row in reader:

                try:
                    date = datetime.strptime(
                        row["date"].strip(),
                        "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")

                    amount = float(
                        row["amount"].strip()
                    )

                    if amount <= 0:
                        skipped += 1
                        continue

                    category = row[
                        "category"
                    ].strip()

                    description = row[
                        "description"
                    ].strip()

                    payment_method = row[
                        "payment_method"
                    ].strip()

                    if not category:
                        skipped += 1
                        continue

                    expense = {
                        "id": get_next_expense_id(),
                        "user_id": user["id"],
                        "date": date,
                        "amount": amount,
                        "category": category,
                        "description": description,
                        "payment_method": payment_method
                    }

                    expenses.append(expense)

                    imported += 1

                except (
                    ValueError,
                    KeyError
                ):
                    skipped += 1

        save_data()

        print(
            f"\n✅ {imported} transactions imported."
        )

        if skipped:
            print(
                f"⚠️ {skipped} rows skipped."
            )

        print("💾 Changes saved.")

    except FileNotFoundError:
        print(
            "\n❌ File not found."
        )

    except OSError as error:
        print(
            f"\n❌ Import failed: {error}"
        )


def import_bank_statement(user):
    print("\n🏦 IMPORT BANK STATEMENT")

    filename = input(
        "Enter bank statement CSV filename: "
    ).strip()

    if not filename:
        print("❌ Filename cannot be empty.")
        return

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("❌ CSV file is empty.")
                return

            print("\nDetected columns:")

            for column in reader.fieldnames:
                print(f"- {column}")

            imported = 0
            skipped = 0

            for row in reader:

                try:
                    date_value = (
                        row.get("date")
                        or row.get("Date")
                        or row.get("DATE")
                    )

                    amount_value = (
                        row.get("amount")
                        or row.get("Amount")
                        or row.get("AMOUNT")
                        or row.get("debit")
                        or row.get("Debit")
                        or row.get("DEBIT")
                    )

                    category_value = (
                        row.get("category")
                        or row.get("Category")
                        or "Bank Statement"
                    )

                    description_value = (
                        row.get("description")
                        or row.get("Description")
                        or row.get("Narration")
                        or row.get("narration")
                        or ""
                    )

                    payment_value = (
                        row.get("payment_method")
                        or row.get("Payment Method")
                        or row.get("Payment")
                        or "Bank"
                    )

                    if not date_value or not amount_value:
                        skipped += 1
                        continue

                    date_value = date_value.strip()

                    date_formats = [
                        "%Y-%m-%d",
                        "%d/%m/%Y",
                        "%d-%m-%Y",
                        "%m/%d/%Y"
                    ]

                    parsed_date = None

                    for date_format in date_formats:
                        try:
                            parsed_date = datetime.strptime(
                                date_value,
                                date_format
                            )
                            break
                        except ValueError:
                            continue

                    if parsed_date is None:
                        skipped += 1
                        continue

                    amount_text = (
                        str(amount_value)
                        .strip()
                        .replace(",", "")
                        .replace("₦", "")
                        .replace("$", "")
                        .replace("€", "")
                    )

                    amount = float(amount_text)

                    if amount <= 0:
                        skipped += 1
                        continue

                    expense = {
                        "id": get_next_expense_id(),
                        "user_id": user["id"],
                        "date": parsed_date.strftime(
                            "%Y-%m-%d"
                        ),
                        "amount": amount,
                        "category": category_value.strip(),
                        "description": description_value.strip(),
                        "payment_method": payment_value.strip()
                    }

                    expenses.append(expense)

                    imported += 1

                except (
                    ValueError,
                    TypeError,
                    AttributeError
                ):
                    skipped += 1

        save_data()

        print(
            f"\n✅ {imported} transactions imported."
        )

        if skipped:
            print(
                f"⚠️ {skipped} rows skipped."
            )

        print("💾 Changes saved.")

    except FileNotFoundError:
        print(
            "\n❌ Bank statement file not found."
        )

    except OSError as error:
        print(
            f"\n❌ Import failed: {error}"
        )


def convert_currency():
    print("\n💱 CURRENCY CONVERTER")

    currencies = ["NGN", "USD", "EUR"]

    print("\nAvailable currencies:")
    for currency in currencies:
        print(f"- {currency}")

    from_currency = input(
        "\nFrom currency: "
    ).strip().upper()

    if from_currency not in currencies:
        print("❌ Invalid source currency.")
        return

    to_currency = input(
        "To currency: "
    ).strip().upper()

    if to_currency not in currencies:
        print("❌ Invalid destination currency.")
        return

    try:
        amount = float(
            input("Amount: ").strip()
        )
    except ValueError:
        print("❌ Invalid amount.")
        return

    if amount < 0:
        print("❌ Amount cannot be negative.")
        return

    amount_in_ngn = (
        amount / CURRENCY_RATES[from_currency]
    )

    converted_amount = (
        amount_in_ngn * CURRENCY_RATES[to_currency]
    )

    print(
        f"\n💱 {amount:,.2f} {from_currency}"
        f" = {converted_amount:,.2f} {to_currency}"
    )


def detect_recurring_expenses(user):
    print("\n🔁 RECURRING EXPENSE DETECTION")

    user_expense_list = get_user_expenses(user["id"])

    if not user_expense_list:
        print("❌ No expenses found.")
        return

    groups = {}

    for expense in user_expense_list:
        key = (
            expense["category"].strip().lower(),
            round(float(expense["amount"]), 2),
            expense["description"].strip().lower()
        )

        if key not in groups:
            groups[key] = []

        groups[key].append(expense)

    recurring = []

    for key, matching_expenses in groups.items():
        if len(matching_expenses) < 2:
            continue

        dates = []

        for expense in matching_expenses:
            try:
                expense_date = datetime.strptime(
                    expense["date"],
                    "%Y-%m-%d"
                )
                dates.append(expense_date)
            except ValueError:
                continue

        dates.sort()

        if len(dates) < 2:
            continue

        intervals = []

        for index in range(1, len(dates)):
            difference = (
                dates[index] - dates[index - 1]
            ).days

            intervals.append(difference)

        if not intervals:
            continue

        average_interval = (
            sum(intervals) / len(intervals)
        )

        if (
            25 <= average_interval <= 35
            or 6 <= average_interval <= 8
            or 85 <= average_interval <= 95
            or 350 <= average_interval <= 380
        ):
            recurring.append({
                "category": key[0],
                "amount": key[1],
                "description": key[2],
                "count": len(matching_expenses),
                "average_interval": average_interval
            })

    if not recurring:
        print("\nℹ️ No recurring expenses detected.")
        return

    print(
        f"\n🔁 {len(recurring)} recurring expense(s) detected:"
    )

    for expense in recurring:
        print("\n------------------------------")
        print(
            f"Category: {expense['category'].title()}"
        )
        print(
            f"Amount: ₦{expense['amount']:,.2f}"
        )
        print(
            f"Description: "
            f"{expense['description'].title()}"
        )
        print(
            f"Occurrences: {expense['count']}"
        )
        print(
            f"Average interval: "
            f"{expense['average_interval']:.1f} days"
        )

        if 25 <= expense["average_interval"] <= 35:
            print("Pattern: 📅 Monthly")

        elif 6 <= expense["average_interval"] <= 8:
            print("Pattern: 📅 Weekly")

        elif 85 <= expense["average_interval"] <= 95:
            print("Pattern: 📅 Quarterly")

        elif 350 <= expense["average_interval"] <= 380:
            print("Pattern: 📅 Yearly")




def main():
    load_data()

    while True:
        print(
            "\n💸 SMART EXPENSE TRACKER 💸"
        )

        print("1. Select User")
        print("2. Create User")
        print("3. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            user = select_user()

            if user:
                user_menu(user)

        elif choice == "2":
            create_user()

        elif choice == "3":
            print(
                "\n👋 Goodbye!"
            )

            break

        else:
            print(
                "\n❌ Invalid option. "
                "Please choose 1–3."
            )


if __name__ == "__main__":
    main()