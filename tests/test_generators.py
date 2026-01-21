from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        # стандарт — code == "USD"
        {"id": 1, "operationAmount": {"amount": "10.00", "currency": {"name": "USD", "code": "USD"}}},
        # другая валюта — code == "RUB"
        {"id": 2, "operationAmount": {"amount": "20.00", "currency": {"name": "EUR", "code": "RUB"}}},
        # нет code — пропускается
        {"id": 3, "operationAmount": {"amount": "30.00", "currency": {"name": "USD"}}},
        # code в смешанном регистре — корректен
        {"id": 4, "operationAmount": {"amount": "40.00", "currency": {"name": "Dollar", "code": "uSd"}}},
        # currency как строка — пропускается
        {"id": 5, "operationAmount": {"amount": "50.00", "currency": "USD"}},
        # Элемент — не словарь — пропускается
        "not a dict",
        # operationAmount отсутствует/None — пропускается
        {"id": 7, "operationAmount": None},
        # code не строка — пропускается
        {"id": 8, "operationAmount": {"amount": "80.00", "currency": {"code": None}}},
    ]


def test_filter_by_currency_matches(sample_transactions: List[Dict[str, Any]]) -> None:
    """
    Функция возвращает только транзакции, у которых в operationAmount.currency.code есть строка,
    совпадающая с искомой валютой (нечувствительно к регистру). Остальные транзакции пропускаются.
    """
    result_list = list(filter_by_currency(sample_transactions, "usd"))
    # Правильные транзакции попали в выдачу
    assert [transaction["id"] for transaction in result_list] == [1, 4]
    # Транзакции с неправильным currency.code — пропускаются
    assert [transaction["id"] for transaction in result_list] != [2, 3, 5, 6, 7, 8]


def test_filter_by_currency_returns_empty() -> None:
    """Пустой список транзакций должен привести к пустому итератору без ошибок."""
    result_list = list(filter_by_currency([], "USD"))
    assert result_list == []


def test_filter_by_currency_iteration_stop(sample_transactions: List[Dict[str, Any]]) -> None:
    """Проверка поведения генератора: next() возвращает элементы по одному, затем после конца — StopIteration."""
    result = filter_by_currency(sample_transactions, "RUB")
    first = next(result)
    assert first["id"] == 2
    with pytest.raises(StopIteration):
        next(result)


def test_filter_by_currency_transaction_typeerror() -> None:
    """Если transaction_list не список — TypeError."""
    with pytest.raises(TypeError):
        # Передаём строку вместо списка
        list(filter_by_currency("not a list", "USD"))  # type: ignore[arg-type]


def test_filter_by_currency_currency_typeerror() -> None:
    """Если currency не строка — TypeError."""
    with pytest.raises(TypeError):
        # Передаём None — это не строка (используем type: ignore для аннотации)
        list(filter_by_currency([], None))  # type: ignore[arg-type]


@pytest.mark.parametrize("bad_currency", ["", "   "])
def test_filter_by_currency_empty_currency(bad_currency: str) -> None:
    """Пустая строка или строка, содержащая только пробелы, вызывает ValueError."""
    with pytest.raises(ValueError):
        list(filter_by_currency([], bad_currency))


# -------------------------------------------------------------------------------------


@pytest.fixture
def sample_transactions_example() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


def test_transaction_descriptions(sample_transactions_example: List[Dict[str, Any]]) -> None:
    """Проверяет, что генератор возвращает все ожидаемые значения и при достижении конца будет StopIteration"""
    gen = transaction_descriptions(sample_transactions_example)
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert list(gen) == expected
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_bad_values() -> None:
    """Проверяем, что некорректные значения пропускаются."""
    transactions = [
        {"id": 1, "description": "Перевод"},        # Корректное значение
        "not a dict",                               # не словарь - пропускается
        {"id": 2},                                  # нет description - пропускается
        {"id": 3, "description": None},             # description == None - пропускается
        {"id": 4, "description": 123},              # числа - пропускается
        {"id": 5, "description": "  Перевод  "},    # Корректное значение с пробелами
        {"id": 6, "description": "   "},            # пробелы - пропускается
    ]
    gen = transaction_descriptions(transactions)
    assert list(gen) == ["Перевод", "Перевод"]


def test_transaction_descriptions_empty_list() -> None:
    """Пустой список транзакций возвращает пустой итератор без ошибок."""
    assert list(transaction_descriptions([])) == []


def test_transaction_descriptions_invalid_type() -> None:
    """Если входной аргумент не список — выбрасывается TypeError."""
    with pytest.raises(TypeError):
        # Передаём None вместо списка
        list(transaction_descriptions(None))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        # Передаём словарь вместо списка
        list(transaction_descriptions({"id": 1}))  # type: ignore[arg-type]


# -------------------------------------------------------------------------------------


def test_card_number_generator() -> None:
    """Генератор возвращает последовательность номеров от start до stop включительно. После - StopIteration"""
    gen = card_number_generator(1, 3)
    expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    assert list(gen) == expected
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_one_item() -> None:
    """Если start == stop — генератор возвращает ровно один номер"""
    assert list(card_number_generator(42, 42)) == ["0000 0000 0000 0042"]


@pytest.mark.parametrize(
    "bad_start,bad_stop",
    [
        ("1", 5),  # строка вместо int
        (1, 5.0),  # float вместо int
        (1.0, 5),  # float вместо int
        (None, 1), # None вместо int
    ],
)
def test_card_number_generator_typeerror(bad_start: Any, bad_stop: Any) -> None:
    """Некорректные типы приводят к TypeError."""
    with pytest.raises(TypeError):
        list(card_number_generator(bad_start, bad_stop))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "bad_start,bad_stop",
    [
        (5, 1),         # start > stop
        (0, 1),         # start ниже минимально допустимого (минимум 1)
        (1, 10**16),    # stop выше максимально допустимого (максимум 10**16-1)
        (-10, 10),      # отрицательное start
    ],
)
def test_card_number_generator_valueerror(bad_start: int, bad_stop: int) -> None:
    """Проверяем, что некорректные данные где start > stop или выход за пределы, вызывают ValueError."""
    with pytest.raises(ValueError):
        list(card_number_generator(bad_start, bad_stop))


def test_card_number_generator_bool_values() -> None:
    """Проверяем данные типа bool. True = 1, False = 0."""
    assert list(card_number_generator(True, 2)) == ["0000 0000 0000 0001", "0000 0000 0000 0002"]

    with pytest.raises(ValueError):
        list(card_number_generator(False, 1))  # type: ignore[arg-type]
