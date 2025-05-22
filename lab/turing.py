'''
Input file must follow this model:
[states]
state_1 value
state_2 value 
(#! value refers to S for start_state, F for final_state or anything else for intermediary states; 
there can only be one start state, but if there are more than one state signaled with S, the last one will be considered the start state; 
there can only be one final state, but if there are more than one state signaled with F, the last one will be considered the start state;
if a start_state is also a final_state it will be set seperately, not on the same row)
...

[sigma]
letter_1
letter_2
...

[rules]
state_1 letter state_2 letter direction (#! first rule must have the start state on the first state position)
state_3 letter state_4 letter direction (#! direction MUST be R or L)
...
'''

# function for loading automaton into dictionary, checks for commentaries or empty lines
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

# function for loading section, checks for commentaries or empty lines
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

# function for checking valid automaton
def is_valid_auto (dc):
    ls = ['states', 'sigma', 'rules']
    for key in ls:
        if key not in dc.keys():
            return False
    return True

# function for checking valid rule
def is_valid_rule(rule, dc):
    states = []
    for state in dc['states']:
        states.append(state[0])
    if len(rule) == 5 and rule[0] in states and rule[2] in states and rule[1] in dc["sigma"] and rule[3] in dc["sigma"] and (rule[4] == "R" or rule[4] == "L"):
        return True
    return False

# function for checking valid rules
def all_valid_rules(dc):
    length = 0
    rules = dc['rules']
    for rule in rules:
        if is_valid_rule(rule,dc):
            length += 1
    if length == len(rules):
        return True
    return False

# function for checking valid first rule - must contain the start state on the first state position
def is_valid_firstrule(rule, start_state):
    if rule[0] == start_state:
        return True
    return False

# function for checking valid input
def is_valid_input(ls, dc):
    for value in ls:
        if value not in dc['sigma']:
            return False
    return True

# getter for section
def get_section(auto, section):
    return auto[section]

auto = load_auto("lfa/lab/turing_input_AI_Gemini3.txt")
states = auto['states']
sigma = auto['sigma']
rules = auto['rules']

# Turing function
def start_turing():
    # checking valid automaton and rules
    if is_valid_auto(auto) and all_valid_rules(auto):
        input_string = list(input().split())
        index = 0
        bandwidth = input_string
        # used a finite number for the length of bandwidth - in this case, len(input) + 100
        # we consider space as '_'
        bandwidth.extend(['_']*100)
        # checking valid input
        if is_valid_input(input_string, auto):
            curr_state = None
            final_state = None
            # searching for start and final state
            for state in states:
                if state[1] == 'S':
                    curr_state = state[0]
                elif state[1] == 'F':
                    final_state = state[0]
            # checking valid first rule 
            if is_valid_firstrule(rules[0], curr_state):
                while curr_state != final_state:
                    # checking secondary condition for stopping
                    if index < 0 or index >= len(bandwidth):
                        print("Moved out of bounds.")
                        break
                    # searching for coresponding rule
                    for rule in rules:
                        if rule[0] == curr_state and rule[1] == bandwidth[index]:
                            curr_state = rule[2]
                            bandwidth[index] = rule[3]
                            # checking direction
                            if rule[4] == "R":
                                index += 1
                            else:
                                index -= 1 
            else:
                print('Not valid first rule, check the input file and try again!')
        else:
            print('Invalid input!')
        # printing bandwidth without empty spaces "_"
        print(bandwidth)
    else:
        print('Not valid automaton, check the input file and try again!')

start_turing()