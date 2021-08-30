"""
This file contains the program to translate assembly code to binary instructions.
"""

f_instr = open("..//assembly_program_files/test.txt", 'r')     # opening the file
word = f_instr.readline()
f_instr.close()
opp, regs = word.split(" ")  # we only keep the first word
regs = regs.split(",")
r_a = int(regs[0][1:])
r_b = regs[1]
r_out = int(regs[-1][1:])


# determines whether r_b is a register or a number
if r_b[0] == "R":
    isANum = 0
    r_b = int(r_b[1:])
else:
    isANum = 1
    r_b = int(r_b)

if opp == "ADD":
    binaryOpp = 1

# final instruction number
instr = 0
instr += binaryOpp << 27
instr += r_a << 22
instr += isANum << 21
instr += r_b << 5
instr += r_out

# writing result in a file
f_out = open("../output_files/test.txt", 'w')
f_out.write(str(instr) + "  ~  " + str(hex(instr)))
f_out.close()