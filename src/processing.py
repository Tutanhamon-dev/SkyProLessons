from typing import Any, Dict, List


def filter_by_state(dictionary_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает список словарей отфильтрованных по заданному ключу поля 'state'.
    Параметры:
      - state: строка со значением ключа 'state' (регистр не важен).
      - dictionary_list: список словарей (каждый элемент — словарь).
    Возвращает:
      - список словарей у которых значение ключа 'state' равно полученному значению (по умолчанию "EXECUTED").
      - если элементы не являются словарями или у них нет ключа 'state', то они игнорируются.
    Исключения:
      - TypeError, если state не строка или records не список.
    """
    if not isinstance(state, str):
        raise TypeError("Значение ключа должно быть строкой")
    if not isinstance(dictionary_list, list):
        raise TypeError("Принимаемый список должен быть списком словарей")

    def key_matches(cur_dictionary: Dict[str, Any]) -> bool:
        if not isinstance(cur_dictionary, dict):
            return False
        state_value = cur_dictionary.get("state")
        if not isinstance(state_value, str):
            return False
        return state_value.upper() == state.upper()

    return [cur_dictionary for cur_dictionary in dictionary_list if key_matches(cur_dictionary)]


def sort_by_date(dictionary_list: List[Dict[str, Any]], direction: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по строковому полю 'date' без парсинга в datetime.
    Параметры:
      - dictionary_list: список словарей; элементы, не словари или не содержат ключ 'date', то в конец результата.
      - direction: True — в начале новые, False — в начале старые.
    Возвращает:
      - новый список, отсортированный по строковому значению поля 'date' в лексикографическом порядке.
    Исключения:
      - TypeError, если dictionary_list не является списком.
    """
    if not isinstance(dictionary_list, list):
        raise TypeError("dictionary_list must be a list")

    # Для элементов без даты используем ключ, который гарантирует появление таких элементов в конце.
    if direction:
        missing_date_key = ""  # используем минимальную строку ''
    else:
        missing_date_key = "\uffff" * 4  # используем большую строку-сентинел

    def _key(item: Any) -> str:
        if not isinstance(item, dict):  # если элемент списка не словарь, то подставляем свой ключ
            return missing_date_key
        date_value = item.get("date")
        if not isinstance(date_value, str):  # если 'date' не строка, то подставляем свой ключ
            return missing_date_key
        return date_value

    return sorted(dictionary_list, key=_key, reverse=direction)
