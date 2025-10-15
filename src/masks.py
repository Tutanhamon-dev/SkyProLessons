from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Возвращает номер карты с маской"""
    str_card_number = str(card_number)
    return f"{str_card_number[0:4]} {str_card_number[4:6]}** **** {str_card_number[-4:]}"


def get_mask_account(account: Union[str, int]) -> str:
    """Возвращает номер счета с маской"""
    return "**" + str(account)[-4:]
