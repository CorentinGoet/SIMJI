import unittest
from translation import Translation


class TestTranslation(unittest.TestCase):
    """
    @author Corentin Goetghebeur
    Unit test class for the Translation class
    """

    def setUp(self):
        # These instructions are executed before each test.
        pass

    def test_get_op(self):
        """
        Test method for get_op.
        """
        t = Translation("test_files/test_get_op.asm")
        for line in t.lines:
            self.assertEqual(t.get_op(line), t.lines.index(line))

    def test_get_params(self):
        """
        Test method for get_params.
        """
        t = Translation("test_files/test_get_params.asm")
        expected_params = [{}, {'r1': 'r1', 'o': '1', 'r2': 'r2'}, {'r1': 'r1', 'o': '-7', 'r2': 'r10'},
                           {'o': '15', 'r': 'r5'}, {'r': 'r0', 'a': '9'}, {'n': '0'}]
        for i in range(len(t.lines)):
            self.assertEquals(t.get_params(t.lines[i]), expected_params[i])

    def test_encode(self):
        """
        Test method for encode, format_param, write_hex.
        """
        t = Translation("test_files/test_get_params.asm")
        for line in t.lines:
            t.hexlines.append(t.encode(line))
        print(t.hexlines)
        t.write_hex("test_files/output_test_encode.asm")

        output_file = open("test_files/output_test_encode.asm")
        ref_file = open("test_files/ref_test_encode.asm")
        self.assertEqual(output_file.read(), ref_file.read())

        output_file.close()
        ref_file.close()


if __name__ == '__main__':
    unittest.main()
