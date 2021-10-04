import Memory


class VM:

    def __init__(self, programFile, cache):
        self.regs = [0] * 32  # 32 registers
        self.prog = self.progLoad(programFile)
        self.pc = 0
        self.running = False
        self.cache = cache


    def progLoad(self, fileName):
        f = open(fileName)
        instrList = f.readlines()

        for i in range(len(instrList)):
            instrList[i] = int(instrList[i].split(" ")[1], 16)
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
            binary_string_o = bin(o)[2:].rjust(15,'0')
            if binary_string_o[0] == '1':
                o -= (1 << 15)


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

        elif instrNum == 18:
            a = instr & ((1 << 26) - 1)
            return instrNum, a



    def eval(self, opp, regs):

        if opp == 0:
            self.running = 0
        elif 1 <= opp <= 14:
            r_a, isANum, o, r_b = regs
            if isANum == 0:
                o = self.regs[o]

            if opp == 1:
                self.regs[r_b] = self.regs[r_a] + o
            elif opp == 2:
                self.regs[r_b] = self.regs[r_a] - o
            elif opp == 3:
                self.regs[r_b] =self.regs[r_a] * o
            elif opp == 4:
                self.regs[r_b] = self.regs[r_a] // o
            elif opp == 5:
                self.regs[r_b] = self.regs[r_a] & o
            elif opp == 6:
                self.regs[r_b] = self.regs[r_a] | o
            elif opp == 7:
                self.regs[r_b] = self.regs[r_a] ^ o
            elif opp == 8:
                self.regs[r_b] = self.regs[r_a] << o
            elif opp == 9:
                self.regs[r_b] = self.regs[r_a] >> o
            elif opp == 10:
                self.regs[r_b] = int(self.regs[r_a] < o)
            elif opp == 11:
                self.regs[r_b] = int(self.regs[r_a] <= o)
            elif opp == 12:
                self.regs[r_b] = int(self.regs[r_a] == o)
            elif opp == 13:
                self.regs[r_b] = self.cache.read(self.regs[r_a] + o)
            elif opp == 14:
                self.cache.write_through(self.regs[r_a] + o, self.regs[r_b])
        elif opp == 15:
            isANum, o, r = regs
            self.regs[r] = o
            self.pc = o

        elif opp == 16:
            r, a = regs
            if self.regs[r] == 0:
                self.pc = a

        elif opp == 17:
            r, a = regs
            if not(self.regs[r] == 0):
                self.pc = a

        elif opp == 18:
            action = regs
            if action == 0:
                print("R1 : ", self.regs[1])
            else:
                self.regs[1] = int(input("R1 : "))

    def run(self):
        self.running = True
        while self.running:
            i = self.pc
            instr = self.fetch()
            opp, regs = self.decode(instr)
            print("operation ", opp)

            self.eval(opp, regs)

