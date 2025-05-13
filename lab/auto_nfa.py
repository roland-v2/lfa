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

# function for loading only one section of the automaton, checks for commentaries or empty lines
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

# function for checking if the atuomaton is valid
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

# function for checking if the first rule is valid, must contain the start state as the first state of the rule
def is_valid_firstrule(rule, start_state):
    if rule[0] == start_state:
        return True
    return False

# function for checking if input in valid
def is_valid_input(ls, dc):
    for value in ls:
        if value not in dc['sigma']:
            return False
    return True

# getter for a section
def get_section(auto, section):
    return auto[section]

auto = load_auto("auto_nfa_input.txt")
states = auto['states']
sigma = auto['sigma']
rules = auto['rules']

# function for checking epsilon rule
def epsilon_state(state):
    for line in rules:
        if line[0] == state and line[1] == 'epsilon':
            return line[2]
    return None

# NFA function
def start_nfa():
    # checking if the automaton and rules are valid
    if is_valid_auto(auto) and all_valid_rules(auto):
        input_string = list(input().split())
        index = 0
        # checking valid input
        if is_valid_input(input_string, auto):
            # used list for current states(curr_states1) and a copy of those(curr_states2)
            curr_states1 = []
            curr_states2 = []
            final_states = []
            #checking the start and final states
            for state in states:
                if state[1] == 'S':
                    curr_states1.append(state[0])
                elif state[1] == 'F':
                    final_states.append(state[0])
            # checking if the first rule is valid
            if is_valid_firstrule(rules[0], curr_states1[0]):
                # checking if the start state has an epsilon trasition
                if epsilon_state(curr_states1[0]) != None:
                    curr_states1.append(epsilon_state(curr_states1[0]))
                print(curr_states1)
                # iterating through input
                for value in input_string:
                    index += 1
                    # finding the next state for every curr_state
                    for curr_state in curr_states1:
                        #finding the rule coresdonding with curr_state and input value
                        for rule in rules:
                            if rule[0] == curr_state and rule[1] == value:
                                curr_states2.append(rule[2])
                                #checking if the next curr_state has an epsilon state
                                if epsilon_state(rule[2]) != None:
                                    curr_states2.append(epsilon_state(rule[2]))
                    curr_states1 = curr_states2
                    curr_states2 = []
                    print(curr_states1)
                # checking apcentance of input
                for state in curr_states1:
                    if state in final_states:
                        print('Input accepted!')
                        break
            else:
                print('Not valid first rule, check the input file and try again!')
        else:
            print('Invalid input!')
    else:
        print('Not valid automaton, check the input file and try again!')

start_nfa()