import pytest
from src.main import Calculator
from src.tokenizer import CalcError


class TestCalculatorErrors:
    def setup_method(self):
        self.calc = Calculator()

    def test_tokenization_errors(self):
        with pytest.raises(CalcError, match='Пустое выражение'):
            self.calc.evaluate('')
        with pytest.raises(CalcError, match='Пустое выражение'):
            self.calc.evaluate('   ')

        with pytest.raises(CalcError, match='Некорректный символ'):
            self.calc.evaluate('2 + a')
        with pytest.raises(CalcError, match='Некорректный символ'):
            self.calc.evaluate('2 @ 3')

        with pytest.raises(CalcError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 3')
        with pytest.raises(CalcError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 3 + 4')

        with pytest.raises(CalcError, match='Выражение не может начинаться с оператора'):
            self.calc.evaluate('* 2 + 3')
        with pytest.raises(CalcError, match='Выражение не может начинаться с оператора'):
            self.calc.evaluate('/ 5')

    def test_number_format_errors(self):
        with pytest.raises(CalcError, match='Число не может начинаться с нуля'):
            self.calc.evaluate('012 + 3')
        with pytest.raises(CalcError, match='Некорректный формат числа'):
            self.calc.evaluate('2. + 3')
        with pytest.raises(CalcError, match='Некорректный формат числа'):
            self.calc.evaluate('2.3.4 + 5')
        with pytest.raises(CalcError, match='Некорректный формат числа'):
            self.calc.evaluate('2..3 + 4')

    def test_parentheses_errors(self):
        with pytest.raises(CalcError, match='Непарные скобки'):
            self.calc.evaluate('(2 + 3')
        with pytest.raises(CalcError, match='Неправильный порядок скобок'):
            self.calc.evaluate('2 + 3)')
        with pytest.raises(CalcError, match='Пустые скобки недопустимы'):
            self.calc.evaluate('()')
        with pytest.raises(CalcError, match='Пустые скобки недопустимы'):
            self.calc.evaluate('2 + ()')
        with pytest.raises(CalcError, match='Пропущен оператор после закрывающей скобки'):
            self.calc.evaluate('(2+3)4')

    def test_operator_sequence_and_missing_operand(self):
        with pytest.raises(CalcError, match='Недопустимая последовательность операторов'):
            self.calc.evaluate('2 + * 3')
        with pytest.raises(CalcError, match='Недопустимая последовательность операторов'):
            self.calc.evaluate('2 * / 3')
        with pytest.raises(CalcError, match='После открывающей скобки не может быть оператора'):
            self.calc.evaluate('(* 2 + 3)')
        with pytest.raises(CalcError, match='Ожидался операнд после оператора'):
            self.calc.evaluate('2 +')
        with pytest.raises(CalcError, match='Ожидался операнд после оператора'):
            self.calc.evaluate('2 * 3 +')

    def test_division_and_integer_operations(self):
        with pytest.raises(CalcError, match='Деление на ноль'):
            self.calc.evaluate('5 / 0')
        with pytest.raises(CalcError, match='Деление на ноль'):
            self.calc.evaluate('10 // 0')
        with pytest.raises(CalcError, match='Деление на ноль'):
            self.calc.evaluate('5 % 0')

        with pytest.raises(CalcError, match='Целочисленное деление только для целых чисел'):
            self.calc.evaluate('5.5 // 2')
        with pytest.raises(CalcError, match='Операция % только для целых чисел'):
            self.calc.evaluate('5.5 % 2')

    def test_overflow(self):
        with pytest.raises(CalcError, match='Результат слишком велик'):
            self.calc.evaluate('10 ** 1000')

    def test_recursion_and_parser_errors(self):
        with pytest.raises(CalcError, match='Слишком сложное выражение'):
            self.calc.evaluate('(' * 1000 + '1' + ')' * 1000)
        with pytest.raises(CalcError, match='Некорректный символ'):
            self.calc.evaluate('abc')
        with pytest.raises(CalcError, match='Пропущен оператор между числами'):
            self.calc.evaluate('2 + 3 4')
