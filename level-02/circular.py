'''
Q6: The Circular Number Sequence (Hard)

Write a program that generates a "circular" number sequence.

Rule: Starting from 1, each number is the sum of the previous two numbers, but limited to a range, and wraps around.

For a max value of 20:

1, 1, 2, 3, 5, 8, 13, 1, 14, 15, 9, 4, 13, 17, 10, 7, 17, ...
The Logic:

1. Start with a = 1, b = 1
2. Print current number
3. Next number = a + b
4. If next > 20, subtract 20 repeatedly until it's in range
5. Continue this process for 20 iterations

Functions needed:

· calculate_next(a, b, max_val) → returns the next number (must be ≤ max_val)
· generate_sequence(length, max_val) → returns a list of numbers
· display_sequence(sequence) → prints neatly

Concepts: while loop, functions, parameters, return values, modulo for wrapping

Sample Output (for max=20, length=10):

Sequence length: 10
Max value: 20
[1, 1, 2, 3, 5, 8, 13, 1, 14, 15]
Harder variation: Print it as a grid:

1  1  2  3  5
8  13 1  14 15
9  4  13 17 10
Concepts: Nested loops, for, functions, list manipulation

---
'''


def calculate_next(a, b, max_val):
    total = a + b
    
    # Using modulo to wrap, adjusted for a 1-based range
    next_num = ((total - 1) % max_val) + 1
    
    return next_num

def generate_sequence(length, max_val):
    # 1. Start with the initial sequence setup
    sequence = [1, 1]
    
    # 2. Use a while loop as requested by the prompt
    while len(sequence) < length:
        # 3. Grab the last two numbers to act as 'a' and 'b'
        a = sequence[-2]
        b = sequence[-1]
        
        # 4. Delegate the math to your worker function
        next_num = calculate_next(a, b, max_val)
        
        # 5. Add the newly calculated number to the list
        sequence.append(next_num)
        
    # 6. Return the finished list (trimming just in case length was 1)
    return sequence[:length]

def display_sequence(sequence, max_val):
    # Calculate the length of the list dynamically
    length = len(sequence)
    
    # Use f-strings (putting an 'f' before the quotes) to insert variables directly
    print(f"Sequence length: {length}")
    print(f"Max value: {max_val}")
    print(sequence)

# 1. Set the variables defined in your sample output
target_length = 5
maximum_value = 20

# 2. Ask the Manager to build the list
final_sequence = generate_sequence(target_length, maximum_value)

# 3. Hand the finished list to the Presenter to print
display_sequence(final_sequence, maximum_value)