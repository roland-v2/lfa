class TuringMachine:
    def __init__(self, filename):
        self.states = {}
        self.start_state = None
        self.final_states = set()
        self.sigma = set()
        self.rules = {}
        self.blank = '_'  # Assume '_' is the blank symbol

        self.load_machine(filename)

    def load_machine(self, filename):
        section = None
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # skip empty lines and comments
                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1].lower()
                    continue

                if section == 'states':
                    parts = line.split()
                    state = parts[0]
                    label = parts[1] if len(parts) > 1 else '0'
                    self.states[state] = label
                    if label == 'S':
                        self.start_state = state
                    if label == 'F':
                        self.final_states.add(state)

                elif section == 'sigma':
                    self.sigma.add(line)

                elif section == 'rules':
                    # format: current_state read_symbol next_state write_symbol direction
                    parts = line.split()
                    key = (parts[0], parts[1])
                    value = (parts[2], parts[3], parts[4])
                    self.rules[key] = value

    def initialize_tape(self, input_string):
        # Represent tape as a dictionary {position: symbol}
        self.tape = {}
        for i, symbol in enumerate(input_string):
            self.tape[i] = symbol
        self.head = 0
        self.current_state = self.start_state

    def step(self):
        symbol = self.tape.get(self.head, self.blank)
        key = (self.current_state, symbol)

        if key not in self.rules:
            return False  # No applicable rule, machine halts

        next_state, write_symbol, direction = self.rules[key]

        # Write symbol
        self.tape[self.head] = write_symbol

        # Move head
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
        else:
            raise ValueError(f"Invalid direction: {direction}")

        # Update state
        self.current_state = next_state

        return True

    def run(self, max_steps=10000):
        steps = 0
        while self.current_state not in self.final_states:
            if not self.step():
                print("Machine halted (no applicable rule).")
                return
            steps += 1
            if steps > max_steps:
                print("Exceeded maximum number of steps.")
                return
        print("Machine finished in a final state.")

    def get_tape_string(self):
        if not self.tape:
            return ''
        min_index = min(self.tape.keys())
        max_index = max(self.tape.keys())
        return ''.join(self.tape.get(i, self.blank) for i in range(min_index, max_index + 1))

    def print_tape(self):
        tape_str = self.get_tape_string()
        head_pos = self.head - min(self.tape.keys())
        print(tape_str)
        print(' ' * head_pos + '^')

# Example usage
if __name__ == "__main__":
    tm = TuringMachine('turing_input.txt')  # your input file here
    tm.initialize_tape('110+11_')  # or whatever your initial tape is
    tm.print_tape()

    tm.run()

    tm.print_tape()