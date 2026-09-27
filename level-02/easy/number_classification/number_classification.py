

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

