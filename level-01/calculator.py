#🧮 HARD CALCULATOR

#The Memory Calculator 🧠

#Create a calculator that:

#1. Asks the user for two numbers
#2. Asks for an operator (+, -, *, /, //, %, **)
#3. Performs the calculation
#4. Stores the result in a "memory"
#5. Asks: "Continue with this result? (y/n)"
#6. If 'y', use the result as the first number for the next operation
#7. If 'n', start fresh with new numbers
#8. Type 'quit' at any time to exit

#Example Flow:

#Enter first number: 10
#Enter operator: +
#Enter second number: 5
#Result: 15
#Continue with 15? (y/n): y
#Enter operator: *
#Enter second number: 2
#Result: 30
#Continue with 30? (y/n): n
#Enter first number: 100
#Enter operator: /
#Enter second number: 4
#Result: 25.0
#Concepts Tested:

#· Variables & reassignment
#· Type conversion (float())
#· Comparison operators
#· Logical operators (checking 'y' or 'n')
#· While loops (implicitly - you'll need to keep running)
#· String formatting
#· input() handling edge cases



def calculate(first, operator, second):
    if operator == "+":
        return first + second
    elif operator == "-":
        return first - second
    elif operator == "*":
        return first * second
    elif operator == "/":
        return first / second
    elif operator == "//":
        return first // second
    elif operator == "%":
        return first % second
    elif operator == "**":
        return first ** second
    else:
        return None


# ------------------------
# OUTER LOOP
# ------------------------
while True:

    first_input = input("Enter first number (or 'quit'): ")
    if first_input.lower() == "quit":
        print("Goodbye!")
        break
    first = float(first_input)

    operator = input("Enter operator (+, -, *, /, //, %, **): ")
    if operator.lower() == "quit":
        print("Goodbye!")
        break
    
    second_input = input("Enter second number: ")
    if second_input.lower() == "quit":
        print("Goodbye!")
        break
    second = float(second_input)

    result = calculate(first, operator, second)

    if result is None:
        print("Invalid operator.")
        continue

    print(f"Result: {result}")

    # ------------------------
    # INNER LOOP (Memory)
    # ------------------------
    while True:

        choice = input(f"Continue with {result}? (y/n): ").lower()

        if choice == "quit":
            print("Goodbye!")
            exit()

        elif choice == "n":
            break

        elif choice == "y":

            operator = input("Enter operator: ")

            if operator.lower() == "quit":
                exit()

            second_input = input("Enter second number: ")

            if second_input.lower() == "quit":
                exit()

            second = float(second_input)

            result = calculate(result, operator, second)

            if result is None:
                print("Invalid operator.")
                continue

            print(f"Result: {result}")

        else:
            print("Please enter y or n.")  


# ------------------------
# OUTER LOOP
# ------------------------
#while True:
    #first_input = input("Enter first number (or 'quit'): ")
    #if first_input.lower() == "quit":
        #print("Goodbye!")
        #break
    #first = float(first_input)

    #operator = input("Enter operator (+, -, *, /, //, %, **): ")
    #if operator.lower() == "quit":
        #print("Goodbye!")
        #break

    #second_input = input("Enter second number: ")
    #if second_input.lower() == "quit":
        #print("Goodbye!")
        #break
    #second = float(second_input)

    #if operator == "+":
        #result = first + second
    #elif operator == "-":
        #result = first - second
    #elif operator == "*":
        #result = first * second
    #elif operator == "/":
        #result = first / second
    #elif operator == "//":
        #result = first // second
    #elif operator == "%":
        #result = first % second
    #elif operator == "**":
        #result = first ** second
    #else:
        #print("Invalid operator.")
        #continue

    #print(f"Result: {result}")

    # ------------------------
    # INNER LOOP (Memory)
    # ------------------------
    #while True:
        #choice = input(f"Continue with {result}? (y/n): ").lower()
        #if choice == "quit":
            #print("Goodbye!")
            #exit()
        #elif choice == "n":
            #break
        #elif choice == "y":
            #operator = input("Enter operator: ")
            #if operator.lower() == "quit":
                #exit()
            #second_input = input("Enter second number: ")
            #if second_input.lower() == "quit":
                #exit()
            #second = float(second_input)

            #if operator == "+":
                #result = result + second
            #elif operator == "-":
                #result = result - second
            #elif operator == "*":
                #result = result * second
            #elif operator == "/":
                #result = result / second
            #elif operator == "//":
                #result = result // second
            #elif operator == "%":
                #result = result % second
            #elif operator == "**":
                #result = result ** second
            #else:
                #print("Invalid operator.")
                #continue

            #print(f"Result: {result}")
        #else:
            #print("Please enter y or n.")