import re


class Tokenizer:
    """Разбивает выражение на токены и выполняет валидацию последовательности"""

    def tokenize(self, expr: str) -> list[str]:
        """Разбивает выражение на токены"""
        if not expr.strip():
            raise ValueError('Пустое выражение')
        expr_no_spaces = expr.replace(' ', '')

        if re.search(r'\d\s+\d', expr):
            raise ValueError('Пропущен оператор между числами')

        if expr_no_spaces[0] in '*/%':
            raise ValueError('Выражение не может начинаться с оператора')

        pattern = r'\d+\.?\d*|\.\d+|\*\*|//|[()*/%+\-]'
        tokens = []
        i = 0

        while i < len(expr_no_spaces):
            match = re.match(pattern, expr_no_spaces[i:])
            if not match:
                raise ValueError('Некорректный символ')
            token = match.group()
            i += len(token)
            tokens.append(token)

        for token in tokens:
            if self.is_number(token):
                if token.startswith('0') and len(token) > 1 and token[1] != '.':
                    raise ValueError('Число не может начинаться с нуля')
                if token.startswith('.') or token.endswith('.'):
                    raise ValueError('Некорректный формат числа')

        self.validate_token_sequence(tokens)

        return tokens

    def validate_token_sequence(self, tokens: list[str]) -> None:
        """Проверяет корректность последовательности токенов"""
        operators = {'+', '-', '*', '/', '//', '%', '**'}
        binary_only = {'*', '/', '//', '%', '**'}
        brackets_count = 0

        for i in range(len(tokens)):
            curr = tokens[i]
            next_token = tokens[i + 1] if i < len(tokens) - 1 else None
            prev_token = tokens[i - 1] if i > 0 else None

            if curr == '(':
                brackets_count += 1
                if next_token == ')':
                    raise ValueError('Пустые скобки недопустимы')
                if next_token in binary_only:
                    raise ValueError('После открывающей скобки не может быть оператора')

            elif curr == ')':
                brackets_count -= 1
                if brackets_count < 0:
                    raise ValueError('Неправильный порядок скобок')
                if next_token and self.is_number(next_token):
                    raise ValueError('Пропущен оператор после закрывающей скобки')

            elif curr in operators:
                is_unary = (prev_token is None or prev_token == '(' or prev_token in operators)
                if curr in binary_only:
                    if next_token in operators and next_token not in {'+', '-'}:
                        raise ValueError('Недопустимая последовательность операторов')
                    if next_token is None:
                        raise ValueError('Ожидался операнд после оператора')
                else:
                    if not is_unary:
                        j = i + 1
                        while j < len(tokens) and tokens[j] in {'+', '-'}:
                            j += 1
                        if j >= len(tokens):
                            raise ValueError('Ожидался операнд после оператора')
                        if tokens[j] in operators and tokens[j] not in {'+', '-'}:
                            raise ValueError('Недопустимая последовательность операторов')
                        if next_token is None:
                            raise ValueError('Ожидался операнд после оператора')
        if brackets_count != 0:
            raise ValueError('Непарные скобки')

    @staticmethod
    def is_number(token: str) -> bool:
        """Проверяет, является ли токен числом"""
        try:
            float(token)
            return True
        except ValueError:
            return False
