from collections.abc import Callable

def filter_none[T](lst: list[T | None]) -> list[T]:
    output: list[T] = [i for i in lst if i is not None]
    return output

def find_first[T](lst: list[T], condition: Callable[[T], bool]) -> T:
    for item in lst:
        if condition(item):
            return item
    return None

def extend_with_unique[T](lst: list[T], new_items: list[T]) -> list[T]:
    unique_items = set(lst)
    for item in new_items:
        if item not in unique_items:
            lst.append(item)
    return lst

def cast_lower(lst: list[str]) -> list[str]:
    return [i.lower() for i in lst]

def flatten[T](lst: list[list[T]]) -> list[T]:
    return [item for sublist in lst for item in sublist]

def drop_duplicates[T](lst: list[T]) -> list[T]:
    new_list = []
    for item in lst:
        if item in new_list:
            continue
        new_list.append(item)
    return new_list

def partition[T](lst: list[T], condition: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    return [item for item in lst if condition(item)], [item for item in lst if not condition(item)]
