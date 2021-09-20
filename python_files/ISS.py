class VM:
    mem = [0]*1024    # mémoire de données
    def __init__(self, programFile):
        self.regs = [0] * 32  # 32 registers
        self.prog = self.progLoad(programFile)
        self.pc = 0
        self.running = False


    def progLoad(self, fileName):
        f = open(fileName)
        instrList = f.readlines()

        for i in range(len(instrList)):
            instrList[i] = int(instrList[i].split(" ")[1][:-1], 16)
        return instrList

    def fetch(self):
        instr = self.prog[self.pc]
        self.pc += 1
        return instr

    def decode(self, instr):
        instrNum = (instr & (0B11111 << 27)) >> 27

        if instrNum == 0:
            return 0, 0

        elif 1 <= instrNum <= 14:
            r_a = (instr & (0B1111 << 22)) >> 22
            isANum = (instr & (1 << 21)) >> 21
            o = (instr & (0B111111111111111 << 5)) >> 5
            r_b = instr & 0B1111

            return instrNum, (r_a, isANum, o, r_b)

        elif instrNum == 15:
            isANum = (instr & 1 << 26) >> 26
            o = (instr & (0xFFFFFF0 ^ (0b11 << 26))) >> 5
            r = (instr & 0b1111)

            return instrNum, (isANum, o, r)

        elif instrNum in [16, 17]:
            r = (instr & (0b11111 << 22)) >> 22
            a = instr & ((1 << 22) - 1)
            return instrNum, (r, a)



    def eval(self, opp, regs):

        if opp == 0:
            print("STOP")
            self.running = 0
        elif 1 <= opp <= 14:
            r_a, isANum, o, r_b = regs
            if isANum == 0:
                o = self.regs[o]

            if opp == 1:
                print("ADD")
                self.regs[r_b] = self.regs[r_a] + o
            elif opp == 2:
                print("SUB")
                self.regs[r_b] = self.regs[r_a] - o
            elif opp == 3:
                print("MULT")
                self.regs[r_b] =self.regs[r_a] * o
            elif opp == 4:
                print("DIV")
                self.regs[r_b] = self.regs[r_a] // o
            elif opp == 5:
                print("AND")
                self.regs[r_b] = self.regs[r_a] & o
            elif opp == 6:
                print("OR")
                self.regs[r_b] = self.regs[r_a] | o
            elif opp == 7:
                print("XOR")
                self.regs[r_b] = self.regs[r_a] ^ o
            elif opp == 8:
                print("SHL")
                self.regs[r_b] = self.regs[r_a] << o
            elif opp == 9:
                print("SHR")
                self.regs[r_b] = self.regs[r_a] >> o
            elif opp == 10:
                print("SLT")
                self.regs[r_b] = int(self.regs[r_a] < o)
            elif opp == 11:
                print("SLE")
                self.regs[r_b] = int(self.regs[r_a] <= o)
            elif opp == 12:
                print("SEQ")
                self.regs[r_b] = int(self.regs[r_a] == o)
            elif opp == 13:
                print("LOAD")
                self.regs[r_b] = VM.mem[self.regs[r_a] + o]
            elif opp == 14:
                print("STORE")
                VM.mem[self.regs[r_a] + o] = self.regs[r_b]
        elif opp == 15:
            print("JMP")
            isANum, o, r = regs
            self.regs[r] = o
            self.pc = o

        elif opp == 16:
            print("BRAZ")
            r, a = regs
            print("registre {} : {}".format(r, self.regs[r]))
            if self.regs[r] == 0:
                print("branchement vers ", a)
                self.pc = a

        elif opp == 17:
            print("BRANZ")
            r, a = regs
            if not(self.regs[r] == 0):
                print("branchement vers ", a)
                self.pc = a

    def run(self):
        self.running = True
        while self.running:
            i = self.pc
            print("line {} started".format(i))
            instr = self.fetch()
            opp, regs = self.decode(instr)
            self.eval(opp, regs)
            print("registres :", self.regs)
            print("line {} OK".format(i))
