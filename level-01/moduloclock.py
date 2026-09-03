#Q6. The Modulo Clock (Hard)
#You have total_seconds = 3723. Write a program that converts this into Hours, Minutes, Seconds.

#· Formula:
#  · hours = total_seconds // 3600
#  · minutes = (total_seconds % 3600) // 60
#  · seconds = total_seconds % 60
#· Now make it interactive: Ask the user to input a large number of seconds, calculate the split, and print: "3723 seconds is 1 hour, 2 minutes, and 3 seconds."
#· Goal: Master the powerful // (floor) and % (modulo) operators—they are heavily used in real-world coding!

total_seconds = int(input("Enter a large number of seconds: "))

hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

hour_word = "hour" if hours < 2 else "hours"
minute_word = "minute" if minutes < 2 else "minutes"
second_word = "second" if seconds < 2 else "seconds"

print(f"{total_seconds} is, {hours} {hour_word}, {minutes} {minute_word}, and {seconds} {second_word}")