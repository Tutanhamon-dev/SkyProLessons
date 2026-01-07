import pytest

from src.masks import *

card_numbers_list = [
    ("1596837868705199", "1596 83** **** 5199"),
    ("7158300734726758", "7158 30** **** 6758"),
    ("7158306758", "7158 30** **** 6758"),
    ("", " ** **** "),
]
bills_list = [("64686473678894779589", "**9589"), ("73654108430135874305", "**4305")]


@pytest.mark.parametrize("x, expected", card_numbers_list)
def test_get_mask_card_number(x, expected):
    assert get_mask_card_number(x) == expected


@pytest.mark.parametrize("x, expected", bills_list)
def test_get_mask_account(x, expected):
    assert get_mask_account(x) == expected
