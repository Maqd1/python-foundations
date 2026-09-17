# Bank Account System

A simple interactive banking system built with Python and Object-Oriented Programming (OOP).

## Features

The system supports:

- Creating Savings Accounts
- Creating Checking Accounts
- Depositing money
- Withdrawing money
- Checking account balances
- Displaying account information
- Savings account interest calculation
- Savings account minimum balance protection
- Checking account overdraft support

## OOP Concepts

This project demonstrates:

- Classes
- Objects
- Attributes
- Methods
- Constructors
- Inheritance
- Encapsulation
- Method overriding
- `super()`
- Private attributes
- Polymorphic behavior
- Composition of program functionality through functions

## Class Structure

### BankAccount

The `BankAccount` class is the parent class.

It contains:

- `account_number`
- `owner`
- `__balance`

Methods:

- `deposit()`
- `withdraw()`
- `get_balance()`
- `display_info()`

The balance is stored using the private attribute `__balance` to demonstrate encapsulation.

### SavingsAccount

`SavingsAccount` inherits from `BankAccount`.

Additional attributes:

- `interest_rate`
- `minimum_balance`

Additional method:

- `calculate_interest()`

The `withdraw()` method is overridden so that the account cannot fall below its minimum balance.

### CheckingAccount

`CheckingAccount` also inherits from `BankAccount`.

Additional attribute:

- `overdraft_limit`

Its `withdraw()` method is overridden to allow the account to use an overdraft up to the specified limit.

## Account Numbers

New accounts receive automatically generated account numbers beginning at:

```text
1001