#Q5. The Truth Table Tester (Hard)
#Without using if statements, write a program that takes two boolean inputs from the user.

#· Note: input() gives a string. To get a boolean, check if the user types "True".
#· Calculate and print the results of:
#  1. A and B
#  2. A or B
#  3. not A
#  4. A == B
#· Print it neatly like:
 
#  A=True, B=False
#  A and B: False
#  A or B: True
#  not A: False
#  A == B: False
  
#· Goal: Deep dive into Boolean logic, bool() conversion logic, and comparison operators.

A_input = input("what is your input for the first? (True or False) ")
B_input = input("what is your input for the second? (True or False) ")

A = A_input == "True"
B = B_input == "True"

print(f"A={A}, B={B}")
print(f"A and B: {A and B}")
print(f"A or B: {A or B}")
print(f"not A: {not A}")
print(f"A == B: {A == B}")
