from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_dictionary_list() -> List[Dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 939735570, "state": "EXECUTED", "date": "2018-09-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Проверяем работу сортировки по 'state'
def test_filter_by_state(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    # значение ключа "state" по умолчанию "EXECUTED"
    modified_list: List[Dict[str, Any]] = filter_by_state(sample_dictionary_list)
    assert isinstance(modified_list, list)  # возвращен список
    assert len(modified_list) == 3  # кол-во элементов в списке 3
    # проверяем что все элементы являются словарями
    assert all(isinstance(item, dict) for item in modified_list)
    # Проверяем, что вернулись три нужных словаря
    assert {i["id"] for i in modified_list} == {41428829, 939735570, 939719570}


# Проверяем сортировку с другим ключом в нижнем регистре
def test_filter_by_state_case_insensitive(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    modified_list: List[Dict[str, Any]] = filter_by_state(sample_dictionary_list, "canceled")
    assert len(modified_list) == 2  # кол-во элементов в списке 2
    # Проверяем, что вернулись два нужных словаря
    assert {i["id"] for i in modified_list} == {594226727, 615064591}


# Проверяем различные игнорируемые случаи
def test_filter_by_state_mixed_list() -> None:
    mixed_list: List[Any] = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": None},  # если значение 'state' не строка, то словарь игнорируется
        {"id": 3},  # если нет ключа 'state', то словарь игнорируется
        "not a dict",  # не dict -> игнорируется
        12345,  # не dict -> игнорируется
        {"id": 4, "state": "executed"},  # lower-case — должно совпадать (регистр игнорируется)
        {"id": 5, "state": 123},  # числовой state -> игнорируется
        {"id": 6, "state": True},  # булев -> игнорируется
        {"id": 6, "state": []},  # если значение 'state' список, то словарь игнорируется
    ]
    modified_list: List[Dict[str, Any]] = filter_by_state(mixed_list, "EXECUTED")
    # ожидаются только элементы с id 1 и 4
    assert len(modified_list) == 2
    assert {i["id"] for i in modified_list} == {1, 4}


# Если список пустой, то возвращает пустой список
def test_filter_by_state_empty_list() -> None:
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_type_error(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    # state не строка
    with pytest.raises(TypeError):
        filter_by_state(sample_dictionary_list, 123)
    # dictionary_list не список
    with pytest.raises(TypeError):
        filter_by_state("not a list", "EXECUTED")


# Проверяем работу сортировки по 'date' по умолчанию
def test_sort_by_date_descending(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    modified_list: List[Dict[str, Any]] = sort_by_date(sample_dictionary_list)
    assert {i["id"] for i in modified_list} == {41428829, 615064591, 939735570, 594226727, 939719570}


# Проверяем работу сортировки по 'date' в обратном порядке
def test_sort_by_date_ascending(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    modified_list: List[Dict[str, Any]] = sort_by_date(sample_dictionary_list, False)
    assert {i["id"] for i in modified_list} == {939719570, 594226727, 939735570, 615064591, 41428829}


def test_sort_by_date_bad_date(sample_dictionary_list: List[Dict[str, Any]]) -> None:
    # Добавляем в список элементы с не корректным значением 'date'
    missing1: Dict[str, Any] = {"id": 100, "state": "UNKNOWN"}  # словарь без 'date'
    missing2: Any = "not a dict"  # не словарь
    missing3: Dict[str, Any] = {"id": 200, "state": "EXECUTED", "date": 12345}  # date не строка
    mixed_dictionary_list: List[Any] = [missing1, missing2] + sample_dictionary_list + [missing3]
    # элементы с некорректной 'date' должны оказаться в конце
    modified_list: List[Any] = sort_by_date(mixed_dictionary_list)
    # В начале элементы отсортированные по датам
    assert [d["id"] for d in modified_list[:5]] == [41428829, 615064591, 939735570, 594226727, 939719570]
    # В конце элементы с некорректной 'date' в том же порядке
    assert modified_list[-3] is missing1
    assert modified_list[-2] is missing2
    assert modified_list[-1] is missing3
    # Проверка сортировки в обратном порядке
    modified_list = sort_by_date(mixed_dictionary_list, False)
    assert [d["id"] for d in modified_list[:5]] == [939719570, 594226727, 939735570, 615064591, 41428829]
    # В конце элементы с некорректной 'date' в том же порядке
    assert modified_list[-3] is missing1
    assert modified_list[-2] is missing2
    assert modified_list[-1] is missing3


# Если список пустой, то возвращает пустой список
def test_sort_by_date_empty_list() -> None:
    assert (
        sort_by_date(
            [],
        )
        == []
    )


def test_sort_by_date_type_error() -> None:
    with pytest.raises(TypeError):
        sort_by_date("not a list")  # если не список, то ошибка TypeError
