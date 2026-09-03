#The Multiplication Table Generator (Mid)

#Write a program that:

#    Asks: "Enter a number: "

#    Prints the multiplication table for 1-12

#    Asks: "Show another? (y/n): "

#    If 'y', repeat

#    If 'n', print "Goodbye!"

#    Extra challenge: Also ask for the range (e.g., print 1-20, or 5-15)

#    Harder: Format it in a nice grid using f-strings

#Sample Output:
#text

#Enter a number: 7
#7 x 1 = 7
#7 x 2 = 14
...
#7 x 12 = 84

#Show another? (y/n): y
#Enter a number: 3
#3 x 1 = 3
...
#3 x 12 = 36

#Show another? (y/n): n
#Goodbye!

#Concepts: for loop, while loop, range(), conditional logic
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



