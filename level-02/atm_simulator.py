'''
Core 2

🏧 CORE ATM SIMULATOR

The Banking System with Fraud Detection 💳

Create a realistic ATM banking system with security features!

Account System:

```python
# Pre-registered accounts
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

Features:

1. Secure Login:
   · 3 attempts for PIN
   · After 3 failures: "Account locked for 30 minutes"
   · Track failed attempts in a separate dictionary
2. Main Menu:
   · Check Balance
   · Withdraw
   · Deposit
   · Transfer (to another account)
   · View Transaction History
   · Change PIN (requires OLD PIN + NEW PIN confirmation)
3. Withdraw Logic (HARD PART):
   · Check daily limit
   · Check if enough balance
   · Check if ATM has enough cash (maintain ATM cash pool)
   · Dispense in specific denominations: 100, 200, 500, 1000 notes
   · Calculate exactly how many of each note to dispense
4. Transfer Logic (HARDER):
   · Verify recipient account exists
   · Check if sender has enough balance
   · Add fee: 1.5% of transfer amount (minimum ₦50)
   · Show fee breakdown before confirming
5. Transaction History:
   · Store each transaction: [timestamp, type, amount, balance_after]
   · Show last 10 transactions
   · Allow filtering by type (withdraw/deposit/transfer)
6. Security Features:
   · If 3 wrong PIN attempts on ANY account → trigger "panic mode"
   · Panic mode: Ask for security question
   · Wrong security answer → freeze all accounts

Sample Output:

```
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

Concepts Tested: Dictionaries, nested dictionaries, while loops, for loops, string methods, f-strings, functions, multiple returns, scope, error handling (implicit), break, continue, match or if/elif for menu

---
'''