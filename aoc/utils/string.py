import json

def consistent_hash(text: str):
    valid_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    hash = 0
    for ch in text[::-1]:
        hash = ((hash * 281) ^ (ord(ch) * 997)) & 0xFFFFFFFF

    string_output = ""
    while hash > 0:
        string_output = valid_characters[hash % 36] + string_output
        hash = hash // 36

    return string_output


def dict_text(input: any) -> str:
    return json.dumps(input.__dict__(), indent=4)

def uncased_equal(a: str, b: str) -> bool:
    return a.lower() == b.lower()

def indent(string: str) -> str:
    """
    Adds a tab character before each line in the input string.

    Args: string (str): The input string.
    Returns: str: The indented string.
    """
    return "\t" + string.replace("\n", "\n\t")


def filter_blank(strings: list[str]) -> list[str]:
    """
    Filters out empty strings from a list.

    Args: input (list): The input list.
    Returns: list: The filtered list.
    """
    return list(filter(lambda x: len(x) > 0, strings))
    