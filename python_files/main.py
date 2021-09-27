#!/usr/bin/env python3

from assembleur import Assembleur
from ISS import VM
from Memory import Cache, Memory

asm = Assembleur("../assembly_program_files/test_scall.asm")
cache = Cache(Memory())

print(cache)
for i in range(len(asm.instrList)):
    instr = asm.getInstrNum(i)
    asm.writeInstr(instr, i)
    print(i)

vm = VM("../output_files/instructions.hex", cache)
vm.run()
print(cache)
#print(cache.memory)
