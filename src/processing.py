def filter_by_state(dictionary_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Возвращает список словарей по state"""
    filtered_dictionary_list: list[dict] = []
    for dictionary in dictionary_list:
        if dictionary["state"] == state:
            filtered_dictionary_list.append(dictionary)
    return filtered_dictionary_list


def sort_by_date(dictionary_list: list[dict], direction: bool = True) -> list[dict]:
    """Возвращает список словарей отсортированный по date"""
    sorted_dictionary_list = sorted(dictionary_list, key=lambda x: ["date"], reverse=direction)
    return sorted_dictionary_list
