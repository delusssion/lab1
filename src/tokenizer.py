import re

class Tokenizer:
    """Разделяет выражение на токены с базовой проверкой структуры"""

    def __init__(self):
        self.operators = {'+', '-', '*', '/', '//', '%', '**'}
        self.binary_only = {'*', '/', '//', '%', '**'}

    def tokenize(self, expr: str) -> list[str]:
        if not expr.strip():
            raise ValueError('Пустое выражение')

        if re.search(r'\d\s+\d', expr):
            raise ValueError('Пропущен оператор')
        if re.search(r'\d\s*\(', expr):
            raise ValueError('Пропущен оператор')
        if re.search(r'\)\s*\d', expr):
            raise ValueError('Пропущен оператор')

        expr_no_spaces = expr.replace(' ', '')
        tokens = self.extract_tokens(expr_no_spaces)
        self.validate_basic_structure(tokens)
        return tokens

    def extract_tokens(self, expr: str) -> list[str]:
        """Извлекает токены из строки"""
        tokens = []
        i = 0
        while i < len(expr):
            if i < len(expr) - 1:
                two_char = expr[i:i+2]
                if two_char in {'**', '//'}:
                    tokens.append(two_char)
                    i += 2
                    continue

            char = expr[i]
            if char in '()+-*/%':
                tokens.append(char)
                i += 1
            elif char.isdigit():
                match = re.match(r'\d+\.?\d*', expr[i:])
                if match:
                    tokens.append(match.group())
                    i += len(match.group())
                else:
                    raise ValueError('Некорректный формат числа')
            else:
                raise ValueError('Некорректный токен')
        return tokens

    def validate_basic_structure(self, tokens: list[str]):
        """Базовая проверка структуры выражений"""
        if not tokens:
            raise ValueError('Пустое выражение')

        brackets = 0
        for token in tokens:
            if token == '(':
                brackets += 1
            elif token == ')':
                brackets -= 1
                if brackets < 0:
                    raise ValueError('Непарные скобки')

        if brackets != 0:
            raise ValueError('Непарные скобки')

        if tokens[0] in self.binary_only:
            raise ValueError('Оператор не может быть в начале выражения')
        if tokens[-1] in self.operators:
            raise ValueError('Ожидался операнд')

        for i in range(len(tokens) - 1):
            if tokens[i] == '(' and tokens[i + 1] in self.binary_only:
                raise ValueError('После открывающей скобки не может быть оператора')

    @staticmethod
    def _is_number(token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False
