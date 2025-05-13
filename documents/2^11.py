# Script is limited to 4300 digits, it is only an example that caculates the powers of 2 that have only even digits

# Fucntion that checks if numer has only even digits
def only_even_digits(n):
    even_digits = ['0', '2', '4', '6', '8']
    return all(digit in even_digits for digit in str(n))

# Find the last power of 2 that has only even digits
max_exponent = 100  # Choose a value here
last_valid_power = None

for exponent in range(1, max_exponent + 1):
    power = 2 ** exponent
    if only_even_digits(power):
        last_valid_power = exponent
        print(f"2^{exponent} = {power} has only even digits.")
    
if last_valid_power is not None:
    print(f"The last power of 2 that contains only even digits is 2^{last_valid_power}.")
else:
    print("No power of 2 with only even digits found.")
