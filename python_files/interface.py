#!/usr/bin/env python3
"""
@author Corentin GOETGHEBEUR (SNS 2023)
"""

import sys
from assembleur import Assembleur
import VM
import time


class Interface:
    """
    This class implements a command line interface for the project.
    """

    def __init__(self):
        self.params = sys.argv
        self.nb_params = len(self.params)
        self.title = self.read_file("../interface_files/title.txt")
        self.help = self.read_file("../interface_files/help.txt")
        self.help_asm = self.read_file("../interface_files/help_asm.txt")
        self.help_iss = self.read_file("../interface_files/help_iss.txt")

    def read_file(self, title_file):
        """
        File reading method reading all the content.
        :return: content of the file (String)
        """
        with open(title_file, 'r') as file:
            return file.read()

    def display_menu(self):
        """
        Print menu file.
        :return: None
        """
        print(self.title)

    def display_help(self, program='default'):
        """
        Print help file.
        :return: None
        """
        if program == 'default':
            print(self.help)
        elif program == 'assemble':
            print(self.help_asm)
        elif program == 'execute':
            print(self.help_iss)

    def run_assemble(self):
        """
        Run asssembly program.
        :return: None
        """
        if self.nb_params == 2:     # Only given argument was assemble
            self.display_help('assemble')
        else:

            if self.nb_params == 4:
                print("Unknown or misused parameters have been ignored.")

            if self.nb_params == 5:
                p1 = self.params[3]  # -o ou --output en fonctionnement normal
                p2 = self.params[4]  # nom du fichier de sortie
                if p1 not in ['-o', '--output']:
                    raise Exception('Unkown parameter or misused parameter: {}'.format(p1))
                output_file = p2
            else:
                output_file = "../instruction_files/instructions.hex"


            file_name = self.params[2]
            try:
                file = open(file_name)
                print("Opening file ...")
                asm = Assembleur(file_name)
                print("Assembly ...")
                for i in range(len(asm.instrList)):
                    instr = asm.getInstrNum(i)
                    asm.writeInstr2(instr, i, output_file)
                print("Assembly finished.")

            except FileNotFoundError as e:
                print("File not found.")
                print(e)
            except Exception as e:
                print("Execution error.")
                print(e)

    def run_execute(self):
        """
        Run iss.
        :return:None
        """
        if self.nb_params == 2:     # Only given parameter is execute
            self.display_help('execute')





    def run(self):
        """
        Main method for execution.
        :return: int (0 if success, error number if failure)
        """

        res = 0

        if self.nb_params == 1:     # Only one parameter -> nothing was given to the program
            self.display_menu()

        else:   # One param was given assemble, execute or help
            p = self.params[1]

            if p in ['-h', '--help']:   # show general help
                self.display_help()

            elif p == 'assemble':
                self.run_assemble()

            elif p == 'execute':
                print('not implemented yet.')

            else:   # error message
                print("Syntax error : Unknown parameter")
                res = 1

        return res







if __name__ == '__main__':
    title = "../Ressources/interface_files/title.txt"
    help = "../Ressources/interface_files/help.txt"
    i = Interface()
    i.display_menu()
    i.display_help()
