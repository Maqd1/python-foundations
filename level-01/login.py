'''
5

🔐 HARD SIMPLE LOGIN

The Brute-Force Protector 🛡️

Write a login system that:

1. Has pre-registered users (store in a dictionary):
  
   users = {
       "admin": "password123",
       "damilola": "python2025",
       "guest": "welcome"
   }
   
2. Ask for username and password
3. If both match, print: "Welcome [username]!"
4. If wrong, give specific errors:
   · "Username not found"
   · "Incorrect password"
5. 🚨 HARD PART: Implement a lockout system:
   · Track failed attempts per username
   · After 3 failed attempts for a username, lock that account
   · Message: "Account locked! Contact admin."
   · Locked accounts cannot log in even with correct password (store in a separate set/list)
6. Add password strength checker for new users:
   · Ask if they want to register (y/n)
   · If 'y', check password:
     · Must be at least 8 characters
     · Must contain at least 1 uppercase letter
     · Must contain at least 1 digit
     · Must contain at least 1 special character (!@#$%^&*)
   · Give specific feedback: "Password too short", "Add uppercase", etc.
7. Only add user if password meets all criteria

Concepts Tested:

· Dictionaries (for user storage)
· Lists/Sets (for locked users)
· Nested if statements
· String methods (.isupper(), .isdigit(), .isalnum())
· Loops (while for login retry)
· Boolean flags (for tracking lockout)
· Input validation

Example Flow:

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
'''

users = {
    "admin": "password123",
    "damilola": "python2025",
    "guest": "welcome"
}

failed_attempts = {}
locked_accounts = set()


def check_password_strength(password):
    if len(password) < 8:
        return "Password too short (min 8 chars)"

    has_upper = False
    has_digit = False
    has_special = False
    special_chars = "!@#$%^&*"

    for char in password:
        if char.isupper():
            has_upper = True
        if char.isdigit():
            has_digit = True
        if char in special_chars:
            has_special = True

    if not has_upper:
        return "Add an uppercase letter"
    if not has_digit:
        return "Add a digit"
    if not has_special:
        return "Add a special character (!@#$%^&*)"

    return "OK"

def register():
    new_username = input("New username: ")
    while True:
        new_password = input("New password: ")
        result = check_password_strength(new_password)
        if result == "OK":
            users[new_username] = new_password
            print(f"✅ Account created! Welcome {new_username}!")
            break
        else:
            print(f"❌ {result}")

def login():
    username = input("Username: ")

    if username in locked_accounts:
        print("⚠️ Account locked! Contact admin.")
        return

    if username not in users:
        print("❌ Username not found")
        return

    password = input("Password: ")

    if password == users[username]:
        print(f"✅ Welcome {username}!")
        failed_attempts[username] = 0  # reset on success
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        attempts = failed_attempts[username]

        if attempts >= 3:
            locked_accounts.add(username)
            print("⚠️ Account locked! Contact admin.")
        else:
            print(f"❌ Incorrect password! (Attempt {attempts}/3)")

while True:
    login()
    again = input("\nTry again? (y/n): ").lower()
    if again != "y":
        break

register_choice = input("Would you like to register? (y/n): ").lower()
if register_choice == "y":
    register()