import pytest
from src.main import Calculator


class TestCalculatorErrors:
    """Тесты всех сценариев ошибок калькулятора"""

    def setup_method(self):
        self.calculator = Calculator()

    def test_empty_expression(self):
        """Пустое выражение"""
        with pytest.raises(ValueError, match='Пустое выражение'):
            self.calculator.evaluate('')
        with pytest.raises(ValueError, match='Пустое выражение'):
            self.calculator.evaluate('   ')

    def test_invalid_tokens(self):
        """Некорректные токены"""
        with pytest.raises(ValueError, match='Некорректный токен'):
            self.calculator.evaluate('2 + a')
        with pytest.raises(ValueError, match='Некорректный токен'):
            self.calculator.evaluate('3 @ 4')
        with pytest.raises(ValueError, match='Некорректный токен'):
            self.calculator.evaluate('5 & 6')
        with pytest.raises(ValueError, match='Некорректный '):
            self.calculator.evaluate('.')

    def test_unpaired_brackets(self):
        """Непарные скобки"""
        with pytest.raises(ValueError, match='Непарные скобки'):
            self.calculator.evaluate('(2 + 3')
        with pytest.raises(ValueError, match='Непарные скобки'):
            self.calculator.evaluate('2 + 3)')
        with pytest.raises(ValueError, match='Непарные скобки'):
            self.calculator.evaluate('((2 + 3)')

    def test_empty_brackets(self):
        """Пустые скобки"""
        with pytest.raises(ValueError, match='Пустые скобки'):
            self.calculator.evaluate('()')
        with pytest.raises(ValueError, match='Пустые скобки'):
            self.calculator.evaluate('() + 2')
        with pytest.raises(ValueError, match='Пустые скобки'):
            self.calculator.evaluate('3 + ()')

    def test_missing_operand_after_operator(self):
        """Ожидался операнд после оператора"""
        with pytest.raises(ValueError, match='Ожидался операнд'):
            self.calculator.evaluate('2 +')
        with pytest.raises(ValueError, match='Ожидался операнд'):
            self.calculator.evaluate('+')
        with pytest.raises(ValueError, match='Ожидался операнд'):
            self.calculator.evaluate('3 *')
        with pytest.raises(ValueError, match='Ожидался операнд'):
            self.calculator.evaluate('2 **')

    def test_missing_operator_between_numbers(self):
        """Пропущен оператор между числами"""
        with pytest.raises(ValueError, match='Пропущен оператор'):
            self.calculator.evaluate('2 3')
        with pytest.raises(ValueError, match='Пропущен оператор'):
            self.calculator.evaluate('2 (3 + 4)')
        with pytest.raises(ValueError, match='Пропущен оператор'):
            self.calculator.evaluate('(2 + 3) 4')

    def test_operator_at_start(self):
        """Оператор в начале выражения"""
        with pytest.raises(ValueError, match='Оператор не может быть в начале выражения'):
            self.calculator.evaluate('* 2')
        with pytest.raises(ValueError, match='Оператор не может быть в начале выражения'):
            self.calculator.evaluate('/ 3')
        with pytest.raises(ValueError, match='Оператор не может быть в начале выражения'):
            self.calculator.evaluate('** 2')

    def test_operator_after_open_bracket(self):
        """Оператор после открывающей скобки"""
        with pytest.raises(ValueError, match='После открывающей скобки не может быть оператора'):
            self.calculator.evaluate('( * 2 )')
        with pytest.raises(ValueError, match='После открывающей скобки не может быть оператора'):
            self.calculator.evaluate('( / 3 + 2 )')

    def test_invalid_number_format(self):
        """Некорректный формат чисел"""
        with pytest.raises(ValueError, match='Число не может начинаться с нуля'):
            self.calculator.evaluate('012')
        with pytest.raises(ValueError, match='Число не может начинаться с нуля'):
            self.calculator.evaluate('00.5')

        with pytest.raises(ValueError, match='Некорректный токен'):
            self.calculator.evaluate('2..3')
        with pytest.raises(ValueError, match='Некорректный формат числа'):
            self.calculator.evaluate('5.')

    def test_division_by_zero(self):
        """Деление на ноль"""
        with pytest.raises(ZeroDivisionError, match='Деление на ноль'):
            self.calculator.evaluate('5 / 0')
        with pytest.raises(ZeroDivisionError, match='Деление на ноль'):
            self.calculator.evaluate('10 // 0')
        with pytest.raises(ZeroDivisionError, match='Деление на ноль'):
            self.calculator.evaluate('8 % 0')

    def test_integer_division_and_modulo_errors(self):
        """Ошибки целочисленного деления и modulo"""
        with pytest.raises(ValueError, match='Целочисленное деление только для целых чисел'):
            self.calculator.evaluate('5.5 // 2')
        with pytest.raises(ValueError, match='Целочисленное деление только для целых чисел'):
            self.calculator.evaluate('5 // 2.5')

        with pytest.raises(ValueError, match='Операция % только для целых чисел'):
            self.calculator.evaluate('5.5 % 2')
        with pytest.raises(ValueError, match='Операция % только для целых чисел'):
            self.calculator.evaluate('5 % 2.5')

    def test_overflow_error(self):
        """Слишком большое число"""
        with pytest.raises(OverflowError, match='Слишком большое число'):
            self.calculator.evaluate('1000 ** 1000')
