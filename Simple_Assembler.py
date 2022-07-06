import sys


def binary(number):
    if len(bin(number)[2::]) > 8:
        return 'f'
    else:
        return "0"*(8-len(bin(number)[2::]))+bin(number)[2::]


def A(string):
    if (string[1] not in registers) or (string[2] not in registers) or (string[3] not in registers):
        return(" Register number out of range")
    if 'FLAGS' in string:
        return(" Illegal use of flags")
    else:
        return opcode[string[0]]+"00"+registers[string[1]]+registers[string[2]]+registers[string[3]]


def B(string):
    if string[1] not in registers:
        return(" Register number out of range")
    if ('FLAGS' in string):
        return(" Illegal use of flags ")
    if ('.' in string[2][1::]):
        return(" Number out of range")
    if binary(int(string[2][1::])) == 'f':
        return(" Number out of range")
    else:
        return opcode[string[0]] + registers[string[1]] + binary(int(string[2][1::]))


def C(string):
    if (string[1] not in registers) or (string[2] not in registers):
        return(" Register number out of range")
    elif ("FLAGS" in string and 'cmp' in string):
        return(" Illegal use of flags")
    a = opcode[string[0]]
    if string[0] == "mov":
        a = '10011'
    return a+"0"*5+registers[string[1]]+registers[string[2]]


def D(string):
    if string[2] not in variables:
        return(" Unknown variable ")
    else:
        if string[2] in variables:
            return opcode[string[0]]+registers[string[1]]+variables[string[2]]
        return opcode[string[0]]+registers[string[1]]+string[2]


def E(string):
    if string[1] not in labels:
        return(" Unknown label")
    else:
        if string[1] in labels:
            return opcode[string[0]]+"0"*3 + str(binary(labels[string[1]]))
        return opcode[string[0]]+"0"*3 + string[1]


def F(string):
    return opcode[string]+"0"*11


def instructionToBin(string):
    newstring = string.split()
    if ":" in string:
        a = string.split(":")
        string = a[1].lstrip().rstrip()
        return instructionToBin(string)
    if "$" in string and newstring[0] in ['mov', 'rs', 'ls']:
        return B(string.split())
    elif "hlt" in string:
        return F(string)
    d = {1: E, 2: D, 3: A}
    string = string.split()
    if string[0] in ['mov', 'div', 'not', 'cmp'] and '$' not in ' '.join(string):
        return C(string)
    if string[0] in ['add', 'sub', 'mul', 'xor', 'or', 'and']:
        return A(string)
    if string[0] in ['ld', 'st']:
        return D(string)
    if string[0] in ['jmp', 'jlt', 'jgt', 'je']:
        return E(string)
    elif string[0] not in opcode:
        return (" unknown instruction!")


opcode = {"add": "10000", "sub": "10001", "mov": "10010", "ld": "10100", "st": "10101", "mul": "10110", "div": "10111",
          "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011", "and": "11100", "not": "11101", "cmp": "11110",
          "jmp": "11111", "jlt": "01100", "jgt": "01101", "je": "01111", "hlt": "01010"}
registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011",
             "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
lines = sys.stdin.readlines()
initial_lines = lines[::]
while '\n' in lines:
    lines.remove('\n')
variables = {}
final_ans = []
var = []
labels = {}
actual_length = len(lines)
newcount = 0
lines = [line.rstrip("\n").lstrip().rstrip() for line in lines]
hlt_count = lines[-1].count('hlt')
for line in lines:
    try:
        if "var" in line:
            var.append(line.split()[1])
            actual_length -= 1
            newcount -= 1
        elif ":" in line:
            labels[line.split(":")[0]] = newcount
        newcount += 1
    except:
        pass
for i in var:
    variables[i] = binary(actual_length)
    actual_length += 1
if (hlt_count != 1):
    b = 'line : '+str(len(initial_lines))+' hlt instruction missing at last'
    final_ans.append(b)
else:
    for i in range(len(lines)):
        if 'var' in lines[i].split():
            continue
        if 'hlt' in lines[i] and i != (len(lines)-1):
            a = 'line : ' + str(len(variables)+i+1) + \
                " misuse of hlt statement\n"
            final_ans.append(a)
        try:
            a = instructionToBin(lines[i])
            if a.isdigit() == False:
                for j in range(len(initial_lines)):
                    if lines[i] in initial_lines[j]:
                        break
                a = 'Line : ' + str(j+1) + a + '\n'
                final_ans.append(a)
            else:
                final_ans.append(a+"\n")
        except:
            pass
flag = True
for i in final_ans:
    if i.rstrip('\n').isdigit() == False:
        print(i)
        flag = False
        break
if flag == True:
    for i in final_ans:
        print(i, end="")
