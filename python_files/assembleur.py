class Assembleur:

    def __init__(self, instr_file_name):
        self.instr_file_name = instr_file_name
        self.oppListOld = ['STOP', 'ADD', 'SUB', 'MULT', 'DIV', 'AND', 'OR', 'XOR', 'SHL', 'SHR', 'SLT', 'SLE', 'SEQ', 'LOAD', 'STORE', 'JMP', 'BRAZ', 'BRANZ', 'SCALL']
        self.oppListNew = ['stop', 'add', 'sub', 'mul', 'div', 'and', 'or', 'xor', 'shl', 'shr', 'slt', 'sle', 'seq', 'load', 'store', 'jmp', 'braz', 'branz', 'scall']
        self.instrList = self.get_instr()
        self.removeComments()
        self.labels = self.get_labels()
        #self.removeComments()

    def get_labels(self):
        """
        Récupère les labels et les correspondances avec les lignes.
        """
        labelDict = {}  # dictionnaire des labels
        # on parcours la liste en cherchant les labels
        for instr in self.instrList:
            firstWord = instr.split(' ')[0]     # on récupère le 1er mot

            if ":\n" in firstWord:
                ind = self.instrList.index(instr)
                self.instrList.pop(ind)
                labelDict[firstWord[:-2]] = ind

            if firstWord[-1] == ":":   # on considère comme label les 1ers mots qui se terminent par :
                ind = self.instrList.index(instr)
                labelDict[firstWord[:-1]] = ind     # on ajoute le label à la liste
                self.instrList[ind] = self.instrList[ind][len(firstWord) + 1:]  # supprime le label de la ligne

        return labelDict

    def removeComments(self):
        """
        Supprime les commentaires du fichier assembleur.
        Sont considérées comme commentaires les parties de lignes situées après ; ou #.
        :return:None
        """

        for i in range(len(self.instrList)):

            # essai de commentaire avec #
            try:
                instr = self.instrList[i]
                ind = instr.index('#')
                instr = instr[:ind]
                self.instrList[i] = instr

            except Exception as e:
                pass

            # commentaires en ;
            try:
                instr = self.instrList[i]
                ind = instr.index(';')
                instr = instr[:ind]
                self.instrList[i] = instr
            except Exception as e:
                pass

        # suppression des espaces en début et fin de ligne + retour fin de ligne
        for i in range(len(self.instrList)):

            instr = self.instrList[i]

            if instr[-2:] == "\n":
                instr = instr[:-2]


            while len(instr) > 0 and instr[-1] == ' ':
                instr = instr[:-1]

            while len(instr) > 0 and instr[0] == ' ':
                instr = instr[1:]

            self.instrList[i] = instr

        # suppression des lignes vides
        print(self.instrList)
        while "" in self.instrList:
            self.instrList.remove("")
        while "\n" in self.instrList:
            self.instrList.remove("\n")
        print(self.instrList)

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

        try:
            oppTxt = oppTxt.strip("\n")
        except Exception as e:
            pass

        # essai avec la syntaxe majuscule
        try:
            ind = self.oppListOld.index(oppTxt)
        except Exception as e:
            print("pas de correspondance maj")


        # essai avec la syntaxe minuscule
        try:
            ind = self.oppListNew.index(oppTxt)
        except Exception as e:
            print("pas de correspondance min")
        return ind

    def get_regs(self, n, opp):
        word = self.instrList[n]
        if opp != 0:
            print("word: ", word)
            tmp = word.split(" ")

            while len(tmp) > 2:
                print('erreur tmp:', tmp)
                lastElement = tmp.pop()
                tmp[-1] = tmp[-1] + lastElement

            if "" in tmp:
                tmp.remove("")
            trash, regs = tmp[0], tmp[1]
        else:
            regs = 0

        if 1 <= opp <= 14:  # operations à 3 arguments

            regs = regs.split(",")
            print("regs: ", regs)
            r_a = int(regs[0][1:])
            r_b = regs[1]
            r_out = int(regs[-1][1:])

            # determines whether r_b is a register or a number
            if r_b[0] in ['r', 'R']:
               isANum = 0
               r_b = int(r_b[1:])
            else:
               isANum = 1
               r_b = int(r_b)
            return r_a, r_b, r_out, isANum

        elif opp == 15:     # jmp
            o, r = regs.split(",")

            if o[0] in ["R", 'r']:
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
            print("a:", a)
            if a[0] == "L":     # si a est un label on le remplace par le num de ligne
                try:
                    a = a.strip("\n")
                except Exception as e:
                    pass
                print(self.labels)
                a = self.labels[a]
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

        if n == 0:
            f = open("../instruction_files/instructions.hex", 'w')
        else:
            f = open("../instruction_files/instructions.hex", 'a')
        f.write(str(hex(n)) + " " + str(hex(instr)) + " " + "\n")
        f.close()

    def writeInstr2(self, instr, n, outputFile):
        f = open(outputFile, 'a')
        f.write(str(hex(n)) + " " + str(hex(instr)) + " " + "\n")
        f.close()




