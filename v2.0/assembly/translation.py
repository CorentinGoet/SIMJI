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
        self.lines = self.file.readlines()
        file.close()

        self.operations = ["stop", "add", "sub", "mul", "div", "and", "or", "xor", "shl", "shr", "slt", "sle", "seq",
                           "load", "store", "jmp", "braz", "branz", "scall"]

    def get_op(self, line):
        """
        This function takes the assembly code line and returns its operation.
        :param line: line of assembly code
        :return: operation code
        """
        return self.operations.index(line.split(" ")[0])

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


            


if __name__ == '__main__':
    print("This python file is not meant to be executed on its own, please refer to README.md for more informations.")
