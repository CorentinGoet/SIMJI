"""
@author Corentin Goetghebeur (github.com/CorentinGoet)
This python file contains the class meant to convert the assembly code in hex values.
It is the second step of the assembly.
"""


class Translation:
    """
    This python class converts the formatted assembly code in hexadecimal values.
    """
    def __init__(self, filepath):
        file = open(filepath)
        self.lines = file.readlines()
        file.close()
        self.hexlines = []
        self.operations = ["stop", "add", "sub", "mul", "div", "and", "or", "xor", "shl", "shr", "slt", "sle", "seq",
                           "load", "store", "jmp", "braz", "branz", "scall"]

    def get_op(self, line):
        """
        This function takes the assembly code line and returns its operation.
        :param line: line of assembly code
        :return: operation code
        """
        return self.operations.index(line.strip().split(" ")[0])

    def get_params(self, line):
        """
        This method returns the parameters of an assembly code line.
        For operations 1->14 the keys are 'r1', 'o' and 'r2',
        for operation 15 the keys are 'o' and 'r',
        for operations 16 and 17, the keys are 'r' and 'a'
        for operation 18, the key is 'n'
        :param line: line of assembly code
        :return: parameters (dict)
        """

        parameters = {}
        op = self.get_op(line)

        if op == 0:
            # No parameters for stop operation
            return parameters
        params = line.split(" ")[1]
        if 1 <= op <= 14:
            parameters['r1'], parameters['o'], parameters['r2'] = params.strip().split(",")

        if op == 15:
            # jmp
            parameters['o'], parameters['r'] = params.strip().split(',')

        if op in [16, 17]:
            # braz or branz
            parameters['r'], parameters['a'] = params.strip().split(',')

        if op == 18:
            # scall
            parameters['n'] = params.strip()

        return parameters

    def encode(self, line):
        """
        Method to translate an assembly code line into hexadecimal instruction for the ISS.
        """

        op = self.get_op(line)
        if op == 0:
            # stop
            return 0

        parameters = self.get_params(line)

        # Write the operation (bits 27 -> 31)
        hexline = op << 27

        # Write the parameters
        if 1 <= op <= 14:
            # r1 at bit 22, imm at bit 21, o at bit 5, r2 at bit 0
            imm, o = self.format_param(parameters['o'])
            hexline += int(parameters['r1'][1:]) << 22
            hexline += imm << 21
            hexline += o << 5
            hexline += int(parameters['r2'][1:])

        if op == 15:
            # jmp: imm at bit 26, o at bit 5 and r at bit 0
            imm, o = self.format_param(parameters['o'])

            hexline += imm << 26
            hexline += int(parameters['o']) << 5
            hexline += o

        if op in [16, 17]:
            # braz/branz: r at bit 22 and a at bit 0
            hexline += int(parameters['r'][1:]) << 22
            hexline += int(parameters['a'])

        if op == 18:
            # scall: n at 0
            hexline += int(parameters['n'])

    def format_param(self, o_param):
        """
        Sub-method for encode() to format parameters o.
        """
        if o_param == 'r':
            # if o is a register
            imm = 0
            o_param = o_param[1:]
        else:
            imm = 1
        return imm, int(o_param)

    def write_hex(self, filepath):
        """
        Writes the hex lines in a file.
        """
        for i in range(len(self.hexlines)):


if __name__ == '__main__':
    print("This python file is not meant to be executed on its own, please refer to README.md for more informations.")
