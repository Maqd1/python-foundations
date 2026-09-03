#Q2. The Rectangle Painter (Easy)
#Write a program that asks for the length and width of a rectangle (as floats)
#· Calculate the area and perimeter.
#· Print both results with 2 decimal places (Hint: f-strings allow formatting: {area:.2f}).
#· Goal: Practice float() conversion, arithmetic operators (*, +), and formatted output.

length = float(input("enter the length of a rectangle:"))
width = float(input("enter the width of a rectangle:"))

area = length * width
perimeter = 2 * (length + width)

print (f"area is {area:.3f} and perimeter is {perimeter:.2f}")