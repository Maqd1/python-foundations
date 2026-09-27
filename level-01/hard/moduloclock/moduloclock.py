
total_seconds = int(input("Enter a large number of seconds: "))

hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

hour_word = "hour" if hours < 2 else "hours"
minute_word = "minute" if minutes < 2 else "minutes"
second_word = "second" if seconds < 2 else "seconds"

print(f"{total_seconds} is, {hours} {hour_word}, {minutes} {minute_word}, and {seconds} {second_word}")