from assembleur import Assembleur

asm = Assembleur("../assembly_program_files/test.txt")
for i in range(len(asm.instrList)):
    instr = asm.getInstrNum(i)
    asm.writeInstr(instr, i)
    print(i)