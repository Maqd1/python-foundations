'''
🟢 Easy Level (2 Questions)
Q1: The Bank Account System (Easy)

Create a simple banking system using OOP.

Requirements:

    Create a BankAccount class with:

        Attributes: account_number, owner, balance

        Methods: deposit(), withdraw(), get_balance(), display_info()

        Use encapsulation (private __balance)

    Create a SavingsAccount class that inherits from BankAccount:

        Add interest_rate attribute

        Add calculate_interest() method

        Override withdraw() to prevent going below minimum balance

    Create a CheckingAccount class that inherits from BankAccount:

        Add overdraft_limit attribute

        Override withdraw() to allow overdraft

    Create a simple interactive program that:

        Creates accounts

        Performs transactions

        Displays account info

Sample Output:
text

🏦 BANK ACCOUNT SYSTEM 🏦

1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Display Info
6. Exit

Choice: 1
Type: (1) Savings (2) Checking: 1
Owner: Damilola
Initial Balance: 1000

✅ Savings account created!
Account Number: 1001
Owner: Damilola
Type: Savings
Interest Rate: 2.5%

Choice: 2
Enter account number: 1001
Enter amount: 500
✅ Deposited ₦500.00. New balance: ₦1,500.00

Choice: 3
Enter account number: 1001
Enter amount: 2000
❌ Insufficient funds! Available: ₦1,500.00
Minimum balance: ₦100.00

Choice: 5
Enter account number: 1001

📋 ACCOUNT DETAILS
Account Number: 1001
Owner: Damilola
Type: Savings
Balance: ₦1,500.00
Interest Rate: 2.5%
Annual Interest: ₦37.50

Concepts: Classes, objects, attributes, methods, constructor, inheritance, encapsulation
'''