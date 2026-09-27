# Password Validator

## Easy Level — Question 1

Write a program that asks the user for a password and checks whether it meets the required conditions.

### Requirements

The password must:

* Be at least **8 characters long**
* Contain at least **one uppercase letter**
* Contain at least **one digit**

### Output

If all conditions are satisfied:

```text
Password is valid! ✅
```

If one or more conditions are not satisfied, display a message for **each issue found**:

```text
Password is too short!
Missing uppercase letter!
Missing digit!
```

Multiple messages should be displayed when multiple requirements are missing.

### Concepts

* `if / elif / else`
* String methods
* Comparison operators

### Sample Output

**Invalid password:**

```text
Enter password: abc
Password is too short!
Missing uppercase!
Missing digit!
```

**Valid password:**

```text
Enter password: Password123
Password is valid! ✅
```
