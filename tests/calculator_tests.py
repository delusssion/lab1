import sys

sys.path.insert(0, '/Users/delusionn/prog/labs/lab1')

from src.main import CalcError, Calculator
import unittest

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_operations(self):
        self.assertEqual(self.calc.calculate('2 + 3'), 5)
        self.assertEqual(self.calc.calculate('7 - 3'), 4)
        self.assertEqual(self.calc.calculate('2 * 3'), 6)
        self.assertEqual(self.calc.calculate('2 ** 3'), 8)
        self.assertEqual(self.calc.calculate('9 / 3'), 3)
        self.assertEqual(self.calc.calculate('10 % 3'), 1)
        self.assertEqual(self.calc.calculate('13 // 4'), 3)

    def test_float_numbers(self):
        self.assertEqual(self.calc.calculate('2.5 + 3.5'), 6)
        self.assertEqual(self.calc.calculate('2.1 + 5.5'), 7.6)
        self.assertEqual(self.calc.calculate('10.0 * 3.1'), 31)
        self.assertEqual(self.calc.calculate('10.0 / 4.0'), 2.5)

    def test_operations_priority(self):
        self.assertEqual(self.calc.calculate('2 + 3 * 4'), 14)
        self.assertEqual(self.calc.calculate('(2 + 3) * 4'), 20)
        self.assertEqual(self.calc.calculate('10 - 2 ** 3'), 2)
        self.assertEqual(self.calc.calculate('2 * 3 + 4 * 5 - 20 / 4'), 21)
        self.assertEqual(self.calc.calculate('10 // 3 ** 2'), 1)
        self.assertEqual(self.calc.calculate('(10 // 3) ** 2'), 9)

    def test_integer_operations(self):
        self.assertEqual(self.calc.calculate('10 // 3'), 3)
        self.assertEqual(self.calc.calculate('10 % 3'), 1)
        self.assertEqual(self.calc.calculate('15 // 2'), 7)
        self.assertEqual(self.calc.calculate('15 % 2'), 1)

    def test_unary_operations(self):
        self.assertEqual(self.calc.calculate('-2'), -2)
        self.assertEqual(self.calc.calculate('+15'), 15)
        self.assertEqual(self.calc.calculate('-3 + 5'), 2)
        self.assertEqual(self.calc.calculate('5 + -3'), 2)
        self.assertEqual(self.calc.calculate('5 - +3'), 2)
        self.assertEqual(self.calc.calculate('+5 * +3'), 15)
        self.assertEqual(self.calc.calculate('-10 * -5'), 50)


    def test_complex_expressions(self):
        self.assertEqual(self.calc.calculate('(5 - 3 * (7 - (2 + 2)) - 1)'), -5)
        self.assertEqual(self.calc.calculate('(8 - 3) * (2 + 2) - (2 * (1 + 2))'), 14)
        self.assertEqual(self.calc.calculate('(10 - 2) ** (3 - 1)'), 64)
        self.assertEqual(self.calc.calculate('(15 % 4) + 2.5 - (7 - 2 + (3 * 4))'), -11.5)

    def test_degree_priority(self):
        self.assertEqual(self.calc.calculate('2 ** 3 ** 2'), 512)
        self.assertEqual(self.calc.calculate('(2 ** 3) ** 2'), 64)

    def test_expr_with_spaces(self):
        self.assertEqual(self.calc.calculate('   2  + 3  '), 5)
        self.assertEqual(self.calc.calculate('-    10   +    -    3'), -13)
        self.assertEqual(self.calc.calculate('      (2 ** 3      )    -  1'), 7)

    def test_incorrect_numbers(self):
        with self.assertRaises(CalcError):
            self.calc.calculate('011')
        with self.assertRaises(CalcError):
            self.calc.calculate('.91')
        with self.assertRaises(CalcError):
            self.calc.calculate('22.')
        with self.assertRaises(CalcError):
            self.calc.calculate('1..1')
        with self.assertRaises(CalcError):
            self.calc.calculate('1.1.1')
        with self.assertRaises(CalcError):
            self.calc.calculate('--2')

    def test_division_by_zero(self):
        with self.assertRaises(CalcError):
            self.calc.calculate('10 / 0')
        with self.assertRaises(CalcError):
            self.calc.calculate('10 // 0')
        with self.assertRaises(CalcError):
            self.calc.calculate('10 % 0')

    def test_integer_operations_with_float_nums(self):
        with self.assertRaises(CalcError):
            self.calc.calculate('10.1 // 2')
        with self.assertRaises(CalcError):
            self.calc.calculate('10 // 2.1')
        with self.assertRaises(CalcError):
            self.calc.calculate('11.4 % 4')
        with self.assertRaises(CalcError):
            self.calc.calculate('10 % 2.5')

    def test_incorrect_syntex(self):
        with self.assertRaises(CalcError):
            self.calc.calculate('10 +')
        with self.assertRaises(CalcError):
            self.calc.calculate('2 3')
        with self.assertRaises(CalcError):
            self.calc.calculate('2 * e')
        with self.assertRaises(CalcError):
            self.calc.calculate('10 $ 3')

    def test_incorrect_brackets(self):
        with self.assertRaises(CalcError):
            self.calc.calculate('(2 - 1')
        with self.assertRaises(CalcError):
            self.calc.calculate('2 - 1)')
        with self.assertRaises(CalcError):
            self.calc.calculate('((2 - 1)')
        with self.assertRaises(CalcError):
            self.calc.calculate('()')

if __name__ == '__main__':
    unittest.main()
