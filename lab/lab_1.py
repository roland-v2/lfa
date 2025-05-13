def save_matrix (m, fn):
    with open (fn, "w") as output:
        for line in m:
            if not line or line[0] == "#":
                continue
            else:
                output.write(f'{" ".join(map(str,line))}\n')

def load_matrix (fn):
    with open (fn) as input:
        for line in input:
            line = line.split()
            if not line or line[0] == "#":
                continue
            m.append(line)

def is_matrix (m):
    x = len(m[0])
    for line in m:
        if len(line) != x:
            return False
        x = len(line)
    return True

m = [['2', '2', '2'], ['4', '4', '4'], ['#', 'c'], [], ['6', '6', '6']]
save_matrix(m, "save_matrix.txt")

m = []
load_matrix("load_matrix.txt")
print(m)

print (is_matrix(m))