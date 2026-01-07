import pytest

from src.widget import *

cards_and_bills_list = [
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("Счет 64686473678894779589", "Счет **9589"),
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет 35383033474447895560", "Счет **5560"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
    ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 305", "Счет **305"),
    ("MasterCard 7158306758", "MasterCard 7158 30** **** 6758"),
    ("7158306758", "7158 30** **** 6758"),
    ("35383033474447895560", "**5560"),
]


date_list = [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2004-05-01 02:26:18.1", "01.05.2004")]


@pytest.mark.parametrize("x, expected", cards_and_bills_list)
def test_mask_account_card(x, expected):
    assert mask_account_card(x) == expected


@pytest.mark.parametrize("x, expected", date_list)
def test_get_date(x, expected):
    assert get_date(x) == expected
