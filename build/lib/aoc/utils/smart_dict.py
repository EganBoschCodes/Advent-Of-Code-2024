from aoc.utils import drop_duplicates

from collections.abc import Callable
from typing import Self

class SmartDict[ValueType]:
    def __init__(self, starting_dict: dict[str, ValueType], default_constructor: Callable[[str], ValueType] = None):
        self.__dictionary = starting_dict
        self.__key_map: dict[str, str] = {key.lower(): key for key in starting_dict.keys()}
        self.default_constructor = default_constructor
        self.__always_return_default = False

    def __initialize_key__(self, key: str) -> None:
        if self.default_constructor is None:
            raise KeyError(f"SmartDict: Key {key} not found in dictionary")
        self.__dictionary[key] = self.default_constructor(key)
        self.__key_map[key.lower()] = key

    def __getitem__(self, key: str) -> ValueType:
        if self.__always_return_default and self.default_constructor is not None:
            return self.default_constructor(key)
        if not key.lower() in self.__key_map:
            self.__initialize_key__(key)
        return self.__dictionary[self.__key_map[key.lower()]]

    def __setitem__(self, key: str, value: ValueType) -> None:
        if not key.lower() in self.__key_map:
            self.__key_map[key.lower()] = key
        self.__dictionary[self.__key_map[key.lower()]] = value

    def __contains__(self, key: str) -> bool:
        return key.lower() in self.__key_map
    
    def __iter__(self) -> iter:
        return iter(self.__dictionary)
    
    def __len__(self) -> int:
        return len(self.__dictionary)
    
    def items(self) -> list[tuple[str, ValueType]]:
        return self.__dictionary.items()
    
    def keys(self) -> list[str]:
        return self.__dictionary.keys()
    
    def values(self) -> list[ValueType]:
        return self.__dictionary.values()
    
    def __str__(self) -> str:
        string = f"SmartDict (length {len(self.__dictionary)}):\n{{"
        for key, value in self.__dictionary.items():
            string += f"\n\t{str(key)}: {str(value)},"
        string += f"\n}}"
        return string
    
    def __delitem__(self, key: str) -> None:
        if key.lower() in self.__key_map:
            del self.__dictionary[self.__key_map[key.lower()]]
            del self.__key_map[key.lower()]
    
    def apply[T](self, f: Callable[[str, ValueType], T]) -> Self:
        return SmartDict[T]({key: f(key, value) for key, value in self.__dictionary.items()})
    
    def for_each(self, f: Callable[[str, ValueType], None]) -> Self:
        for key, value in self.__dictionary.items():
            f(key, value)
        return self
    
    def set_default(self, default_constructor: Callable[[str], ValueType]):
        self.default_constructor = default_constructor
        return self
    
    def clear(self):
        self.__dictionary = {}
        self.__key_map = {}
        return self
    
    def filter(self, f: Callable[[str, ValueType], bool]) -> Self:
        return SmartDict({key: value for key, value in self.__dictionary.items() if f(key, value)}, self.default_constructor)
    
    def sort(self, key: Callable[[str, ValueType], any] = lambda k, v: k):
        return SmartDict({key: value for key, value in sorted(self.__dictionary.items(), key = lambda x: key(x[0], x[1]))}, self.default_constructor)
    
def coalesce_smart_dicts[T](dicts: list[SmartDict[list[T]]]) -> SmartDict[list[T]]:
    new_dict = SmartDict({}, lambda _: [])
    for dictionary in dicts:
        for key, value in dictionary.items():
            if not key in new_dict:
                new_dict[key] = value
                continue
            new_dict[key] += value
            #new_dict[key] = new_dict[key] + value
    for key, value in new_dict.items():
        new_dict[key] = drop_duplicates(value)

    return new_dict.set_default(lambda _: [])
