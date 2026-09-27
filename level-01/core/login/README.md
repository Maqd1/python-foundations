# 🔐 HARD SIMPLE LOGIN - The Brute-Force Protector

## Difficulty

Core

## Task

Write a login system that has pre-registered users stored in a dictionary:

```python
users = {
    "admin": "password123",
    "damilola": "python2025",
    "guest": "welcome"
}
```

Ask the user for:

* Username
* Password

### Login

If both the username and password match, print:

```text
Welcome [username]!
```

If the login fails, provide a specific error:

```text
Username not found
```

or:

```text
Incorrect password
```

### Account Lockout

Implement a lockout system.

The program must:

* Track failed login attempts for each username.
* Allow a maximum of 3 failed attempts.
* Lock the account after the third failed attempt.
* Store locked accounts separately using a set or list.
* Print:

```text
Account locked! Contact admin.
```

when an account is locked.

A locked account must remain unable to log in, even if the correct password is subsequently entered.

### Password Strength Checker

Add a registration option.

Ask:

```text
Would you like to register? (y/n)
```

If the user chooses `y`, ask for:

* New username
* New password

The new password must:

* Contain at least 8 characters
* Contain at least 1 uppercase letter
* Contain at least 1 digit
* Contain at least 1 special character from:

```text
!@#$%^&*
```

Give specific feedback when a requirement is missing, such as:

```text
Password too short
```

or:

```text
Add uppercase
```

Only add the new user to the users dictionary if the password satisfies all requirements.

## Example Flow

```text
Username: admin
Password: wrong
❌ Incorrect password! (Attempt 1/3)

Username: admin
Password: wrong
❌ Incorrect password! (Attempt 2/3)

Username: admin
Password: wrong
⚠️ Account locked! Contact admin.

Username: guest
Password: welcome
✅ Welcome guest!

Would you like to register? (y/n): y
New username: dave
New password: 123
❌ Password too short (min 8 chars)

Try again: Dave2025!
✅ Account created! Welcome dave!
```

## Goal

Build a login system that combines user authentication, failed-attempt tracking, account lockout, password validation, and registration.

## Concepts Tested

* Dictionaries
* Lists/Sets
* Nested `if` statements
* String methods
* `.isupper()`
* `.isdigit()`
* `.isalnum()`
* Loops (`while`)
* Boolean flags
* Input validation
* String processing
* Conditional logic
