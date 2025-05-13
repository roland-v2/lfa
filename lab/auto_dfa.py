'''
Input file must follow this model:
[states]
state_1 value
state_2 value 
(#! value refers to S for start_state, F for final_state or anything else for intermediary states; 
there can only be one start state, but if there are more than one state signaled with S, the last one will be considered the start state; 
there can be multiple final states;
if a start_state is also a final_state it will be set seperately, not on the same row)
...

[sigma]
letter_1
letter_2
...

[rules]
state_1 letter state_2 (#! first rule must have the start state on the first state position)
state_3 letter state_4
...
'''

# Function for loading the states, alphabet and rules in a dictionary, checks for commentaries or empty lines
def load_auto (name):
    auto = {}
    with open (name) as input:
        curr = None
        for line in input:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            if line.startswith('[') and line.endswith(']'):
                curr = line.strip('[]')
                auto[curr] = []
            elif curr == "sigma":
                if line.strip() not in auto[curr]:
                    auto[curr].append(line.strip())
            elif curr is not None:
                if line.split() not in auto[curr]:
                    auto[curr].append(line.split())
    return auto

# function for loading only one section of the input file, checks for commentaries or empty lines
def load_section (name, section):
    sect = {}
    with open (name) as input:
        curr = None
        for line in input:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            if line.startswith('[') and line.endswith(']'):
                curr = line.strip('[]')
                if curr == section:
                    sect[curr] = []
            elif curr == section == 'sigma':
                if line.strip() not in sect[curr]:
                    sect[curr].extend(line.strip())
            elif curr == section:
                if line.split() not in sect[curr]:
                    sect[curr].append(line.split())
    return sect

# function for checking if the loaded automaton is valid or not
def is_valid_auto (dc):
    ls = ['states', 'sigma', 'rules']
    for key in ls:
        if key not in dc.keys():
            return False
    return True

# function for checking if a rule is valid
def is_valid_rule(rule, dc):
    states = []
    for state in dc['states']:
        states.append(state[0])
    if len(rule) == 3 and rule[0] in states and rule[2] in states and rule[1] in dc["sigma"]:
        return True
    return False

# function for checking if all rules are valid
def all_valid_rules(dc):
    length = 0
    rules = dc['rules']
    for rule in rules:
        if is_valid_rule(rule,dc):
            length += 1
    if length == len(rules):
        return True
    return False

# function for checking if the first rule is valid(if it has the start state on the first state position)
def is_valid_firstrule(rule, start_state):
    if rule[0] == start_state:
        return True
    return False

# function for checking if input is valid
def is_valid_input(ls, dc):
    for value in ls:
        if value not in dc['sigma']:
            return False
    return True

# getter for section
def get_section(auto, section):
    return auto[section]

auto = load_auto("auto_dfa_input.txt")
states = auto['states']
sigma = auto['sigma']
rules = auto['rules']

# DFA function
def start_dfa():
    if is_valid_auto(auto) and all_valid_rules(auto):
        input_string = list(input().split())
        index = 0
        # check input
        if is_valid_input(input_string, auto):
            # load start and final states
            curr_state = None
            final_states = []
            for state in states:
                if state[1] == 'S':
                    curr_state = state[0]
                elif state[1] == 'F':
                    final_states.append(state[0])
            # check first rule
            if is_valid_firstrule(rules[0], curr_state):
                print(f"{curr_state}", end='')
                # iterate through values of input
                for value in input_string:
                    index += 1
                    # find coresponding rule for current state and value 
                    for rule in rules:
                        if rule[0] == curr_state and rule[1] == value:
                            curr_state = rule[2]
                            if index != len(input_string):
                                print(f" -> {curr_state}", end='')
                            # checking acceptance at end of input
                            else:
                                print(f" -> {curr_state}")
                                if curr_state in final_states:
                                    print('Input Accepted!')
                                else:
                                    print('Not in a final state...')
                            break
            else:
                print('Not valid first rule, check the input file and try again!')
        else:
            print('Invalid input!')
    else:
        print('Not valid automaton, check the input file and try again!')

start_dfa()