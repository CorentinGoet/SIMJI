"""
@author Corentin Goetghebeur (github.com/CorentinGoet)
This python file contains the class meant to reformat the assembly code before the translation to hexadecimal.
"""


class Format:
    """
    This class formats the assembly code to be translated to hexadecimal by translation.py
    This reformatting is made in several steps:
    - add number to each line
    - remove comments and blank lines
    - remove labels and replace with line number
    """
    def __init__(self, filepath):

        # Read the file
        self.file = open(filepath)
        self.lines = self.file.readlines()
        self.file.close()


    def write_file(self, output_file="tmp_asm.asm"):
        """
        This method writes the content of self.lines in the specified file.
        """
        file = open(output_file, 'w')
        for line in self.lines:
            file.write(line)


    def number(self):
        """
        This function adds a temporary number before each line to ensure jumps and branches go to the right address.
        """
        nb_lines = len(self.lines)
        for i in range(nb_lines):
            self.lines[i] = str(i) + self.lines[i]


    def remove_blanks(self):
        """
        This function removes the blank lines from the file.
        (The lines with only a number added by self.number() are deleted as well)
        """
        pass

    def remove_comments(self):
        """
        This function removes anything after a '#' or ';' in all lines.
        """
        pass

    def replace_labels(self):
        """
        This function replace the labels with their address in the file.
        """
        pass


if __name__ == '__main__':
    print("This python file is not meant to be executed on its own, please refer to README.md for more informations.")
    f = Format("examples/ex1.asm")
    f.number()
    print(f.lines)
