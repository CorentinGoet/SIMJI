"""
@author Corentin GOETGHEBEUR (SNS 2023)
Ce programme contient la modélisation de l'iss.
"""
import time

class VM:

    def __init__(self, programFile, cache):
        """
        Constructeur de la classe VM.
        :param programFile: nom du programme hexadécimal à executer.
        :param cache: Objet cache servant à l'execution
        """
        self.regs = [0] * 32  # 32 registers
        self.prog = self.progLoad(programFile)
        self.pc = 0
        self.running = False
        self.cache = cache
        self.perf = []


    def progLoad(self, fileName):
        """
        Charge les instructions du programme dans une liste de chaines de caractères.
        :param fileName: Nom du programme à charger
        :return: Liste d'instructions
        """
        f = open(fileName)
        instrList = f.readlines()

        for i in range(len(instrList)):
            instrList[i] = int(instrList[i].split(" ")[1], 16)
        return instrList

    def fetch(self):
        """
        Méthode d'accès à la mémoire de programme modélisée par une liste.
        :return: instruction suivante dans l'execution.
        """
        instr = self.prog[self.pc]
        self.pc += 1
        return instr

    def decode(self, instr):
        """
        Méthode de reconstruction de l'instruction hexadécimale.
        :param instr: instruction
        :return: Numéro de l'opération, (argument1, argument 2, ...)
        """
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
        """
        Méthode d'exécution de l'instruction sur les registres.
        :param opp: Opération
        :param regs: arguments (Ex: R_a, o, R_b)
        :return: None
        """
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
                self.regs[r_b] = self.regs[r_a] * o
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
            if action == 1:
                print("R1 : ", self.regs[1])
            else:
                self.regs[1] = int(input("R1 : "))

    def run(self):
        """
        Méthode d'execution de l'iss.
        :return: (Nombre d'opérations effectuées, temps total d'exécution, nombre d'opérations par secondes
        """
        t_ini = time.time()
        nb_op = 0   # compteur d'opérations
        self.running = True
        while self.running:
            i = self.pc
            instr = self.fetch()
            opp, regs = self.decode(instr)
            self.eval(opp, regs)
            nb_op += 1

        t_op = time.time() - t_ini
        self.perf = nb_op, t_op, self.cache.perf_counter, self.cache.perf_counter_cache


