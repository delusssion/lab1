from tokenizer import Tokenizer
from parser import Parser


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
                raise ValueError('Некорректное выражение')
            return round(result, 10)
        except ValueError:
            raise
        except ZeroDivisionError:
            raise ValueError('Деление на ноль')
        except OverflowError:
            raise ValueError('Слишком большое число')
        except RecursionError:
            raise ValueError('Слишком сложное выражение')
        except Exception as e:
            raise ValueError(f'Непредвиденная ошибка: {str(e)}')


def main():
    calculator = Calculator()
    print('Введите выражение:')
    try:
        expression = input()
        result = calculator.evaluate(expression)
        print(f'Результат: {result}')
    except KeyboardInterrupt:
        print('\nВычисление прервано')
    except ValueError as e:
        print(f'Ошибка: {e}')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')


if __name__ == '__main__':
    main()
