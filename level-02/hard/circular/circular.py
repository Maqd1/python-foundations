

def calculate_next(a, b, max_val):
    total = a + b
    
    # Using modulo to wrap, adjusted for a 1-based range
    next_num = ((total - 1) % max_val) + 1
    
    return next_num

def generate_sequence(length, max_val):

    sequence = [1, 1]
    
    while len(sequence) < length:
        a = sequence[-2]
        b = sequence[-1]
        
        next_num = calculate_next(a, b, max_val)
        
        sequence.append(next_num)
        
    return sequence[:length]

def display_sequence(sequence, max_val):

    length = len(sequence)
    
    print(f"Sequence length: {length}")
    print(f"Max value: {max_val}")
    print(sequence)

target_length = 5
maximum_value = 20

final_sequence = generate_sequence(target_length, maximum_value)

display_sequence(final_sequence, maximum_value)