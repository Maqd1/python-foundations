#The Number Classifier (Easy)

#Write a program that:

#    Takes an integer input from the user

#    Prints ONE of these categories:

#        "Positive even number" (if > 0 and even)

#        "Positive odd number" (if > 0 and odd)

#        "Negative even number" (if < 0 and even)

#        "Negative odd number" (if < 0 and odd)

#        "Zero is neither positive nor negative" (if exactly 0)

#Concepts: if/elif/else, modulo operator, comparison

value = int(input("Enter a number: "))

if value > 0 and value % 2 == 0:
    print("Positive even number")
elif value > 0 and value % 2 != 0:
    print("Positive odd number")
elif value < 0 and value % 2 == 0:
    print("Negative even number")
elif value < 0 and value % 2 != 0:
    print("Negative odd number")
else:
    print("Zero is neither positive nor negative")

