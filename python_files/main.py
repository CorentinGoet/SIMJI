from assembleur import Assembleur
from ISS import VM



asm = Assembleur("../assembly_program_files/test_branch.txt")


for i in range(len(asm.instrList)):
    instr = asm.getInstrNum(i)
    asm.writeInstr(instr, i)
    print(i)

vm = VM("../output_files/test.txt")
vm.run()
print(VM.mem)