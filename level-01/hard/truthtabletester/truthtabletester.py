

A_input = input("what is your input for the first? (True or False) ")
B_input = input("what is your input for the second? (True or False) ")

A = A_input == "True"
B = B_input == "True"

print(f"A={A}, B={B}")
print(f"A and B: {A and B}")
print(f"A or B: {A or B}")
print(f"not A: {not A}")
print(f"A == B: {A == B}")
