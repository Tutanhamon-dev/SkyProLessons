from typing import List, Dict


def filter_by_state(dictionary_list: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Возвращает список словарей по state"""
    filtered_dictionary_list: List[Dict] = []
    for dictionary in dictionary_list:
        if dictionary["state"] == state:
            filtered_dictionary_list.append(dictionary)
    return filtered_dictionary_list


def sort_by_date(dictionary_list: List[Dict], direction: bool = True) -> List[Dict]:
    """Возвращает список словарей отсортированный по date"""
    sorted_dictionary_list = sorted(dictionary_list, key=lambda x: x["date"], reverse=direction)
    return sorted_dictionary_list
