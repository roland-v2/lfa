# Function that checks for the pressence of "0" up to 2^limit
def check_powers_of_two(limit):
    for n in range(1, limit + 1):
        power = str(2 ** n)
        if '0' in power:
            print(f"2^{n} contains a 0: {power}")
        else:
            print(f"2^{n} does not contain a 0: {power}")

# Check pressence of "0" for given limit
check_powers_of_two(100)
