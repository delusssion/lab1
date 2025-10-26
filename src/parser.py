class Parser:
    """Парсер и вычислитель выражений (рекурсивный спуск)"""

    def parse_expression(self, tokens: list[str]) -> float:
        """Вход - список токенов"""
        return self.parse_addition(tokens)

    def parse_addition(self, tokens: list[str]) -> float:
        """Обработка сложения и вычитания"""
        result = self.parse_multiplication(tokens)
        while tokens and tokens[0] in {'+', '-'}:
            operator = tokens.pop(0)
            if tokens and tokens[0] in {'+', '-'}:
                right = self.parse_unary(tokens)
            else:
                right = self.parse_multiplication(tokens)
            result = result + right if operator == '+' else result - right
        return result

    def parse_multiplication(self, tokens: list[str]) -> float:
        """Обработка умножения и деления"""
        result = self.parse_power(tokens)
        while tokens and tokens[0] in {'*', '/', '//', '%'}:
            operator = tokens.pop(0)
            if tokens and tokens[0] in {'+', '-'}:
                right = self.parse_unary(tokens)
            else:
                right = self.parse_power(tokens)
            if operator == '*':
                result *= right
            elif operator == '/':
                if right == 0:
                    raise ZeroDivisionError()
                result /= right
            elif operator == '//':
                if not self.is_integer(result) or not self.is_integer(right):
                    raise ValueError('Целочисленное деление только для целых чисел')
                if right == 0:
                    raise ZeroDivisionError()
                result //= right
            else:
                if not self.is_integer(result) or not self.is_integer(right):
                    raise ValueError('Операция % только для целых чисел')
                if right == 0:
                    raise ZeroDivisionError()
                result %= right
        return result

    def parse_power(self, tokens: list[str]) -> float:
        """Обработка возведения в степень"""
        result = self.parse_unary(tokens)
        if tokens and tokens[0] == '**':
            tokens.pop(0)
            right = self.parse_power(tokens)
            try:
                result = result ** right
            except OverflowError:
                raise ValueError('Результат слишком велик')
        return result

    def parse_unary(self, tokens: list[str]) -> float:
        """Обработка унарных операторов"""
        sign = 1
        while tokens and tokens[0] in {'+', '-'}:
            if tokens.pop(0) == '-':
                sign = -sign
        return sign * self.parse_primary(tokens)

    def parse_primary(self, tokens: list[str]) -> float:
        """Обработка чисел и скобок"""
        token = tokens.pop(0)
        if token == '(':
            if tokens[0] == ')':
                raise ValueError('Пустые скобки недопустимы')
            result = self.parse_expression(tokens)
            tokens.pop(0)
            return result
        try:
            return float(token)
        except ValueError:
            raise ValueError('Некорректное число')

    @staticmethod
    def is_integer(number: float) -> bool:
        """Проверяет, является ли число целым"""
        return float(number).is_integer()
