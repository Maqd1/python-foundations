'''

🎯 VERY CORE HARD OOP PROJECTS
1️⃣ 🏦 VERY HARD BANK SYSTEM
The Enterprise Banking System with Fraud Detection 💳

Build a complete banking system that handles multiple account types, transactions, loans, and fraud detection!

Package Structure:
text

bank_system/
    __init__.py
    accounts/
        __init__.py
        account.py
        savings.py
        checking.py
        investment.py
        loan.py
    customers/
        __init__.py
        customer.py
        business.py
        individual.py
    transactions/
        __init__.py
        transaction.py
        transfer.py
        payment.py
    services/
        __init__.py
        fraud_detector.py
        interest_calculator.py
        notification.py
    database/
        __init__.py
        repository.py
    exceptions/
        __init__.py
        bank_exceptions.py
    config/
        __init__.py
        settings.py
    tests/
        __init__.py
        test_accounts.py
    main.py
    cli.py
    setup.py

Data Structure:
python

# accounts/account.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Transaction:
    """Immutable transaction record"""
    transaction_id: str
    account_number: str
    amount: float
    type: str  # DEPOSIT, WITHDRAWAL, TRANSFER, FEE, INTEREST
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    balance_after: float = 0.0
    status: str = "PENDING"  # PENDING, COMPLETED, FAILED, REVERSED

@dataclass
class Account(ABC):
    """Abstract base account class"""
    account_number: str
    customer_id: str
    balance: float = 0.0
    currency: str = "NGN"
    status: str = "ACTIVE"  # ACTIVE, FROZEN, CLOSED
    created_at: datetime = field(default_factory=datetime.now)
    transactions: List[Transaction] = field(default_factory=list)
    
    @abstractmethod
    def get_account_type(self) -> str:
        pass
    
    @abstractmethod
    def calculate_interest(self) -> float:
        pass
    
    @abstractmethod
    def get_max_withdrawal(self) -> float:
        pass
    
    def deposit(self, amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self._create_transaction(amount, "DEPOSIT", description)
    
    def withdraw(self, amount: float, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.get_max_withdrawal():
            raise ValueError(f"Exceeds maximum withdrawal limit")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Available: {self.balance}")
        self.balance -= amount
        return self._create_transaction(-amount, "WITHDRAWAL", description)
    
    def _create_transaction(self, amount: float, type: str, description: str) -> Transaction:
        transaction = Transaction(
            transaction_id=f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
            account_number=self.account_number,
            amount=amount,
            type=type,
            description=description,
            balance_after=self.balance
        )
        self.transactions.append(transaction)
        return transaction

# accounts/savings.py
@dataclass
class SavingsAccount(Account):
    """Savings account with interest and minimum balance"""
    interest_rate: float = 0.025  # 2.5% per annum
    min_balance: float = 1000.0
    withdrawal_limit_per_day: float = 50000.0
    daily_withdrawn: float = 0.0
    
    def get_account_type(self) -> str:
        return "SAVINGS"
    
    def calculate_interest(self) -> float:
        # Monthly interest calculation
        return self.balance * (self.interest_rate / 12)
    
    def get_max_withdrawal(self) -> float:
        daily_remaining = self.withdrawal_limit_per_day - self.daily_withdrawn
        available = min(self.balance - self.min_balance, daily_remaining)
        return max(0, available)
    
    def withdraw(self, amount: float, description: str = "") -> Transaction:
        if self.balance - amount < self.min_balance:
            raise ValueError(f"Cannot go below minimum balance of {self.min_balance}")
        # Reset daily withdrawn if new day
        self.daily_withdrawn += amount
        return super().withdraw(amount, description)

Requirements:

    Account Types (Inheritance):

        SavingsAccount: Interest rate, min balance, daily withdrawal limit

        CheckingAccount: Overdraft protection, transaction fees

        InvestmentAccount: Stocks, bonds, mutual funds portfolio

        LoanAccount: Principal, interest rate, payment schedule

        BusinessAccount: Multiple signatories, transaction limits

    Customer Types (Polymorphism):

        IndividualCustomer: Personal info, KYC documents

        BusinessCustomer: Company registration, directors

        JointCustomer: Multiple account holders

    Transaction System (Encapsulation):

        Transaction: Immutable record with validation

        Transfer: Between accounts (same/different banks)

        Payment: Bills, utilities, merchants

        StandingOrder: Recurring payments

    Fraud Detection System (Strategy Pattern - HARD):

        Pattern detection: Unusual locations, large amounts

        Velocity checks: Multiple transactions in short time

        Suspicious activity scoring

        Automatic account freezing

        Alert generation

    Interest Calculator (Strategy Pattern):

        Different strategies for different account types

        Daily/ Monthly/ Annually compounding

        Tiered interest rates based on balance

    Notification System (Observer Pattern):

        Email notifications

        SMS alerts

        Push notifications

        Dashboard updates

    Loan Management (HARDEST):

        Loan amortization calculation

        Payment schedules

        Early payment penalties

        Refinancing options

Sample Output:
text

🏦 NIGERIA BANK SYSTEM v5.0 🏦

Customer: Damilola Ogunleye (Individual)
Customer ID: CUST001
KYC Status: VERIFIED
Accounts: 3

📋 ACCOUNT SUMMARY:
1. Savings Account (SAV001)
   Balance: ₦1,250,000.00
   Status: ACTIVE
   Interest Rate: 2.5%
   Min Balance: ₦1,000.00

2. Checking Account (CHK001)
   Balance: ₦500,000.00
   Status: ACTIVE
   Overdraft Limit: ₦200,000.00
   Available: ₦700,000.00

3. Investment Account (INV001)
   Balance: ₦5,000,000.00
   Status: ACTIVE
   Portfolio: 45% Stocks, 30% Bonds, 25% Mutual Funds
   Performance: +12.5% YTD

=====================================
🚨 FRAUD DETECTION ALERT! 🚨
Account: SAV001
Transaction: ₦2,500,000.00 WITHDRAWAL
Location: Paris, France
Risk Score: 85/100 (HIGH)

Security Question: What is your mother's maiden name?
Answer: Okafor
✅ Verified!

Transaction processed successfully.
=====================================

💸 TRANSFER REQUEST
From: SAV001 (Damilola)
To: CHK001 (Damilola)
Amount: ₦250,000.00

Daily transfer limit: ₦1,000,000.00
Remaining today: ₦750,000.00

Confirm? (y/n): y
✅ Transfer completed!

=====================================
📊 INTEREST EARNED (Last Month)
Savings (SAV001): ₦2,604.17
Investment (INV001): ₦15,625.00
Total Interest: ₦18,229.17

=====================================
💳 LOAN APPLICATION
Customer: Damilola Ogunleye
Amount: ₦10,000,000.00
Term: 5 years
Interest Rate: 15% APR

Monthly Payment: ₦237,860.00
Total Interest: ₦4,271,600.00
Total Payment: ₦14,271,600.00

Credit Score: 720 (GOOD)
Eligibility: APPROVED

Accept loan offer? (y/n): y
✅ Loan approved! Funds disbursed to SAV001

=====================================
📈 INVESTMENT PORTFOLIO
Account: INV001
Total Value: ₦5,625,000.00
ROI: +12.5%

Holdings:
1. GTBank (GTCO) - ₦2,250,000.00 (40%)
   Units: 5,000 shares @ ₦450.00
   
2. Dangote Cement (DANGCEM) - ₦1,687,500.00 (30%)
   Units: 3,750 shares @ ₦450.00
   
3. MTN Nigeria (MTNN) - ₦1,125,000.00 (20%)
   Units: 1,500 shares @ ₦750.00

Recommendations:
✅ Add: Zenith Bank (ZENITHBANK)
✅ Add: BUA Cement (BUACEMENT)

=====================================
🔔 NOTIFICATIONS (Today):
📧 Email: Interest credit of ₦2,604.17
📱 SMS: ₦250,000.00 transfer to CHK001
🔔 Push: Portfolio value increased by 1.2%

=====================================
📋 MONTHLY STATEMENT
Account: SAV001
Period: August 2026

Opening Balance: ₦1,200,000.00
Deposits: ₦350,000.00
Withdrawals: -₦300,000.00
Interest: +₦2,604.17
Closing Balance: ₦1,252,604.17

Transactions: 12
Average Balance: ₦1,226,302.08

=====================================
💰 TOTAL NET WORTH
Customer: Damilola Ogunleye
Total Assets: ₦6,877,604.17
Total Liabilities: ₦10,000,000.00 (Loan)
Net Worth: -₦3,122,395.83

Would you like to view detailed statements? (y/n):

Concepts Tested: Abstract classes, inheritance, polymorphism, encapsulation, strategy pattern, observer pattern, dataclasses, property decorators, magic methods, exception hierarchy, repository pattern, dependency injection'''