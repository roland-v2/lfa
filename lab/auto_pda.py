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
state_1 input_value pop_value push_value state_2 (#! first rule must have the start state on the first state position)
state_3 input_value pop_value push_value state_4
...
'''

# function for loading automaton, checks for commentaries or empty lines
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

# function for loading only one section, checks for commentaries or empty lines
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
    if len(rule) == 5 and rule[0] in states and rule[4] in states and rule[1] in dc['sigma'] and rule[2] in dc['sigma'] and rule[3] in dc['sigma']:
        return True
    return False

# function for checking all valid rules
def all_valid_rules(dc):
    length = 0
    rules = dc['rules']
    for rule in rules:
        if is_valid_rule(rule, dc):
            length += 1
    if length == len(rules):
        return True
    return False

# function for checking valid first rule, must have the start_state on the first state position
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

auto = load_auto("auto_pda_input2.txt")
states = auto['states']
sigma = auto['sigma']
rules = auto['rules']

# PDA function
def start_pda():
    # check valid automaton and rules
    if is_valid_auto(auto) and all_valid_rules(auto):
        input_string = list(input().split())
        stack = []
        ok = 0
        # check valid input
        if is_valid_input(input_string, auto):
            curr_state = None
            final_states = []
            # searching for start and final states
            for state in auto['states']:
                if state[1] == 'S':
                    curr_state = state[0]
                elif state[1] == 'F':
                    final_states.append(state[0])
            # check valid first_rule
            if is_valid_firstrule(auto['rules'][0], curr_state):
                print(f'{curr_state} ->', end = ' ')
                # iterating through input
                for value in input_string:
                    # 3 checks to make sure no input value is skipped 
                    # checking epsilon state
                    ok = 0
                    for rule in rules:
                        if curr_state == rule[0] and rule[1] == 'e':
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                    # checking for input value
                    for rule in rules:
                        if curr_state == rule[0] and rule[1] == value:
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                    # checking epsilon value again, in case the new curr_state has epsilon transition
                    for rule in rules:
                        if curr_state == rule[0] and rule[1] == 'e':
                            if stack and stack[-1] == rule[2]:
                                stack.pop()
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                            elif 'e' == rule[2]:
                                if rule[3] != 'e':
                                    stack.append(rule[3])
                                curr_state = rule[4]
                                print(f'{curr_state} ->', end = " ")
                                print(stack)
                                ok = 1
                                break
                    # if input is not accepted, according message is displayed
                    # if input in accepted, no message is displayed and stack is empty
                    if ok == 0:
                        print('!!! Not accepted !!!')
                        break
                if stack != []:
                    print('!!! Not accepted !!!')
                print(f'Stack: {stack}')        
            else:
                print('Nu e automat valid, verificati fisierul de input si incercati din nou!')
        else:
            print('Input invalid!')
    else:
        print('Nu e automat valid, verificati fisierul de input si incercati din nou!')

start_pda()