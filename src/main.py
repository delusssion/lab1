from .tokenizer import Tokenizer, CalcError
from .parser import Parser


class Calculator:
    """Токенизация + парсинг + обработка ошибок"""

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def evaluate(self, expression: str) -> float:
        try:
            tokens = self.tokenizer.tokenize(expression)
            result = self.parser.parse_expression(tokens)
            if tokens:
                raise CalcError('Некорректное выражение')
            return round(result, 10)
        except CalcError:
            raise
        except ZeroDivisionError:
            raise CalcError('Деление на ноль')
        except OverflowError:
            raise CalcError('Слишком большое число')
        except RecursionError:
            raise CalcError('Слишком сложное выражение')
        except Exception as e:
            raise CalcError(f'Непредвиденная ошибка: {str(e)}')


def main():
    calculator = Calculator()
    print('Введите выражение:')
    try:
        expression = input()
        result = calculator.evaluate(expression)
        print(f'Результат: {result}')
    except KeyboardInterrupt:
        print('\nВычисление прервано')


if __name__ == '__main__':
    main()
