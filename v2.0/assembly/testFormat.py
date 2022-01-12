import unittest
from format import Format
import os


class TestFormat(unittest.TestCase):
    """
    @author Corentin Goetghebeur
    Unit test class for the Format class.
    """
    def setUp(self):
        # This is executed before each Method
        pass

    def test_write_file(self):
        """
        Test method for write_file.
        """
        input_file_name = "test_files/test_write_file.asm"
        output_file_name = "test_files/output_write_file.asm"

        # execute method
        f = Format(input_file_name)
        f.write_file(output_file_name)

        # check result
        ref_file = open(input_file_name)
        test_file = open(output_file_name)

        self.assertEqual(ref_file.read(), test_file.read())

        ref_file.close()
        test_file.close()
        os.remove(output_file_name)

    def test_number(self):
        """
        Test method for the number method.
        """
        f = Format("test_files/test_asm.asm")
        f.number()
        for line in f.lines:
            self.assertEqual(int(line[0]), f.lines.index(line))

    def test_remove_comments(self):
        """
        Test method for remove_comments.
        """
        input_file_name = "test_files/test_remove_comments.asm"
        output_file_name = "test_files/output_remove_comments.asm"
        ref_file_name = "test_files/ref_test_remove_comments.asm"

        f = Format(input_file_name)
        f.remove_comments()
        f.write_file(output_file_name)

        output_file = open(output_file_name)
        ref_file = open(ref_file_name)
        self.assertEqual(output_file.read(), ref_file.read())

        output_file.close()
        ref_file.close()
        os.remove(output_file_name)

    def test_remove_blanks(self):
        """
        Test methods for remove_blanks
        """
        input_file_name = "test_files/test_remove_blanks.asm"
        output_file_name = "test_files/output_remove_blanks.asm"
        ref_file_name = "test_files/ref_test_remove_blanks.asm"

        f = Format(input_file_name)
        f.remove_blanks()
        f.write_file(output_file_name)

        ref_file = open(ref_file_name)
        output_file = open(output_file_name)
        self.assertEqual(ref_file.read(), output_file.read())

        ref_file.close()
        output_file.close()
        os.remove(output_file_name)

    def test_find_labels(self):
        """
        Test method for find_labels.
        """
        input_file_name = "test_files/test_replace_labels.asm"
        output_file_name = "test_files/output_find_labels.asm"
        ref_file_name = "test_files/ref_test_find_labels.asm"

        f = Format(input_file_name)
        f.number()
        f.remove_comments()
        f.remove_blanks()
        f.find_labels()
        f.write_file(output_file_name)

        output_file = open(output_file_name)
        ref_file = open(ref_file_name)
        self.assertEqual(output_file.read(), ref_file.read())
        expected_labels = {'L1': 4, 'L_end': 11}
        self.assertEqual(expected_labels, f.labels)

        output_file.close()
        ref_file.close()
        os.remove(output_file_name)

    def test_replace_labels(self):
        """
        Test method for replace_labels.
        """
        input_file_name = "test_files/test_replace_labels.asm"
        output_file_name = "test_files/output_replace_labels.asm"
        ref_file_name = "test_files/ref_test_replace_labels.asm"

        f = Format(input_file_name)
        f.number()
        f.remove_comments()
        f.remove_blanks()
        f.find_labels()
        f.replace_labels()
        f.write_file(output_file_name)

        output_file = open(output_file_name)
        ref_file = open(ref_file_name)
        self.assertEqual(ref_file.read(), output_file.read())

        output_file.close()
        ref_file.close()
        os.remove(output_file_name)

    def test_rectify_numbers(self):
        """
        Test method for rectify_numbers
        """
        input_file_name = "test_files/test_replace_labels.asm"
        output_file_name = "test_files/output_rectify_numbers.asm"
        ref_file_name = "test_files/ref_test_rectify_numbers.asm"

        f = Format(input_file_name)
        f.number()
        f.remove_comments()
        f.remove_blanks()
        f.find_labels()
        f.replace_labels()
        f.rectify_numbers()
        f.write_file(output_file_name)

        output_file = open(output_file_name)
        ref_file = open(ref_file_name)
        self.assertEqual(ref_file.read(), output_file.read())

        output_file.close()
        ref_file.close()
        os.remove(output_file_name)


if __name__ == '__main__':
    unittest.main()
