import pytest
from src.main import Calculator


class TestCalculator:

    def setup_method(self):
        self.calc = Calculator()

    def test_addition(self):
        assert self.calc.evaluate('2 + 3') == 5.0
        assert self.calc.evaluate('10 + 20') == 30.0
        assert self.calc.evaluate('0 + 0') == 0.0
        assert self.calc.evaluate('-5 + 10') == 5.0

    def test_subtraction(self):
        assert self.calc.evaluate('5 - 3') == 2.0
        assert self.calc.evaluate('10 - 20') == -10.0
        assert self.calc.evaluate('0 - 5') == -5.0
        assert self.calc.evaluate('-5 - 3') == -8.0

    def test_multiplication(self):
        assert self.calc.evaluate('2 * 3') == 6.0
        assert self.calc.evaluate('10 * 5') == 50.0
        assert self.calc.evaluate('0 * 100') == 0.0
        assert self.calc.evaluate('-5 * 3') == -15.0

    def test_division(self):
        assert self.calc.evaluate('6 / 2') == 3.0
        assert self.calc.evaluate('10 / 4') == 2.5
        assert self.calc.evaluate('5 / 2') == 2.5
        assert self.calc.evaluate('-10 / 2') == -5.0

    def test_combined_operations(self):
        assert self.calc.evaluate('2 + 3 + 4') == 9.0
        assert self.calc.evaluate('10 - 5 - 2') == 3.0
        assert self.calc.evaluate('2 * 3 * 4') == 24.0

    def test_mult_before_add(self):
        assert self.calc.evaluate('2 + 3 * 4') == 14.0
        assert self.calc.evaluate('3 * 4 + 2') == 14.0
        assert self.calc.evaluate('2 + 3 * 4 + 5') == 19.0

    def test_mult_before_subtract(self):
        assert self.calc.evaluate('10 - 3 * 2') == 4.0
        assert self.calc.evaluate('3 * 2 - 10') == -4.0

    def test_power_before_mult(self):
        assert self.calc.evaluate('2 * 3 ** 2') == 18.0
        assert self.calc.evaluate('3 ** 2 * 2') == 18.0

    def test_power_before_add(self):
        assert self.calc.evaluate('2 + 3 ** 2') == 11.0
        assert self.calc.evaluate('2 ** 3 + 1') == 9.0

    def test_same_precedence_left_to_right(self):
        assert self.calc.evaluate('10 - 5 - 2') == 3.0
        assert self.calc.evaluate('20 / 4 / 2') == 2.5
        assert self.calc.evaluate('2 * 3 / 2') == 3.0

    def test_unary_minus(self):
        assert self.calc.evaluate('-5') == -5.0
        assert self.calc.evaluate('-0') == 0.0
        assert self.calc.evaluate('-(5)') == -5.0

    def test_unary_plus(self):
        assert self.calc.evaluate('+5') == 5.0
        assert self.calc.evaluate('+0') == 0.0
        assert self.calc.evaluate('+(5)') == 5.0

    def test_unary_minus_with_addition(self):
        assert self.calc.evaluate('5 + -3') == 2.0
        assert self.calc.evaluate('-5 + 3') == -2.0
        assert self.calc.evaluate('5 - -3') == 8.0

    def test_multiple_unary(self):
        assert self.calc.evaluate('--5') == 5.0
        assert self.calc.evaluate('---5') == -5.0
        assert self.calc.evaluate('-+5') == -5.0
        assert self.calc.evaluate('+-5') == -5.0

    def test_unary_in_parentheses(self):
        assert self.calc.evaluate('(-5)') == -5.0
        assert self.calc.evaluate('2 * (-3)') == -6.0
        assert self.calc.evaluate('(+5) + (-3)') == 2.0

    def test_simple_parentheses(self):
        assert self.calc.evaluate('(2 + 3)') == 5.0
        assert self.calc.evaluate('(10 - 4)') == 6.0
        assert self.calc.evaluate('(2 * 3)') == 6.0

    def test_parentheses_override_precedence(self):
        assert self.calc.evaluate('(2 + 3) * 4') == 20.0
        assert self.calc.evaluate('2 * (3 + 4)') == 14.0
        assert self.calc.evaluate('(10 - 5) * 2') == 10.0

    def test_nested_parentheses(self):
        assert self.calc.evaluate('((2 + 3))') == 5.0
        assert self.calc.evaluate('(2 + (3 * 4))') == 14.0
        assert self.calc.evaluate('((2 + 3) * (4 - 1))') == 15.0

    def test_multiple_groups(self):
        assert self.calc.evaluate('(2 + 3) * (4 + 5)') == 45.0
        assert self.calc.evaluate('(10 - 2) / (3 - 1)') == 4.0
        assert self.calc.evaluate('(2 * 3) + (4 * 5)') == 26.0

    def test_integer_division(self):
        assert self.calc.evaluate('10 // 3') == 3.0
        assert self.calc.evaluate('10 // 2') == 5.0
        assert self.calc.evaluate('-10 // 3') == -4.0
        assert self.calc.evaluate('7 // 2') == 3.0

    def test_modulo(self):
        assert self.calc.evaluate('10 % 3') == 1.0
        assert self.calc.evaluate('10 % 2') == 0.0
        assert self.calc.evaluate('7 % 3') == 1.0
        assert self.calc.evaluate('5 % 5') == 0.0

    def test_mixed_int_ops(self):
        assert self.calc.evaluate('10 // 2 + 3 % 2') == 6.0
        assert self.calc.evaluate('(10 // 3) * 2') == 6.0
        assert self.calc.evaluate('10 + 5 // 2') == 12.0

    def test_positive_exponent(self):
        assert self.calc.evaluate('2 ** 3') == 8.0
        assert self.calc.evaluate('5 ** 2') == 25.0
        assert self.calc.evaluate('10 ** 0') == 1.0
        assert self.calc.evaluate('1 ** 100') == 1.0

    def test_negative_exponent(self):
        assert self.calc.evaluate('2 ** -2') == 0.25
        assert self.calc.evaluate('10 ** -1') == 0.1
        assert self.calc.evaluate('5 ** -2') == 0.04

    def test_fractional_base(self):
        assert self.calc.evaluate('0.5 ** 2') == 0.25
        assert self.calc.evaluate('2.5 ** 2') == 6.25

    def test_right_associativity(self):
        assert self.calc.evaluate('2 ** 3 ** 2') == 512.0
        assert self.calc.evaluate('2 ** 2 ** 3') == 256.0

    def test_power_with_parentheses(self):
        assert self.calc.evaluate('(2 ** 3) ** 2') == 64.0
        assert self.calc.evaluate('2 ** (3 ** 2)') == 512.0

    def test_simple_decimals(self):
        assert self.calc.evaluate('2.5') == 2.5
        assert self.calc.evaluate('0.5') == 0.5
        assert self.calc.evaluate('3.14159') == 3.14159

    def test_arithmetic_with_decimals(self):
        assert self.calc.evaluate('2.5 + 1.5') == 4.0
        assert self.calc.evaluate('3.5 - 1.5') == 2.0
        assert self.calc.evaluate('2.5 * 2') == 5.0
        assert self.calc.evaluate('5 / 2') == 2.5

    def test_decimals_with_operators(self):
        assert self.calc.evaluate('2.5 ** 2') == 6.25
        assert self.calc.evaluate('0.1 * 10') == 1.0
        assert self.calc.evaluate('1.5 + 2.5 * 2') == 6.5

    def test_zero_operations(self):
        assert self.calc.evaluate('0 + 0') == 0.0
        assert self.calc.evaluate('0 - 0') == 0.0
        assert self.calc.evaluate('0 * 100') == 0.0
        assert self.calc.evaluate('0 / 5') == 0.0

    def test_large_numbers(self):
        assert self.calc.evaluate('1000000 + 1000000') == 2000000.0
        assert self.calc.evaluate('999999 * 999999') == 999998000001.0

    def test_result_rounding(self):
        result = self.calc.evaluate('1 / 3 + 2 / 3')
        assert result == 1.0

        result = self.calc.evaluate('0.1 + 0.2')
        assert abs(result - 0.3) < 1e-10

    def test_single_number(self):
        assert self.calc.evaluate('42') == 42.0
        assert self.calc.evaluate('3.14') == 3.14

    def test_complex_expression(self):
        assert self.calc.evaluate('(2 + 3) * (4 + 5) - 6 / 2') == 42.0
        assert self.calc.evaluate('2 ** 3 + 4 * 5 - 6 / 2') == 25.0
        assert self.calc.evaluate('10 / 2 / 5') == 1.0

    def test_no_spaces(self):
        assert self.calc.evaluate('2+3') == 5.0
        assert self.calc.evaluate('10*2-5') == 15.0

    def test_with_spaces(self):
        assert self.calc.evaluate('2 + 3') == 5.0
        assert self.calc.evaluate('10 * 2 - 5') == 15.0

    def test_excess_spaces(self):
        assert self.calc.evaluate('2  +  3') == 5.0
        assert self.calc.evaluate('  10  *  2  ') == 20.0
