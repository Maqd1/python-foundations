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


from datetime import datetime, timedelta

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

failed_attempts = {}   # account_number -> consecutive wrong-PIN count
locked_until = {}      # account_number -> datetime the lock expires

atm_cash = {1000: 20, 500: 10, 200: 30, 100: 40}  # ATM's note pool

SECURITY_QUESTION = "Security check — what is the bank's secret word? "
SECURITY_ANSWER = "python"  # simplified: one shared security answer for the demo

system_frozen = False


def naira(amount):
    return f"\u20a6{amount:,.2f}"


def record_transaction(acct_num, ttype, amount, balance_after):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    accounts[acct_num]["transactions"].append({
        "timestamp": timestamp,
        "type": ttype,
        "amount": amount,
        "balance_after": balance_after,
    })


def is_locked(acct_num):
    lock_time = locked_until.get(acct_num)
    if lock_time is None:
        return False
    if datetime.now() >= lock_time:
        del locked_until[acct_num]
        failed_attempts[acct_num] = 0
        return False
    remaining = lock_time - datetime.now()
    minutes_left = int(remaining.total_seconds() // 60) + 1
    print(f"\U0001f512 Account locked. Try again in {minutes_left} minute(s).")
    return True


def trigger_panic_mode():
    """Runs after any account hits 3 failed PIN attempts. Wrong answer freezes the system."""
    global system_frozen
    print("\n\U0001f6a8 SECURITY ALERT: multiple failed login attempts detected.")
    answer = input(SECURITY_QUESTION).strip().lower()
    if answer != SECURITY_ANSWER:
        system_frozen = True
        print("\u274c Incorrect security answer. ALL ACCOUNTS HAVE BEEN FROZEN.")
    else:
        print("\u2705 Security check passed.")


def login():
    if system_frozen:
        print("\U0001f6a8 SYSTEM FROZEN. Please contact your bank administrator.")
        return None

    acct_num = input("Enter Account Number: ").strip()
    if acct_num not in accounts:
        print("\u274c Account not found.")
        return None

    if is_locked(acct_num):
        return None

    attempts = failed_attempts.get(acct_num, 0)
    while attempts < 3:
        pin = input("Enter PIN: ").strip()
        if pin == accounts[acct_num]["pin"]:
            failed_attempts[acct_num] = 0
            print(f"\u2705 Welcome, {accounts[acct_num]['name']}!")
            return acct_num

        attempts += 1
        failed_attempts[acct_num] = attempts
        remaining = 3 - attempts
        if remaining > 0:
            print(f"\u274c Incorrect PIN. {remaining} attempt(s) remaining.")
        else:
            locked_until[acct_num] = datetime.now() + timedelta(minutes=30)
            print("\U0001f512 Account locked for 30 minutes.")
            trigger_panic_mode()

    return None


def check_balance(acct_num):
    acct = accounts[acct_num]
    print(f"\n\U0001f4b0 Current balance: {naira(acct['balance'])}")
    print(f"\U0001f3e6 Savings balance: {naira(acct['savings'])}")


def calculate_denominations(amount):
    """Greedy dispensing limited by the ATM's actual note counts.
    Returns (breakdown_dict, success_bool) — success is False if the
    exact amount can't be made with what's left in the machine."""
    remaining = amount
    breakdown = {}
    for note in sorted(atm_cash.keys(), reverse=True):
        if remaining <= 0:
            break
        available = atm_cash[note]
        needed = int(remaining // note)
        use = min(needed, available)
        if use > 0:
            breakdown[note] = use
            remaining -= use * note
    return breakdown, remaining == 0


def withdraw(acct_num):
    acct = accounts[acct_num]
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("\u274c Invalid amount.")
        return
    if amount <= 0:
        print("\u274c Amount must be positive.")
        return
    if amount % 100 != 0:
        print("\u274c Amount must be in multiples of \u20a6100.")
        return

    if acct["daily_withdrawn"] + amount > acct["daily_limit"]:
        remaining_limit = acct["daily_limit"] - acct["daily_withdrawn"]
        print(f"\u274c Daily limit exceeded. You can withdraw up to {naira(remaining_limit)} more today.")
        return

    if amount > acct["balance"]:
        print("\u274c Insufficient balance.")
        return

    breakdown, possible = calculate_denominations(amount)
    if not possible:
        print("\u274c ATM cannot dispense this exact amount with available notes. Try a different amount.")
        return

    print("\n\U0001f4b0 Withdrawal Breakdown:")
    for note in sorted(breakdown.keys(), reverse=True):
        count = breakdown[note]
        print(f"{count} \u00d7 {naira(note)} = {naira(note * count)}")
    print(f"Total: {naira(amount)}")
    print(f"Daily limit: {naira(acct['daily_limit'])} | Today's usage: {naira(acct['daily_withdrawn'])}")

    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm != "y":
        print("Transaction cancelled.")
        return

    for note, count in breakdown.items():
        atm_cash[note] -= count
    acct["balance"] -= amount
    acct["daily_withdrawn"] += amount
    record_transaction(acct_num, "Withdrawal", amount, acct["balance"])
    print("\u2705 Transaction successful!")
    print(f"New balance: {naira(acct['balance'])}")


def deposit(acct_num):
    acct = accounts[acct_num]
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("\u274c Invalid amount.")
        return
    if amount <= 0:
        print("\u274c Amount must be positive.")
        return

    acct["balance"] += amount
    record_transaction(acct_num, "Deposit", amount, acct["balance"])
    print("\u2705 Deposit successful!")
    print(f"New balance: {naira(acct['balance'])}")


def transfer(acct_num):
    acct = accounts[acct_num]
    recipient_num = input("Enter recipient account: ").strip()

    if recipient_num == acct_num:
        print("\u274c You cannot transfer to your own account.")
        return
    if recipient_num not in accounts:
        print("\u274c Recipient account not found.")
        return

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("\u274c Invalid amount.")
        return
    if amount <= 0:
        print("\u274c Amount must be positive.")
        return

    fee = max(0.015 * amount, 50)
    total_deducted = amount + fee

    if total_deducted > acct["balance"]:
        print("\u274c Insufficient balance to cover transfer + fee.")
        return

    print(f"\nTransfer fee: {naira(fee)} (1.5%, \u20a650 minimum)")
    print(f"Total deducted: {naira(total_deducted)}")
    confirm = input("Confirm? (y/n): ").strip().lower()
    if confirm != "y":
        print("Transfer cancelled.")
        return

    acct["balance"] -= total_deducted
    accounts[recipient_num]["balance"] += amount

    record_transaction(acct_num, "Transfer", amount, acct["balance"])
    record_transaction(recipient_num, "Transfer In", amount, accounts[recipient_num]["balance"])

    print("\u2705 Transfer successful!")
    print(f"New balance: {naira(acct['balance'])}")


def transaction_history(acct_num):
    acct = accounts[acct_num]
    if not acct["transactions"]:
        print("\nNo transactions yet.")
        return

    filter_choice = input("Filter by type? (withdraw/deposit/transfer/all): ").strip().lower()

    filtered = acct["transactions"]
    if filter_choice not in ("all", ""):
        filtered = [t for t in acct["transactions"] if filter_choice in t["type"].lower()]

    recent = filtered[-10:][::-1]  # last 10, most recent first

    print("\n===== TRANSACTION HISTORY =====")
    if not recent:
        print("No matching transactions.")
        return
    for i, t in enumerate(recent, start=1):
        print(f"{i}. {t['timestamp']} | {t['type']:<11} | {naira(t['amount'])} | Balance: {naira(t['balance_after'])}")


def change_pin(acct_num):
    acct = accounts[acct_num]
    old_pin = input("Enter current PIN: ").strip()
    if old_pin != acct["pin"]:
        print("\u274c Incorrect current PIN.")
        return

    new_pin = input("Enter new PIN: ").strip()
    confirm_pin = input("Confirm new PIN: ").strip()

    if not new_pin.isdigit() or len(new_pin) != 4:
        print("\u274c PIN must be exactly 4 digits.")
        return
    if new_pin != confirm_pin:
        print("\u274c New PIN and confirmation do not match.")
        return

    acct["pin"] = new_pin
    print("\u2705 PIN changed successfully.")


def main_menu(acct_num):
    while True:
        print("\n===== MAIN MENU =====")
        print("1. Check Balance")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Exit")
        choice = input("Choice: ").strip()

        match choice:
            case "1":
                check_balance(acct_num)
            case "2":
                withdraw(acct_num)
            case "3":
                deposit(acct_num)
            case "4":
                transfer(acct_num)
            case "5":
                transaction_history(acct_num)
            case "6":
                change_pin(acct_num)
            case "7":
                print("Thank you for banking with us! \U0001f44b")
                break
            case _:
                print("\u274c Invalid choice.")


def main():
    print("\U0001f3e6 WELCOME TO PYTHON BANK ATM \U0001f3e6")
    while True:
        if system_frozen:
            print("\U0001f6a8 SYSTEM FROZEN. Please contact your bank administrator.")
            break
        acct_num = login()
        if acct_num:
            main_menu(acct_num)
        again = input("\nAnother session? (y/n): ").strip().lower()
        if again != "y":
            break


if __name__ == "__main__":
    main()


    