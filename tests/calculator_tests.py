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
        assert self.calc.evaluate('0 - 0') == 0.0
        assert self.calc.evaluate('-5 - 10') == -15.0

    def test_multiplication(self):
        assert self.calc.evaluate('2 * 3') == 6.0
        assert self.calc.evaluate('10 * 0') == 0.0
        assert self.calc.evaluate('-5 * 4') == -20.0
        assert self.calc.evaluate('2.5 * 4') == 10.0

    def test_division(self):
        assert self.calc.evaluate('6 / 2') == 3.0
        assert self.calc.evaluate('10 / 4') == 2.5
        assert self.calc.evaluate('0 / 5') == 0.0
        assert self.calc.evaluate('-10 / 2') == -5.0

    def test_integer_division(self):
        assert self.calc.evaluate('7 // 2') == 3.0
        assert self.calc.evaluate('10 // 3') == 3.0
        assert self.calc.evaluate('-7 // 2') == -4.0

    def test_modulo(self):
        assert self.calc.evaluate('7 % 3') == 1.0
        assert self.calc.evaluate('10 % 5') == 0.0
        assert self.calc.evaluate('8 % 3') == 2.0

    def test_power(self):
        assert self.calc.evaluate('2 ** 3') == 8.0
        assert self.calc.evaluate('5 ** 2') == 25.0
        assert self.calc.evaluate('10 ** 0') == 1.0
        assert self.calc.evaluate('2 ** -1') == 0.5

    # Комплексные выражения
    def test_complex_expressions(self):
        assert self.calc.evaluate('2 + 3 * 4') == 14.0
        assert self.calc.evaluate('(2 + 3) * 4') == 20.0
        assert self.calc.evaluate('10 - 2 * 3 + 4') == 8.0
        assert self.calc.evaluate('2 * 3 + 4 * 5') == 26.0

    def test_nested_parentheses(self):
        assert self.calc.evaluate('((2 + 3) * 4)') == 20.0
        assert self.calc.evaluate('(2 * (3 + 4))') == 14.0
        assert self.calc.evaluate('((1 + 2) * (3 + 4))') == 21.0

    def test_unary_operators(self):
        assert self.calc.evaluate('+5') == 5.0
        assert self.calc.evaluate('-5') == -5.0
        assert self.calc.evaluate('--5') == 5.0
        assert self.calc.evaluate('+-5') == -5.0
        assert self.calc.evaluate('-+5') == -5.0
        assert self.calc.evaluate('++5') == 5.0
        assert self.calc.evaluate('++--++-+++--5') == -5.0

    def test_unary_with_binary(self):
        assert self.calc.evaluate('5 + -3') == 2.0
        assert self.calc.evaluate('10 * -2') == -20.0
        assert self.calc.evaluate('-5 * -4') == 20.0
        assert self.calc.evaluate('10 / -2') == -5.0

    def test_floats(self):
        assert self.calc.evaluate('2.5 + 3.5') == 6.0
        assert self.calc.evaluate('0.1 + 0.2') == 0.3
        assert self.calc.evaluate('3.14 * 2') == 6.28
        assert self.calc.evaluate('10.5 / 2') == 5.25

    def test_operator_precedence(self):
        assert self.calc.evaluate('2 + 3 * 4') == 14.0
        assert self.calc.evaluate('2 * 3 + 4') == 10.0
        assert self.calc.evaluate('2 + 3 ** 2') == 11.0
        assert self.calc.evaluate('2 * 3 ** 2') == 18.0

    def test_no_spaces(self):
        assert self.calc.evaluate('2+3') == 5.0
        assert self.calc.evaluate('(2+3)*4') == 20.0
        assert self.calc.evaluate('2*3+4*5') == 26.0

    def test_with_spaces(self):
        assert self.calc.evaluate('  2  +  3  ') == 5.0
        assert self.calc.evaluate('( 2 + 3 ) * 4 ') == 20.0
        assert self.calc.evaluate(' 2 * 3 + 4 * 5 ') == 26.0

    def test_mixed_operations(self):
        assert self.calc.evaluate('2 + 3 * 4 - 5 / 2') == 11.5
        assert self.calc.evaluate('(2 + 3) * (4 - 1)') == 15.0
        assert self.calc.evaluate('2 ** 3 + 4 * 5') == 28.0
        assert self.calc.evaluate('10 % 3 + 7 // 2') == 4.0

    def test_edge_cases(self):
        assert self.calc.evaluate('0') == 0.0
        assert self.calc.evaluate('1') == 1.0
        assert self.calc.evaluate('0.00000000001') == 0.0
