import pytest
from src.main import Calculator


class TestCalculatorErrors:
    def setup_method(self):
        self.calc = Calculator()

    def test_tokenization_errors(self):
        with pytest.raises(ValueError, match='Пустое выражение'):
            self.calc.evaluate('')
        with pytest.raises(ValueError, match='Пустое выражение'):
            self.calc.evaluate('   ')

        with pytest.raises(ValueError, match='Некорректный символ'):
            self.calc.evaluate('2 + a')
        with pytest.raises(ValueError, match='Некорректный символ'):
            self.calc.evaluate('2 @ 3')

        with pytest.raises(ValueError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 3')
        with pytest.raises(ValueError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 3 + 4')

        with pytest.raises(ValueError, match='Выражение не может начинаться с оператора'):
            self.calc.evaluate('* 2 + 3')
        with pytest.raises(ValueError, match='Выражение не может начинаться с оператора'):
            self.calc.evaluate('/ 5')

    def test_number_format_errors(self):
        with pytest.raises(ValueError, match='Число не может начинаться с нуля'):
            self.calc.evaluate('012 + 3')
        with pytest.raises(ValueError, match='Некорректный формат числа'):
            self.calc.evaluate('2. + 3')
        with pytest.raises(ValueError, match='Некорректный формат числа'):
            self.calc.evaluate('2.3.4 + 5')
        with pytest.raises(ValueError, match='Некорректный формат числа'):
            self.calc.evaluate('2..3 + 4')

    def test_parentheses_errors(self):
        with pytest.raises(ValueError, match='Непарные скобки'):
            self.calc.evaluate('(2 + 3')
        with pytest.raises(ValueError, match='Неправильный порядок скобок'):
            self.calc.evaluate('2 + 3)')
        with pytest.raises(ValueError, match='Пустые скобки недопустимы'):
            self.calc.evaluate('()')
        with pytest.raises(ValueError, match='Пустые скобки недопустимы'):
            self.calc.evaluate('2 + ()')
        with pytest.raises(ValueError, match='Пропущен оператор после закрывающей скобки'):
            self.calc.evaluate('(2+3)4')

    def test_operator_sequence_and_missing_operand(self):
        with pytest.raises(ValueError, match='Недопустимая последовательность операторов'):
            self.calc.evaluate('2 + * 3')
        with pytest.raises(ValueError, match='Недопустимая последовательность операторов'):
            self.calc.evaluate('2 * / 3')
        with pytest.raises(ValueError, match='После открывающей скобки не может быть оператора'):
            self.calc.evaluate('(* 2 + 3)')
        with pytest.raises(ValueError, match='Ожидался операнд после оператора'):
            self.calc.evaluate('2 +')
        with pytest.raises(ValueError, match='Ожидался операнд после оператора'):
            self.calc.evaluate('2 * 3 +')

    def test_division_and_integer_operations(self):
        with pytest.raises(ValueError, match='Деление на ноль'):
            self.calc.evaluate('5 / 0')
        with pytest.raises(ValueError, match='Деление на ноль'):
            self.calc.evaluate('10 // 0')
        with pytest.raises(ValueError, match='Деление на ноль'):
            self.calc.evaluate('5 % 0')
        with pytest.raises(ValueError, match='Целочисленное деление только для целых чисел'):
            self.calc.evaluate('5.5 // 2')
        with pytest.raises(ValueError, match='Операция % только для целых чисел'):
            self.calc.evaluate('5.5 % 2')

    def test_overflow(self):
        with pytest.raises(ValueError, match='Результат слишком велик'):
            self.calc.evaluate('10 ** 1000')
        with pytest.raises(ValueError, match='Результат слишком велик'):
            self.calc.evaluate('2 ** 1024')

    def test_recursion_and_parser_errors(self):
        deep_expr = '(' * 1000 + '1' + ')' * 1000
        with pytest.raises(ValueError, match='Слишком сложное выражение'):
            self.calc.evaluate(deep_expr)
        with pytest.raises(ValueError, match='Некорректный символ'):
            self.calc.evaluate('abc')
        with pytest.raises(ValueError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 + 3 4')
