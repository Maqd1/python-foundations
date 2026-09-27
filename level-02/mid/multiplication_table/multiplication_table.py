
while True:
    number = int(input("Enter the main number: "))
    the_end = int(input("Enter the number to stop at: "))

    for i in range(1,(the_end + 1)):
        print(f"{number} * {i} = {number * i}")

    cont_ques = input("Show another? (y/n): ")

    if cont_ques.lower() == "y":
        continue
    if cont_ques.lower() == "n":
        print("Goodbye!")
        break



