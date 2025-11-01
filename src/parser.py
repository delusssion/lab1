class Parser:
    """Парсер и вычислитель выражений (рекурсивный спуск) с полной проверкой структуры"""

    def parse_expression(self, tokens: list[str]) -> float:
        """Вход - список токенов"""
        if not tokens:
            raise ValueError('Пустое выражение')
        result = self._parse_addition(tokens)
        return result

    def _parse_addition(self, tokens: list[str]) -> float:
        """Обработка сложения и вычитания"""
        result = self._parse_multiplication(tokens)

        while tokens and tokens[0] in {'+', '-'}:
            operator = tokens.pop(0)
            if not tokens:
                raise ValueError('Ожидался операнд')
            right = self._parse_multiplication(tokens)
            result = result + right if operator == '+' else result - right

        return result

    def _parse_multiplication(self, tokens: list[str]) -> float:
        """Обработка умножения и деления"""
        result = self._parse_power(tokens)

        while tokens and tokens[0] in {'*', '/', '//', '%'}:
            operator = tokens.pop(0)
            if not tokens:
                raise ValueError('Ожидался операнд')
            right = self._parse_power(tokens)

            if operator == '*':
                result *= right
            elif operator == '/':
                if right == 0:
                    raise ZeroDivisionError('Деление на ноль')
                result /= right
            elif operator == '//':
                if not self._is_integer(result) or not self._is_integer(right):
                    raise ValueError('Целочисленное деление только для целых чисел')
                if right == 0:
                    raise ZeroDivisionError('Деление на ноль')
                result = int(result) // int(right)
            else:  # %
                if not self._is_integer(result) or not self._is_integer(right):
                    raise ValueError('Операция % только для целых чисел')
                if right == 0:
                    raise ZeroDivisionError('Деление на ноль')
                result = int(result) % int(right)

        return result

    def _parse_power(self, tokens: list[str]) -> float:
        """Обработка возведения в степень (правоассоциативная)"""
        result = self._parse_unary(tokens)

        if tokens and tokens[0] == '**':
            tokens.pop(0)
            if not tokens:
                raise ValueError('Ожидался операнд')
            right = self._parse_power(tokens)
            try:
                result = result ** right
            except OverflowError:
                raise OverflowError('Слишком большое число')

        return result

    def _parse_unary(self, tokens: list[str]) -> float:
        """Обработка унарных операторов"""
        sign = 1
        while tokens and tokens[0] in {'+', '-'}:
            if tokens.pop(0) == '-':
                sign = -sign

        result = self._parse_primary(tokens)
        return sign * result

    def _parse_primary(self, tokens: list[str]) -> float:
        """Обработка чисел и скобок"""
        if not tokens:
            raise ValueError('Ожидался операнд')

        token = tokens.pop(0)

        if token == '(':
            if not tokens:
                raise ValueError('Пустые скобки')
            if tokens[0] == ')':
                raise ValueError('Пустые скобки')

            result = self._parse_addition(tokens)
            if not tokens or tokens.pop(0) != ')':
                raise ValueError('Непарные скобки')
            return result

        if self._is_number(token):
            self._validate_number_format(token)
            if tokens and self._is_number(tokens[0]):
                raise ValueError('Пропущен оператор')

        try:
            return float(token)
        except ValueError:
            raise ValueError('Некорректный токен')

    def _validate_number_format(self, token: str):
        """Проверка формата числа (перенесено из токенизатора)"""
        if len(token) > 1 and token[0] == '0' and token[1] != '.':
            raise ValueError('Число не может начинаться с нуля')
        if token.startswith('.') or token.endswith('.'):
            raise ValueError('Некорректный формат числа')
        if token.count('.') > 1:
            raise ValueError('Некорректный формат числа')

    @staticmethod
    def _is_integer(number: float) -> bool:
        """Проверяет, является ли число целым"""
        return isinstance(number, int) or float(number).is_integer()

    @staticmethod
    def _is_number(token: str) -> bool:
        """Проверяет, является ли токен числом"""
        try:
            float(token)
            return True
        except ValueError:
            return False
