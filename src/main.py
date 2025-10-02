import re


class CalcError(Exception):
    """Исключение для ошибок калькулятора."""
    pass

class Calculator:
    """Калькулятор для вычисления математических выражений"""

    def tokenize(self, expr: str) -> list[str]:
        """Токенизация математического выражения"""
        
        if not expr.strip():
            raise CalcError('Пустое выражение')

        expr_clean = expr.replace(' ', '')

        if re.match(r'^[+\-]{2,}', expr_clean):
            raise CalcError('Несколько унарных операторов подряд')
            
        if expr_clean[0] in ['*', '/', '%']:
            if not (len(expr_clean) > 1 and expr_clean[1] in ['*', '/']):
                raise CalcError('Выражение не может начинаться с оператора')

        if re.search(r'\d\s+\d', expr):
            raise CalcError('Пропущен оператор между числами')

        pattern = r'\d+\.?\d*|\.\d+|\*\*|//|[()*/%+-]'

        tokens: list[str] = []
        i = 0
        while i < len(expr_clean):
            match = re.match(pattern, expr_clean[i:])
            if match:
                token = match.group()
                tokens.append(token)
                i += len(token)
            else:
                raise CalcError(f'Некорректный символ: {expr_clean[i]}')

        for token in tokens:
            token_without_unary = token.lstrip('-+')
            if token_without_unary.replace('.', '').isdigit():
                if (len(token_without_unary) > 1 and token_without_unary[0] == '0' and token_without_unary[1] != '.'):
                    raise CalcError(f'Число не может начинаться с нуля: "{token}"')

                if token.startswith('.'):
                    raise CalcError(f'Число не может начинаться с точки: "{token}"')

                if token.endswith('.'):
                    raise CalcError(f'Число не может заканчиваться точкой: "{token}"')

        for i in range(len(tokens) - 1):
            curr_token = tokens[i]
            next_token = tokens[i + 1]

            if (curr_token in ['+', '**', '//', '%', '/', '*', '-'] and next_token in ['+', '**', '//', '%', '/', '*', '-'] and not (curr_token + next_token in ['**', '//'])):
                raise CalcError('Недопустимая последовательность операторов')

            if curr_token == '(' and next_token in '*/%+':
                raise CalcError('После открывающей скобки не может быть оператора')

            if curr_token in '+-*/%' and next_token == ')':
                raise CalcError('Перед закрывающей скобкой не может быть оператора')

            if (self.is_number(curr_token) and next_token == '('):
                raise CalcError('Пропущен оператор между числом и открывающей скобкой')

            if (curr_token == ')' and self.is_number(next_token)):
                raise CalcError('Пропущен оператор между закрывающей скобкой и числом')

        if tokens['(', ')']:
            raise CalcError('Пустые скобки')

        if tokens and tokens[-1] in ['+', '-', '*', '/', '//', '%', '**']:
            raise CalcError('Выражение не может заканчиваться оператором')

        bracket_balance = 0
        for token in tokens:
            if token == '(':
                bracket_balance += 1
            elif token == ')':
                bracket_balance -= 1
                if bracket_balance < 0:
                    raise CalcError('Некорректный порядок скобок')

        if bracket_balance != 0:
            raise CalcError('Некорректное использование скобок')

        return tokens

    def expr(self, tokens: list[str]) -> float:
        return self.add(tokens)

    def add(self, tokens: list[str]) -> float:
        result = self.mul(tokens)

        while tokens and tokens[0] in ['+', '-']:
            op = tokens.pop(0)
            right = self.mul(tokens)
            if op == '+':
                result += right
            else:
                result -= right

        return result

    def mul(self, tokens: list[str]) -> float:
        result = self.pow(tokens)

        while tokens and tokens[0] in ['*', '/', '//', '%']:
            op = tokens.pop(0)
            right = self.pow(tokens)
            if op == '*':
                result *= right
            elif op == '/':
                if right == 0:
                    raise CalcError('Деление на ноль')
                result /= right
            elif op == '//':
                if not self.is_integer(result) or not self.is_integer(right):
                    raise CalcError('Операция // допустима только для целых чисел')
                if right == 0:
                    raise CalcError('Деление на ноль')
                result //= right
            elif op == '%':
                if not self.is_integer(result) or not self.is_integer(right):
                    raise CalcError('Операция % допустима только для целых чисел')
                if right == 0:
                    raise CalcError('Деление на ноль')
                result %= right

        return result

    def pow(self, tokens: list[str]) -> float:
        result = self.unary(tokens)
        if tokens and tokens[0] == '**':
            tokens.pop(0)
            right = self.pow(tokens)
            result **= right
        return result

    def unary(self, tokens: list[str]) -> float:
        if tokens and tokens[0] in ['+', '-']:
            op = tokens.pop(0)
            result = self.unary(tokens)
            return result if op == '+' else -result
        else:
            return self.primary(tokens)

    def primary(self, tokens: list[str]) -> float:
        if tokens[0] == '(':
            tokens.pop(0)
            result = self.expr(tokens)
            tokens.pop(0)
            return result
        else:
            token = tokens.pop(0)
            if not self.is_number(token):
                raise CalcError(f'Некорректный токен: {token}')
            if '.' in token:
                return float(token)
            else:
                return int(token)

    def is_number(self, token: str) -> bool:
        token_without_unary = token.lstrip('-+')
        return token_without_unary.replace('.', '').isdigit() and token_without_unary.count('.') <= 1

    def is_integer(self, number: float) -> bool:
        return isinstance(number, int) or (isinstance(number, float) and number.is_integer())

    def calculate(self, expression: str) -> float:
        tokens = self.tokenize(expression)
        result = self.expr(tokens)
        return result


if __name__ == '__main__':
    calculator = Calculator()
    print('Введите выражение:')
    try:
        result = calculator.calculate(input())
        print(f'Результат: {result}')
    except CalcError as error:
        print(f'Ошибка: {error}')