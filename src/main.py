from src.power import power_function
from src.constants import SAMPLE_CONSTANT


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    target, degree = map(int, input("Введите два числа разделенные пробелом: ").split(" "))

    result = power_function(target=target, power=degree)

    print(result)

    print(SAMPLE_CONSTANT)

if __name__ == "__main__":
    main()
