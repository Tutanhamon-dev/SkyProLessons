from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(original_string: str) -> str:
    """Принимает строку с названим карты и номером или номером счета и возвращает сокрытый номер"""
    original_string_list = original_string.split()
    if len(original_string_list[-1]) < 20:
        original_string_list[-1] = get_mask_card_number(original_string_list[-1])
    else:
        original_string_list[-1] = get_mask_account(original_string_list[-1])
    return " ".join(original_string_list)


def get_date(full_date: str) -> str:
    """Принимает строку вида 'ГГГГ-ММ-ДДTчч:мм:сс.ссс' возвращает 'ДД.ММ.ГГГГ'"""
    datetime_object = datetime.strptime(full_date.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")
    formatted_date = datetime_object.strftime("%d.%m.%Y")
    return formatted_date
