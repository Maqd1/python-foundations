#Easy Level (2 Questions)
#Q1: The Password Validator (Easy)

#Write a program that:

#    Asks the user for a password

#    Checks if the password:

#        Is at least 8 characters long

#        Contains at least one uppercase letter

#        Contains at least one digit

#    Prints:

#        "Password is valid! ✅" (if all conditions met)

#        "Password is too short!" (if too short)

#        "Missing uppercase letter!" (if no uppercase)

#        "Missing digit!" (if no digit)

#        Multiple messages if multiple issues found

#Concepts: if/elif/else, string methods, comparison operators

#Sample Output:
#text

#Enter password: abc
#Password is too short!
#Missing uppercase!
#Missing digit!

#Enter password: Password123
#Password is valid! ✅
password = input("Enter user password: ")

isvalid = True

if len(password) < 8:
    print("password is too short")
    isvalid = False

upper = False
for char in password:
    if char.isupper():
        upper = True
        break
if not upper:
        print("Missing uppercase letter!")
        isvalid = False

digit = False
for char in password:
    if char.isdigit():
        digit = True
        break

if not digit:
        print("Missing digit!")
        isvalid = False

if isvalid:
    print("Password is valid! ✅")