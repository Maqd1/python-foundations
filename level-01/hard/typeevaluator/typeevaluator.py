
value = input("Enter a single value: ")

is_number = value.isdigit()
is_boolean = bool(value)
length = len(value)

print(f"Is it a number (int)? {is_number}")
print(f"Boolean value: {is_boolean}")
print(f"Length of string: {length}")