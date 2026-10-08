# 🎯 CORE PROJECT QUESTIONS

## 1️⃣ EXPENSE TRACKER

# The Smart Expense Tracker with Reports 💰

Build a complete expense tracking system with CSV/JSON storage, categories, and analytics.

---

## 📋 Requirements

### Data Storage

- Store expenses in JSON/CSV
- Fields:
  - `date`
  - `amount`
  - `category`
  - `description`
  - `payment_method`
- Support multiple users

### Core Features

- Add expenses
- Edit expenses
- Delete expenses
- View expenses by category
- View expenses by date range
- Monthly summaries
- Budget tracking by category

### Analytics — HARD

- Monthly spending trends
- Category breakdown (% and amount)
- Top spending categories
- Daily average spending
- Year-over-year comparison

### Advanced Features — HARD

- Export reports to CSV/PDF
- CSV import from bank statements
- Currency conversion (NGN/USD/EUR)
- Recurring expense detection
- Budget alerts when exceeding limits

### Data Persistence

- Auto-save on every change
- Multiple backup versions
- Export/import backup

---

# 💻 Implementation

The Smart Expense Tracker was implemented as a Python CLI application using JSON for persistent storage.

### Implemented Features

| Requirement | Status |
|---|---|
| JSON storage | ✅ |
| CSV export | ✅ |
| Multiple users | ✅ |
| Add expenses | ✅ |
| Edit expenses | ✅ |
| Delete expenses | ✅ |
| Filter by category/date | ✅ |
| Monthly summaries | ✅ |
| Category budgets | ✅ |
| Monthly spending trends | ✅ |
| Category breakdown | ✅ |
| Top spending categories | ✅ |
| Daily average spending | ✅ |
| Year-over-year comparison | ✅ |
| CSV report export | ✅ |
| PDF report export | ✅ |
| Bank statement CSV import | ✅ |
| NGN/USD/EUR conversion | ✅ |
| Recurring expense detection | ✅ |
| Budget alerts | ✅ |
| Auto-save | ✅ |
| Multiple backup versions | ✅ |
| Backup export | ✅ |
| Backup import | ✅ |

---

# 📊 Sample Output

```text
💸 SMART EXPENSE TRACKER 💸

📊 MONTHLY SUMMARY (September 2026)
Total Spent: ₦245,000.00
Average Daily: ₦8,166.67
Transactions: 45

📈 SPENDING BY CATEGORY:
Food: ₦85,000.00 (34.7%) ████████████████████
Transport: ₦45,000.00 (18.4%) ███████████
Bills: ₦55,000.00 (22.4%) █████████████
Shopping: ₦35,000.00 (14.3%) ████████
Others: ₦25,000.00 (10.2%) ██████

📊 BUDGET TRACKING:
Food: ₦100,000.00 budget → ₦85,000.00 used (85%) ✅
Transport: ₦50,000.00 budget → ₦45,000.00 used (90%) ✅
Bills: ₦60,000.00 budget → ₦55,000.00 used (92%) ✅
Shopping: ₦40,000.00 budget → ₦35,000.00 used (88%) ✅

⚠️ ALERT: Entertainment budget 95% used!
Spent: ₦19,000 of ₦20,000 budget

📥 Import CSV: Enter filename
Reading bank_statement.csv...
✅ 45 transactions imported

📤 Export Report: Enter filename
Report exported to: expense_report_2026_09.pdf

💾 Backup created: backup_2026-09-05.json
```

---

# 🧪 Features Tested

The following features were tested during development:

- Monthly spending trends
- Year-over-year comparison
- Recurring expense detection
- Budget tracking
- Budget alerts
- CSV expense export
- Bank statement CSV import
- PDF report export
- Currency conversion
- Backup export/import
- Automatic persistence
- Multiple backup creation
- Multiple-user data separation

Example tested results included:

```text
📊 2025 vs 2026
2025 Spending: ₦0.00
2026 Spending: ₦3,812,500.00
📈 Increase: ₦3,812,500.00
📊 Percentage Change: N/A (no previous-year spending)
```

```text
📊 BUDGET TRACKING — October 2026
food: ₦10,000.00 budget → ₦15,000.00 used (150%) 🚨 OVER BUDGET
```

```text
🔁 RECURRING EXPENSE DETECTION

ℹ️ No recurring expenses detected.
```

---

# 🗂️ Project Files

```text
expense_tracker/
├── README.md
├── expense_tracker.py
└── expenses.json
```

Generated test files and backup artifacts are not included in the committed project.

---

# 🧠 Concepts Practiced

- JSON
- CSV
- File handling
- Data persistence
- CRUD operations
- Functions
- Lists and dictionaries
- Date handling
- Data filtering
- Data aggregation
- Analytics
- Reporting
- Import/export
- Backup management
- Multiple-user data management
- Budget tracking
- Currency conversion
- Error handling
- Python CLI applications

---

# 🚀 Running the Project

From the project directory:

```bash
python expense_tracker.py
```

The application provides:

```text
💸 SMART EXPENSE TRACKER 💸
1. Select User
2. Create User
3. Exit
```

After selecting a user, the main application menu provides access to expense management, budgets, analytics, import/export, currency conversion, and persistence features.