import re
from datetime import datetime
from typing import Any

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(original_text_string: str) -> str:
    """
    Маскирует номер карты или счёта в строке:
    Правила:
      - original_text_string должен быть типа 'str' иначе выбрасывается TypeError.
      - Присутствует один блок цифр. Если блоков с цифрами нет или более одного, то ValueError.
      - В блоке цифр не должно быть прочих символов кроме цифр, иначе ValueError.
      - Перед блоком цифр должен быть непустой префикс. Если префикса нет (цифры в начале строки), то ValueError.
      - Если префикс равен "счет" (регистр не важен) или длина блока цифр >= 20 -> считается счётом.
      - Если вспомогательная функция вернула строку "некорректный номер", то ValueError.
      - Возвращается строка с заменой блока цифр на результат маскирования.
    """
    # Проверяем тип входных данных
    if not isinstance(original_text_string, str):
        raise TypeError("original_text_string должна быть строкой")
    striped_original_string = original_text_string.strip()
    # Создаем список с блоками цифр
    matches = list(re.finditer(r"\d+", striped_original_string))
    # Пустая строка, строка с пробелами, нет блока с цифрами или есть несколько блоков с цифрами. Вызываем ValueError
    if len(matches) > 1 or len(matches) == 0:
        raise ValueError("номер должен состоять из одного блока цифр (без разделителей) и префикса перед ним")
    digits_block = matches[0].group(0)
    # Префикс - вся часть строки до блока цифр, без завершающих пробелов
    prefix = striped_original_string.rstrip(" " + digits_block)
    # Если префикса нет, то ValueError
    if not prefix:
        raise ValueError("Нет префикса перед номером")
    # Вызываем функции маскирования.
    # Если явный "Счет" или номер >= 20, то считаем номером счета. Иначе считаем номером карты.
    if prefix.lower() == "счет" or (len(digits_block) >= 20):
        masked = get_mask_account(digits_block)
    else:
        masked = get_mask_card_number(digits_block)
    # Если функции вернули 'некорректный номер', вызываем ValueError
    if masked == "некорректный номер":
        raise ValueError("некорректный номер")
    else:
        result = prefix + " " + masked
    return result


def get_date(full_date: Any) -> str:
    """
    Принимает строку даты и возвращает строку в формате "ДД.ММ.ГГГГ".
    Поддерживаемые входные форматы (обязательны секунды):
      - "YYYY-MM-DDTHH:MM:SS.ffffff"
      - "YYYY-MM-DD HH:MM:SS.ffffff"
      - "YYYY-MM-DDTHH:MM:SS"
      - "YYYY-MM-DD HH:MM:SS"
    Поведение:
      - Если аргумент не строка вызывается ошибка TypeError.
      - Если строка пустая или не соответствует одному из поддерживаемых форматов вызывается ошибка ValueError.
      - В случае успешного парсинга возвращается дата в формате "ДД.ММ.ГГГГ".
    """
    # Если тип не str, вызываем ошибку TypeError
    if not isinstance(full_date, str):
        raise TypeError("full_date должна быть строкой")
    striped_date = full_date.strip()
    # Регулярное выражение для строгой валидации
    _ISO_WITH_SECONDS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$")
    # Строгая валидация: требует наличие секунд и только разрешённые конструкции иначе ValueError
    if not _ISO_WITH_SECONDS_RE.match(striped_date):
        raise ValueError("Неподдерживаемый формат даты")
    # получаем date из striped_date, указанной в ISO формате
    dt = datetime.fromisoformat(striped_date)
    return dt.strftime("%d.%m.%Y")
