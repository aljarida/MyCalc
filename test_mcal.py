import sys
import unittest
import math
import mcal
from io import StringIO

class McalTester(unittest.TestCase):
    def setUp(self):
        # Capturing stdout and stderr for testing printed output
        self.saved_stdout = sys.stdout 
        self.saved_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        # Restore stdout and stderr after tests are done
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr

    def set_sys_argv(self, string):
        args = ["./mcal"] + string.split(" ")
        sys.argv = args

    def mcal_result_for(self, string, to_float=True):
        self.set_sys_argv(string)
        mcal.main()
        result = sys.stdout.getvalue()
        if to_float:
            return float(result)
        else:
            return result

class CLITester(McalTester):
    def test_pi(self):
        result = self.mcal_result_for("PI")
        self.assertEqual(result, math.pi)

    def test_e(self):
        result = self.mcal_result_for("E")
        self.assertEqual(result, math.e)

    def test_caret(self):
        result = self.mcal_result_for("2^10")
        self.assertEqual(result, 2**10)

    def test_X(self):
        result = self.mcal_result_for("1280X720")
        self.assertEqual(result, 1280*720)

    def test_many_arguments(self):
        sys.argv = ["./mcal", "(5+5", "(10)", ")", "/5"]
        mcal.main()
        result = sys.stdout.getvalue()
        self.assertEqual(result, "11.0\n")

class FunctionsTester(unittest.TestCase):
    def test_replace_with_dict(self):
        result = mcal.replace_with_dict("123454321", {"1": "Yes", "3": "No"})
        self.assertEqual(result, "Yes2No454No2Yes")

    def test_make_implicit_multiplication_explicit(self):
        result = mcal.make_implicit_multiplication_explicit("(4)5 - 5(3)(2)1")
        self.assertEqual(result, "(4)*5 - 5*(3)*(2)*1")
    
    def test_advance_to_function_end(self):
        result = mcal.advance_to_function_end("log(5)", 0)
        self.assertEqual(result, 3)

        result = mcal.advance_to_function_end("long_function_name(log(5)))", 0)
        self.assertEqual(result, 18)
    
        with self.assertRaises(Exception):
            result = mcal.advance_to_function_end("Log(5)", 0)

        with self.assertRaises(Exception):
            result = mcal.advance_to_function_end("log5)", 0)

    def test_advance_to_closed_parenthesis(self):
        result = mcal.advance_to_closed_parenthesis("((()4567)9)+10", 0)
        self.assertEqual(result, 10)

        result = mcal.advance_to_closed_parenthesis("01(3(5)78)", 2)
        self.assertEqual(result, 9)

        with self.assertRaises(Exception):
            result = mcal.advance_to_closed_parenthesis(")", 0)

        with self.assertRaises(Exception):
            result = mcal.advance_to_closed_parenthesis("(()", 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
