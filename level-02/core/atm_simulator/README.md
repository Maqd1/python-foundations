# 🏧 Core ATM Simulator

## The Banking System with Fraud Detection 💳

Create a realistic ATM banking system with security features.

## Account System

Use pre-registered accounts with information such as PIN, name, balance, savings, transactions, daily withdrawal limits, and daily withdrawal usage.

Example:

```python
accounts = {
    "12345678": {
        "pin": "1234",
        "name": "Damilola",
        "balance": 5000.00,
        "savings": 2000.00,
        "transactions": [],
        "daily_limit": 500.00,
        "daily_withdrawn": 0.00
    },
    "87654321": {
        "pin": "4321",
        "name": "John",
        "balance": 3000.00,
        "savings": 1000.00,
        "transactions": [],
        "daily_limit": 300.00,
        "daily_withdrawn": 0.00
    }
}
```

## Features

### 1. Secure Login

* Give the user **3 attempts** to enter the correct PIN.
* After 3 failed attempts, display:

  ```text
  Account locked for 30 minutes
  ```
* Track failed attempts in a **separate dictionary**.

### 2. Main Menu

Provide the following options:

1. Check Balance
2. Withdraw
3. Deposit
4. Transfer
5. Transaction History
6. Change PIN
7. Exit

Changing the PIN requires:

* The old PIN
* Confirmation of the new PIN

### 3. Withdraw Logic — Hard Part

The withdrawal system must:

* Check the daily withdrawal limit.
* Check whether the account has enough balance.
* Check whether the ATM has enough cash.
* Maintain an ATM cash pool.
* Dispense specific denominations:

  * ₦100
  * ₦200
  * ₦500
  * ₦1,000
* Calculate exactly how many of each denomination should be dispensed.

### 4. Transfer Logic — Harder

The transfer system must:

* Verify that the recipient account exists.
* Check that the sender has enough balance.
* Add a transfer fee of **1.5% of the transfer amount**.
* Apply a **minimum fee of ₦50**.
* Show the fee breakdown before confirmation.
* Ask the user to confirm the transfer.

### 5. Transaction History

Store every transaction with:

```text
[timestamp, type, amount, balance_after]
```

The system should:

* Display the **last 10 transactions**.
* Allow filtering by transaction type:

  * Withdrawal
  * Deposit
  * Transfer

### 6. Security Features

If there are **3 wrong PIN attempts on any account**, trigger:

```text
panic mode
```

During panic mode:

1. Ask the user a security question.
2. If the security answer is correct, continue according to the system's security logic.
3. If the security answer is wrong, **freeze all accounts**.

## Sample Output

```text
🏦 WELCOME TO PYTHON BANK ATM 🏦
Enter Account Number: 12345678
Enter PIN: ****

✅ Welcome, Damilola!

===== MAIN MENU =====
1. Check Balance
2. Withdraw
3. Deposit
4. Transfer
5. Transaction History
6. Change PIN
7. Exit

Choice: 2
Enter amount: 2500

💰 Withdrawal Breakdown:
2 × ₦1000 = ₦2000
2 × ₦200 = ₦400
1 × ₦100 = ₦100
Total: ₦2500

Daily limit: ₦5000 | Today's usage: ₦0
Proceed? (y/n): y

✅ Transaction successful!
New balance: ₦2500.00

Choice: 4
Enter recipient account: 87654321
Enter amount: 500
Transfer fee: ₦7.50 (1.5%)
Total deducted: ₦507.50
Confirm? (y/n): y

✅ Transfer successful!
New balance: ₦1992.50

Choice: 5
===== TRANSACTION HISTORY =====
1. 2026-01-15 14:23 | Withdrawal | ₦2500 | Balance: ₦2500.00
2. 2026-01-15 14:25 | Transfer   | ₦500  | Balance: ₦1992.50
3. 2026-01-15 14:20 | Deposit    | ₦1000 | Balance: ₦5000.00

Choice: 7
Thank you for banking with us! 👋
```

## Concepts Tested

* Dictionaries
* Nested dictionaries
* `while` loops
* `for` loops
* String methods
* f-strings
* Functions
* Multiple return values
* Variable scope
* Error handling
* `break`
* `continue`
* `match`
* `if / elif / else`
* Transaction tracking
* State management
