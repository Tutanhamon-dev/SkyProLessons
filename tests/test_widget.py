import re

import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def sample_inputs() -> list[str]:
    return [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]


@pytest.fixture
def expected_outputs() -> dict:
    return {
        "Maestro 1596837868705199": "Maestro 1596 83** **** 5199",
        "Счет 64686473678894779589": "Счет **9589",
        "MasterCard 7158300734726758": "MasterCard 7158 30** **** 6758",
        "Счет 35383033474447895560": "Счет **5560",
        "Visa Classic 6831982476737658": "Visa Classic 6831 98** **** 7658",
        "Visa Platinum 8990922113665229": "Visa Platinum 8990 92** **** 5229",
        "Visa Gold 5999414228426353": "Visa Gold 5999 41** **** 6353",
        "Счет 73654108430135874305": "Счет **4305",
    }


def test_mask_account_card(sample_inputs: list[str], expected_outputs: dict) -> None:
    # Проверяем корректность маскирования стандартных примеров.
    for inp in sample_inputs:
        assert mask_account_card(inp) == expected_outputs[inp]


def test_mask_account_card_bill_case_insensitive() -> None:
    # Проверяем, что слово "счет" распознаётся в любом регистре
    inp_lower = "счет 73654108430135874305"
    expected = "счет **4305"
    assert mask_account_card(inp_lower) == expected


def test_mask_account_card_bad_types() -> None:
    with pytest.raises(TypeError):
        mask_account_card(None)
    with pytest.raises(TypeError):
        mask_account_card(12345)


def test_mask_account_card_bad_values() -> None:
    with pytest.raises(ValueError):
        mask_account_card("")  # Пустая строка
    with pytest.raises(ValueError):
        mask_account_card("   ")  # Строка с пробелами
    with pytest.raises(ValueError):
        mask_account_card("No digits")  # Строка без цифр
    with pytest.raises(ValueError):
        mask_account_card("346547658")  # Строка без указания карты или счета
    with pytest.raises(ValueError):
        mask_account_card("Visa Classic 6831*9824_76737658")  # Номер содержит недопустимые символы
    with pytest.raises(ValueError):
        mask_account_card("Счет 7658")  # Номер карты слишком короткий


@pytest.mark.parametrize(
    "x, expected",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2019-07-03 18:35:29.512364", "03.07.2019"),
        ("2019-07-03T18:35:29", "03.07.2019"),
        ("2019-07-03 18:35:29", "03.07.2019"),
        ("2020-01-02T00:00:00Z", "02.01.2020"),
        ("2020-01-02T00:00:00+03:00", "02.01.2020"),
        ("2020-12-31T23:59:59.000000-05:00", "31.12.2020"),
        (" 2019-07-03T18:35:29.512364 ", "03.07.2019"),
        ("2021-01-05T01:02:03", "05.01.2021"),  # проверяем нулевое заполнение дня/месяца и корректность года
        ("2000-12-31T23:59:59", "31.12.2000"),
    ],
)
def test_get_date(x: str, expected: str) -> None:
    assert get_date(x) == expected
    # проверяем формат результата
    assert re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", get_date(x))


@pytest.mark.parametrize(
    "bad", [None, 12345, 12.34, ["2019-07-03T18:35:29.512364"], {"date": "2019-07-03T18:35:29.512364"}]
)
def test_get_date_typeerror(bad: object) -> None:
    with pytest.raises(TypeError):
        get_date(bad)


@pytest.mark.parametrize("bad_str", ["", "not a date", "2019-07-03T18:35", "2019/07/03 18:35:29"])
def test_get_date_valueerror(bad_str: str) -> None:
    with pytest.raises(ValueError):
        get_date(bad_str)
