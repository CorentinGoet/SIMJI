#!/usr/bin/env python3
"""
@author Corentin GOETGHEBEUR (SNS 2023)
"""

import sys
from assembleur import Assembleur
from Data import Storage, Cache
from VM import VM
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
        self.perf = self.read_file("../interface_files/perf.txt")

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

    def display_perf(self, nb_op, t_op, data_op, data_op_cache):
        """
        Print performances
        :param nb_op: number of operations done
        :param t_op: run time
        :return: None
        """
        perf = round(nb_op / t_op)  # Number of operations per second
        data_perf = nb_op + data_op
        data_perf_cache = nb_op + data_op_cache
        s = self.perf.format(nb_op, t_op, perf, data_perf, data_perf_cache)
        print(s)

    def run_assemble(self):
        """
        Run asssembly program.
        :return: None
        """
        if self.nb_params == 2 or self.params[2] in ['-h', '--help']:     # Only given argument was assemble
            self.display_help('assemble')
        else:

            output_file = self.params_assemble()

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

    def params_assemble(self):
        """
        Parameters management for asm / assemble.
        :return: output_file
        """
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
        return output_file

    def run_execute(self):
        """
        Run iss.
        :return:None
        """
        if self.nb_params == 2 or self.params[2] in ['-h', '--help']:     # given parameter is only execute or execute -h
            self.display_help('execute')

        else:
            try:
                # parameters recognition
                instruction_file = self.params[2]
                data_file, cache_display, memory_display, debug, perf = self.params_exec()

                # Data storage creation
                dataMem = Storage()
                if data_file is None:
                    print("Creating data storage ...")
                else:
                    print("Loading data storage ...")
                    print(data_file)
                    dataMem.loadMem(data_file)

                print("Creating cache ...")
                cache = Cache(dataMem)

                # execution
                print("Starting ISS ...")
                vm = VM(instruction_file, cache)
                print("Computing instructions from {}...".format(instruction_file))
                res = vm.run()
                print("Writing data file ...")
                vm.cache.memory.writeMem("../output_files/memoire.hex")
                if cache_display:
                    print(vm.cache)
                if memory_display:
                    print(vm.cache.memory)
                if perf:
                    try:
                        nb_op, t_op, data_counter, data_counter_cache = vm.perf
                        self.display_perf(nb_op, t_op, data_counter, data_counter_cache)
                    except ZeroDivisionError:
                        print("Runtime too short to display performances.")


            except FileNotFoundError:
                print('Instruction file not found.')
            #except Exception as e:
            #   print("Execution error.")
            #   print(e)


    def params_exec(self):
        """
        Parameters management for iss / execute.
        :return: [data_input_file, cache_display (bool), memory_display (bool), debug (bool), perf (bool)]
        """
        if '-d' in self.params:
            data_id = self.params.index('-d')
            try:
                data_file = self.params[data_id + 1]
            except FileNotFoundError:
                raise Exception("Data file not found.")

        if '--data' in self.params:
            data_id = self.params.index('-d')
            try:
                data_file = self.params[data_id + 1]
            except FileNotFoundError:
                raise Exception("Data file not found.")

        if not ('-d' in self.params or '--data' in self.params):
            data_file = None

        cache_display = '-c' in self.params or '--cache' in self.params
        memory_display = '-m' in self.params or '--memory' in self.params
        debug = '-d' in self.params or '--debug' in self.params
        perf = '-p' in self.params

        return [data_file, cache_display, memory_display, debug, perf]



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
                self.run_execute()

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
