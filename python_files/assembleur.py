class Assembleur:

    def __init__(self, instr_file_name):
        self.instr_file_name = instr_file_name
        self.oppList = ['STOP', 'ADD', 'SUB', 'MULT', 'DIV', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'SLT', 'SLE', 'SEQ', 'LOAD', 'STORE', 'JMP', 'BRAZ', 'BRANZ', 'SCALL']
        self.instrList = self.get_instr()


    def get_instr(self):
        f = open(self.instr_file_name, 'r')
        l = f.readlines()
        f.close()
        f = open("../output_files/test.txt",'w')
        f.write('')
        f.close()
        return l

    def get_opp(self, n):

        word = self.instrList[n]
        oppTxt = word.split(" ")[0]
        return self.oppList.index(oppTxt)

    def get_regs(self, n, opp):
        word = self.instrList[n]
        if opp != 0:
            trash, regs = word.split(" ")
        else:
            regs = 0

        if 1 <= opp <= 14:  # operations à 3 arguments

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
            return r_a, r_b, r_out, isANum

        elif opp == 15:     # jmp
            o, r = regs.split(",")
            if o[0] == "R":
                isANum = 0
                o = int(o[1:])
            else:
                isANum = 1
                o = int(o)

            return o, int(r[1:]), isANum

        elif opp in [16, 17]:     # braz ou branz
            r, a = regs.split(",")
            return int(r[1:]), int(a)

        elif opp == 18:     # scall
            return int(regs)

        else:
            return 0






    def getInstrNum(self, n):
        opp = self.get_opp(n)
        regs = self.get_regs(n, opp)
        if opp == 0:
            instr = 0

        elif 1 <= opp <= 14:
            r_a, r_b, r_out, isANum = regs
            instr = 0
            instr += opp << 27
            instr += r_a << 22
            instr += isANum << 21
            instr += r_b << 5
            instr += r_out

        elif opp == 15:     # jmp
            o, r, isANum = regs
            instr = 0
            instr += opp << 27
            instr += isANum << 26
            instr += o << 5
            instr += r

        elif opp in [16, 17]:
            r, a = regs
            instr = 0
            instr += opp << 27
            instr += r << 22
            instr += a

        elif opp == 18:
            n = regs
            instr = 0
            instr += opp << 27
            instr += n

        return instr


    def writeInstr(self, instr, n):
        f = open("../output_files/test.txt", 'a')
        f.write("0x" + str(n) + " " + str(hex(instr)) + "\n")
        f.close()




