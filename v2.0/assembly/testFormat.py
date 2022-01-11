import unittest
from format import Format


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

    def test_number(self):
        """
        Test method for the number method.
        """
        f = Format("test_files/test_asm.asm")
        f.number()
        for line in f.lines:
            self.assertEqual(int(line[0]), f.lines.index(line))



if __name__ == '__main__':
    unittest.main()
