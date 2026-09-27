

password = input("Enter password: ")
isvalid = True

if len(password) < 8:
    print("Password is too short!")
    isvalid = False

if not any(char.isupper() for char in password):
    print("Missing uppercase!")
    isvalid = False

if not any(char.isdigit() for char in password):
    print("Missing digit!")
    isvalid = False

if isvalid:
    print("Password is valid! ✅")