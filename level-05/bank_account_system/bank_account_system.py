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

class BankAccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be greater than ₦0.")
            return

        self.__balance += amount
        print(
            f"✅ Deposited ₦{amount:,.2f}. "
            f"New balance: ₦{self.__balance:,.2f}"
        )

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be greater than ₦0.")
            return False

        if amount > self.__balance:
            print(
                f"❌ Insufficient funds! "
                f"Available: ₦{self.__balance:,.2f}"
            )
            return False

        self.__balance -= amount
        print(
            f"✅ Withdrawn ₦{amount:,.2f}. "
            f"New balance: ₦{self.__balance:,.2f}"
        )
        return True

    def get_balance(self):
        return self.__balance

    def display_info(self):
        print("\n📋 ACCOUNT DETAILS")
        print(f"Account Number: {self.account_number}")
        print(f"Owner: {self.owner}")
        print(f"Balance: ₦{self.__balance:,.2f}")


class SavingsAccount(BankAccount):
    def __init__(
        self,
        account_number,
        owner,
        balance=0,
        interest_rate=2.5,
        minimum_balance=100
    ):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance

    def calculate_interest(self):
        return self.get_balance() * (self.interest_rate / 100)

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be greater than ₦0.")
            return False

        remaining_balance = self.get_balance() - amount

        if remaining_balance < self.minimum_balance:
            print(
                f"❌ Insufficient funds! "
                f"Available: ₦{self.get_balance():,.2f}"
            )
            print(
                f"Minimum balance: ₦{self.minimum_balance:,.2f}"
            )
            return False

        return super().withdraw(amount)

    def display_info(self):
        super().display_info()
        print(f"Type: Savings")
        print(f"Interest Rate: {self.interest_rate}%")
        print(
            f"Annual Interest: "
            f"₦{self.calculate_interest():,.2f}"
        )


class CheckingAccount(BankAccount):
    def __init__(
        self,
        account_number,
        owner,
        balance=0,
        overdraft_limit=500
    ):
        super().__init__(account_number, owner, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be greater than ₦0.")
            return False

        available = self.get_balance() + self.overdraft_limit

        if amount > available:
            print(
                f"❌ Withdrawal exceeds overdraft limit!"
            )
            print(
                f"Available: ₦{available:,.2f}"
            )
            return False

        # Accessing the private balance directly is not possible.
        # We use a controlled transaction through the parent class.
        current_balance = self.get_balance()

        if amount <= current_balance:
            return super().withdraw(amount)

        overdraft_used = amount - current_balance

        # Bring the account balance to zero first.
        if current_balance > 0:
            super().withdraw(current_balance)

        # Then represent the overdraft portion.
        self._apply_overdraft(overdraft_used)

        print(
            f"✅ Withdrawn ₦{amount:,.2f}. "
            f"New balance: ₦-{overdraft_used:,.2f}"
        )
        return True

    def _apply_overdraft(self, amount):
        # This method is intentionally overridden below by
        # maintaining the overdraft amount separately.
        if not hasattr(self, "_overdraft_used"):
            self._overdraft_used = 0

        self._overdraft_used += amount

    def get_balance(self):
        balance = super().get_balance()
        overdraft_used = getattr(self, "_overdraft_used", 0)
        return balance - overdraft_used

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be greater than ₦0.")
            return

        overdraft_used = getattr(self, "_overdraft_used", 0)

        if overdraft_used > 0:
            if amount >= overdraft_used:
                remaining = amount - overdraft_used
                self._overdraft_used = 0

                if remaining > 0:
                    super().deposit(remaining)
                else:
                    print(
                        f"✅ Deposited ₦{amount:,.2f}. "
                        f"Overdraft cleared."
                    )
            else:
                self._overdraft_used -= amount
                print(
                    f"✅ Deposited ₦{amount:,.2f}. "
                    f"Overdraft reduced."
                )
        else:
            super().deposit(amount)

    def display_info(self):
        print("\n📋 ACCOUNT DETAILS")
        print(f"Account Number: {self.account_number}")
        print(f"Owner: {self.owner}")
        print(f"Type: Checking")
        print(f"Balance: ₦{self.get_balance():,.2f}")
        print(
            f"Overdraft Limit: "
            f"₦{self.overdraft_limit:,.2f}"
        )


def get_account(accounts):
    try:
        account_number = int(input("Enter account number: "))
    except ValueError:
        print("❌ Account number must be a number.")
        return None

    account = accounts.get(account_number)

    if account is None:
        print("❌ Account not found.")

    return account


def create_account(accounts, next_account_number):
    print("\n1. Savings")
    print("2. Checking")

    account_type = input("Type: ")

    owner = input("Owner: ")

    try:
        initial_balance = float(input("Initial Balance: ₦"))
    except ValueError:
        print("❌ Invalid balance.")
        return next_account_number

    if initial_balance < 0:
        print("❌ Initial balance cannot be negative.")
        return next_account_number

    account_number = next_account_number

    if account_type == "1":
        account = SavingsAccount(
            account_number,
            owner,
            initial_balance
        )
        account_type_name = "Savings"

    elif account_type == "2":
        account = CheckingAccount(
            account_number,
            owner,
            initial_balance
        )
        account_type_name = "Checking"

    else:
        print("❌ Invalid account type.")
        return next_account_number

    accounts[account_number] = account

    print(f"\n✅ {account_type_name} account created!")
    print(f"Account Number: {account_number}")
    print(f"Owner: {owner}")
    print(f"Type: {account_type_name}")

    if isinstance(account, SavingsAccount):
        print(f"Interest Rate: {account.interest_rate}%")
    else:
        print(
            f"Overdraft Limit: "
            f"₦{account.overdraft_limit:,.2f}"
        )

    return next_account_number + 1


def main():
    accounts = {}
    next_account_number = 1001

    print("\n🏦 BANK ACCOUNT SYSTEM 🏦")

    while True:
        print("\n1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Display Info")
        print("6. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            next_account_number = create_account(
                accounts,
                next_account_number
            )

        elif choice == "2":
            account = get_account(accounts)

            if account:
                try:
                    amount = float(input("Enter amount: ₦"))
                    account.deposit(amount)
                except ValueError:
                    print("❌ Invalid amount.")

        elif choice == "3":
            account = get_account(accounts)

            if account:
                try:
                    amount = float(input("Enter amount: ₦"))
                    account.withdraw(amount)
                except ValueError:
                    print("❌ Invalid amount.")

        elif choice == "4":
            account = get_account(accounts)

            if account:
                print(
                    f"💰 Current Balance: "
                    f"₦{account.get_balance():,.2f}"
                )

        elif choice == "5":
            account = get_account(accounts)

            if account:
                account.display_info()

        elif choice == "6":
            print("\nThank you for using the Bank Account System! 👋")
            break

        else:
            print("❌ Invalid choice. Please select 1–6.")


if __name__ == "__main__":
    main()