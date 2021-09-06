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
        if 1 <= opp <= 14:
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
            return r_a, r_b, r_out, isANum

    def getInstrNum(self, n):
        opp = self.get_opp(n)
        regs = self.get_regs(n, opp)
        if 1 <= opp <= 14:
            r_a, r_b, r_out, isANum = regs
            instr = 0
            instr += opp << 27
            instr += r_a << 22
            instr += isANum << 21
            instr += r_b << 5
            instr += r_out

        return instr

    def writeInstr(self, instr, n):
        f = open("../output_files/test.txt", 'a')
        f.write("0x" + str(n) + " " + str(hex(instr)) + "\n")
        f.close()




