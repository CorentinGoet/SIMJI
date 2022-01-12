import unittest
from format import Format
import os

class TestFormat(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
