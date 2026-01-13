import re
from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Возвращает номер с маской в формате: 'XXXX XX** **** XXXX'
    Правила:
      - Из входа извлекаются только цифры.
      - Если цифр < 10 или > 100 возвращается 'некорректный номер'.
      - Если цифр >= 10 и < 100 n возвращается формат 'XXXX XX** **** XXXX' независимо от общей длины (включая >16).
    Пример:
      "19273465960727348596" -> "1927 34** **** 8596"
    """
    # Проверяем тип входных данных
    if not isinstance(card_number, (str, int, float)):
        raise TypeError("card_number must be str, int or float")
    # Вычленяем только цифры
    s = str(card_number)
    digits = re.sub(r"\D", "", s)
    n = len(digits)
    # Проверяем ограничение по длине
    if n < 10 or n > 100:
        return "некорректный номер"
    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account: Union[str, int]) -> str:
    """
    Возвращает номер с маской в формате: '**XXXX'
    Правила:
      - Из входа извлекаются только цифры.
      - Если цифр < 6 или > 100 возвращается 'некорректный номер'.
      - В остальных случаях возвращается формат '**XXXX'.
    Пример:
      "65960727348596" -> "**8596"
    """
    # Проверяем тип входных данных
    if not isinstance(account, (str, int, float)):
        raise TypeError("account must be str, int or float")
    # Вычленяем только цифры
    s = str(account)
    digits = re.sub(r"\D", "", s)
    n = len(digits)
    # Проверяем ограничение по длине
    if n < 6 or n > 100:
        return "некорректный номер"
    return "**" + digits[-4:]
