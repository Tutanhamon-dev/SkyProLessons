from typing import Any, Dict, Iterator, List


def filter_by_currency(transaction_list: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Генератор — итератор по транзакциям, у которых валюта операции соответствует заданной.
    Правила:
    - transaction_list: должен быть списком (List), если нет, то элемент пропускается.
    - currency: должен быть строкой (str).
    - Сравнение валюты нечувствительно к регистру и игнорирует внешние пробелы.
    - Функция пропускает записи с отсутствующими или некорректными полями.
    - Возвращает генератор. Если транзакций с заданной валютой нет — итератор завершается
    Исключения:
    - TypeError: если transactions не список или currency не строка
    - ValueError: если currency пустая или содержит только пробелы
    """
    # Проверки входных параметров (граничные случаи)
    if not isinstance(transaction_list, list):
        raise TypeError("transaction_list должен быть списком")
    if not isinstance(currency, str):
        raise TypeError("currency должен быть строкой")
    # Обрезаем пробелы и проверяем пустоту
    currency = currency.strip().upper()
    if not currency:
        raise ValueError("currency не может быть пустой строкой или строкой из пробелов")
    for transaction in transaction_list:
        # Пропускаем если не словари
        if not isinstance(transaction, dict) or not isinstance(transaction.get("operationAmount"), dict):
            continue
        cur_code = transaction.get("operationAmount").get("currency")  # type: ignore
        if isinstance(cur_code, dict) and isinstance(cur_code.get("code"), str):
            if cur_code.get("code").upper() == currency:  # type: ignore
                yield transaction


def transaction_descriptions(transaction_list: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор — итератор, который по очереди возвращает поле `description` каждой транзакции списка.
    Правила:
    - transactions должен быть списком.
    - Каждый элемент списка обрабатывается, только если это словарь.
    - Для каждого словаря берётся значение по ключу "description".
      Если значение является строкой, удаляются внешние пробелы и строка возвращается.
    - Записи без ключа "description", со значениями не str или с пустыми/пробельными значениями - пропускаются.
    - Если элементов нет — итератор завершается (StopIteration).
    Исключения:
    - TypeError: если transactions не список
    """
    # Проверка входного аргумента
    if not isinstance(transaction_list, list):
        raise TypeError("transactions должен быть списком")
    for transaction in transaction_list:
        # Пропускаем элементы, которые не являются словарями
        if not isinstance(transaction, dict):
            continue
        description = transaction.get("description")
        # Берём только строковые описания; пропускаем None, числа и т.п.
        if isinstance(description, str) and description.strip() != "":
            yield description.strip()


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    Правила:
    - Генерирует номера в диапазоне от start до stop включительно.
    - Каждый номер представлен как строка длиной 16 символов с ведущими нулями.
    - Номера разделены пробелами по 4 символа.
    - Начальное значение должно быть меньше или равно конечному.
    - Диапазон значений: от 1 до 9999999999999999.

    Исключения:
    - TypeError: если start или stop не целые числа.
    - ValueError: если start > stop или значения вне допустимого диапазона.
    """
    # Проверка типов
    if not isinstance(start, int) or not isinstance(stop, int):
        raise TypeError("start и stop должны быть целыми числами")

    # Проверка диапазона
    if start > stop or not (1 <= start <= 9999999999999999) or not (1 <= stop <= 9999999999999999):
        raise ValueError("должно быть: start <= stop и start, stop в диапазоне от 1 до 9999999999999999")

    for number in range(start, stop + 1):
        # Форматируем номер как строку длиной 16 символов с ведущими нулями
        formatted = f"{number:016d}"
        # Разбиваем на блоки по 4 символа
        yield " ".join(formatted[i: i + 4] for i in range(0, 16, 4))
