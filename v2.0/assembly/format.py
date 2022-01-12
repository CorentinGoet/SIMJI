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
        self.labels = {}


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
            self.lines[i] = str(i) + ' ' + self.lines[i]

    def remove_blanks(self):
        """
        This function removes the blank lines from the file.
        (The lines with only a number added by self.number() are deleted as well)
        It also removes any spaces at the end of lines.
        """
        nb_lines = len(self.lines)

        # Find the lines to remove
        lines_to_remove = []
        for i in range(nb_lines):
            self.lines[i] = self.lines[i].strip()+"\n"
            line = self.lines[i]
            if line == "":  # remove empty lines
                lines_to_remove.append(line)

            # remove lines with only a number (also works with number +\n)
            try:
                int(line)
                lines_to_remove.append(line)
            except ValueError as e:
                pass

        # remove the lines
        for line in lines_to_remove:
            try:
                self.lines.remove(line)
            except ValueError:
                print("Formatting error: a blank line could not be removed")

    def remove_comments(self):
        """
        This function removes anything after a '#' or ';' in all lines.
        """
        for i in range(len(self.lines)):
            line = self.lines[i]
            clean_line = line

            # Try to find a comment with #
            try:
                ind = line.index('#')
                clean_line = line[0:ind] + "\n"

            except ValueError as e:
                pass

            # Try to find comment with ;
            try:
                ind = line.index(';')
                clean_line = line[0:ind] + "\n"

            except ValueError as e:
                pass

            # replace the line
            self.lines[i] = clean_line

    def find_labels(self):
        """
        This function finds the labels with their address in the file.
        """
        # find labels
        self.labels = {}
        lines_to_remove = []

        nb_lines = len(self.lines)
        for i in range(nb_lines):
            line = self.lines[i]

            if ":\n" in line:   # The label is the full line it means we have to jump to the next instruction
                label = line.split(" ")[1][:-2]  # we have to remove the ':' and the '\n'
                address = int(self.lines[i+1].split(" ")[0])
                self.labels[label] = address
                lines_to_remove.append(line)

            elif ":" in line:
                # add label to the list
                label = line.split(" ")[1][:-1]
                address = int(line.split(" ")[0])
                self.labels[label] = address

                # remove label from the line
                clean_line = ""
                for element in line.split(" "):
                    if clean_line != "" and ":" not in element:
                        clean_line += " "
                    if ":" not in element:
                        clean_line += element

                self.lines[i] = clean_line

        # remove the lines with only the label
        for line in lines_to_remove:
            self.lines.remove(line)

    def replace_labels(self):
        """
        This function replaces the Labels in the assembly code instructions jump, braz and branz by their address.
        """
        nb_lines = len(self.lines)
        for i in range(nb_lines):
            # only look for jmp, braz and branz
            line = self.lines[i]
            if line.split(" ")[1] in ['jmp', 'braz', 'branz']:
                nb, instruction, params = line.split(" ")
                param1, param2 = params.split(",")
                if instruction == 'jmp' and param1 in self.labels.keys():
                    self.lines[i] = nb + " " + instruction + " " + str(self.labels[param1]) + "," + param2

                if instruction in ['braz', 'branz'] and param2[:-1] in self.labels.keys():
                    self.lines[i] = nb + " " + instruction + " " + param1 + "," + str(self.labels[param2[:-1]]) + "\n"

    def rectify_numbers(self):
        """
        This method corrects the numbers in the jumps and branches.
        The structure is very similar to replace labels
        """
        # Build the dict of (old line number => new)
        line_numbers = {}
        for i in range(len(self.lines)):
            line = self.lines[i]
            old_val = line.split(" ")[0]
            line_numbers[old_val] = i

        # Replace in the jumps and branches
        for i in range(len(self.lines)):
            line = self.lines[i]
            if line.split(" ")[1] in ['jmp', 'braz', 'branz']:
                nb, instruction, params = line.split(" ")
                param1, param2 = params.split(",")
                if instruction == 'jmp' and param1 in line_numbers.keys():
                    self.lines[i] = nb + " " + instruction + " " + str(line_numbers[param1]) + "," + param2

                if instruction in ['braz', 'branz'] and param2[:-1] in line_numbers.keys():
                    self.lines[i] = nb + " " + instruction + " " + param1 + "," + str(line_numbers[param2[:-1]]) + "\n"

            # remove the line number
            line_list = self.lines[i].split(" ")[1:]
            self.lines[i] = ""
            for element in line_list:
                self.lines[i] += element + " "
            self.lines[i] = self.lines[i][:-1]


if __name__ == '__main__':
    print("This python file is not meant to be executed on its own, please refer to README.md for more informations.")

