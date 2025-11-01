from tokenizer import Tokenizer
from parser import Parser


class Calculator:
    """Токенизация + парсинг + обработка ошибок"""

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def evaluate(self, expression: str) -> float:
        """Вычисляет математическое выражение"""
        try:
            tokens = self.tokenizer.tokenize(expression)
            result = self.parser.parse_expression(tokens.copy())
            return round(result, 10)
        except ValueError as e:
            raise ValueError(str(e))
        except ZeroDivisionError:
            raise ZeroDivisionError('Деление на ноль')
        except OverflowError:
            raise OverflowError('Слишком большое число')
        except RecursionError:
            raise RecursionError('Слишком сложное выражение')
        except Exception as e:
            raise ValueError(f'Ошибка вычисления: {str(e)}')


def main():
    calculator = Calculator()
    print('Введите выражение:')

    try:
        expression = input()
        result = calculator.evaluate(expression)
        print(f'Результат: {result}')
    except ValueError as e:
        print(f'Ошибка: {e}')
    except ZeroDivisionError as e:
        print(f'Ошибка: {e}')
    except OverflowError as e:
        print(f'Ошибка: {e}')
    except RecursionError as e:
        print(f'Ошибка: {e}')
    except KeyboardInterrupt:
        print('\nВычисление прервано')
    except Exception as e:
        print(f'Непредвиденная ошибка: {e}')


if __name__ == '__main__':
    main()
