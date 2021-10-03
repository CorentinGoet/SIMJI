class Assembleur:

    def __init__(self, instr_file_name):
        self.instr_file_name = instr_file_name
        self.oppList = ['STOP', 'ADD', 'SUB', 'MULT', 'DIV', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'SLT', 'SLE', 'SEQ', 'LOAD', 'STORE', 'JMP', 'BRAZ', 'BRANZ', 'SCALL']
        self.instrList = self.get_instr()
        self.labels = self.get_labels()

    def get_labels(self):
        """
        Récupère les labels et les correspondances avec les lignes.
        """
        labelDict = {}  # dictionnaire des labels
        # on parcours la liste en cherchant les labels
        for instr in self.instrList:
            firstWord = instr.split(' ')[0]     # on récupère le 1er mot
            if firstWord[-1] == ":":   # on considère comme label les 1ers mots qui se terminent par :
                ind = self.instrList.index(instr)
                labelDict[firstWord[:-1]] = ind     # on ajoute le label à la liste
                self.instrList[ind] = self.instrList[ind][len(firstWord) +1:]  # supprime le label de la ligne

        return labelDict


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
        print(oppTxt)
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
            elif o[0] == "L":
                isANum = 1
                o = int(self.labels[o])
            else:
                isANum = 1
                o = int(o)

            return o, int(r[1:]), isANum

        elif opp in [16, 17]:     # braz ou branz
            r, a = regs.split(",")
            if a[0] == "L":     # si a est un label on le remplace par le num de ligne
                a = self.labels[a.strip("\n")]

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

            while not - (1 << 16) < r_b < (1 << 16) - 1:
                r_b -= 1 << 16

            if r_b < 0:
                r_b = (1 << 16) + r_b
                print("nombre négatif ", r_b, bin(r_b))
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
        f = open("../instruction_files/instructions.hex", 'a')
        f.write("0x" + str(n) + " " + str(hex(instr)) + " " + "\n")
        f.close()

    def writeInstr2(self, instr, n, outputFile):
        f = open(outputFile, 'a')
        f.write("0x" + str(n) + " " + str(hex(instr)) + " " + "\n")
        f.close()




