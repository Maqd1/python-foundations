

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