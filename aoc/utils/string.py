import regex
import re
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

def split_on_non_nested(string: str, seps: list[str]) -> tuple[list[str], list[str]]:
    """
    Splits a string on non-nested separators.
    A separator is considered non-nested if it is not enclosed in quotes or brackets.

    Example: split_on_non_nested("a, (b, c), d", seps = [","]) -> ["a", "(b, c)", "d"]

    Args:
        input (str): The input string.
        seps (list[str], optional): The list of separators. Defaults to [","].

    Returns:
        tuple[list[str], list[str]]: A tuple containing the split parts and the separators.
    """
    if len(string) == 0:
        return [], []

    if not any([(sep in string) for sep in seps]):
        return [string], []

    split, splitters = [], []
    accumulator, remaining = "", string
    depth = 0

    double_quote, single_quote = False, False
    while len(remaining) > 0:
        if depth == 0:
            found_separator = False
            for sep in seps:
                if remaining.startswith(sep):
                    if len(accumulator.strip()) > 0:
                        splitters.append(sep)
                        split.append(accumulator.strip())
                    accumulator, remaining = "", remaining[len(sep):]
                    found_separator = True
                    break
            if found_separator:
                continue

        current, remaining = remaining[0], remaining[1:]
        if not double_quote and not single_quote:
            if current in "({[":
                depth += 1
            elif current in ")}]":
                depth -= 1

        if current == '"' and not single_quote:
            double_quote = not double_quote
            depth += 1 if double_quote else -1
        elif current == "'" and not double_quote:
            single_quote = not single_quote
            depth += 1 if single_quote else -1
        accumulator += current

    remaining = (accumulator + remaining).strip()
    if len(remaining) > 0:
        split.append(remaining)

    return split, splitters


def split_on_non_nested_commas(string: str) -> list[str]:
    """
    Shorthand for when splitting exclusively on non-nested commas, for cleaner syntax.
    """
    return split_on_non_nested(string, [","])[0]


def split_on_non_nested_spaces(string: str) -> list[str]:
    """
    Shorthand for when splitting exclusively on non-nested spaces, for cleaner syntax.
    """
    return split_on_non_nested(string, [" "])[0]


def split_on_non_quoted(string: str, seps: list[str], depth = 0):
    """
    Splits a string on non-quoted separators.
    A seperator is considered quoted when it is inside of either a pair of single or double quotes.

    Args:
        string (str): The input string.
        seps (list[str], optional): The list of separators. Defaults to [","].
        depth (int, optional): The current depth of nested quotes. Defaults to 0.

    Returns:
        list[str]: The split parts.
    """
    accumulator = ""
    toggles = {
        '"': False,
        "'": False
    }
    for i, char in enumerate(string):
        for sep in seps:
            if depth == 0 and i <= len(string) - len(sep) and string[i:i+len(sep)] == sep:
                remaining_split, remaining_seps = split_on_non_quoted(string[i+len(sep):], seps, depth)
                return [accumulator.strip()] + remaining_split, [sep] + remaining_seps
        accumulator += char
        if char in toggles:
            toggles[char] = not toggles[char]
            depth += 1 if toggles[char] else -1

    return [accumulator.strip()], []


def search_until(string: str, keys: list[str]) -> tuple[str, str]:
    """
    Searches for a substring until one of the specified keys is found.
    Usually used in a while loop to consume pieces of a string given that each substring starts with a specific tag.


    Example: search_until("The quick brown fox jumped", ["brown", "jumped"]) -> ("The quick ", "brown fox jumped")
             search_until("brown fox jumped", ["brown", "jumped"]) -> ("brown fox", "jumped")
             search_until("jumped", ["brown", "jumped"]) -> ("jumped", "")

    Args:
        string (str): The input string.
        keys (list[str]): The list of keys to search for.

    Returns:
        tuple[str, str]: A tuple containing the substring until the key is found and the remaining string.
    """
    depth = 0
    leader = ""
    for key in keys:
        if string.startswith(key):
            leader = key
            string = string[len(key):]
            break

    for i, char in enumerate(string):
        if char in '{(':
            depth += 1
        elif char in '})':
            depth -= 1
        if depth == 0 and any([string[i:].startswith(key) for key in keys]):
            return leader + string[:i], string[i:]
        
    return leader + string, ""


def search_between(string, start, end):
    """
    Searches for a substring between two specified strings.

    Example: search_between("The quick brown fox jumped", "quick", "jumped") -> " brown fox "

    Args:
        string (str): The input string.
        start (str): The starting string.
        end (str): The ending string.

    Returns:
        str: The substring between the start and end strings.
    """
    return string[string.index(start) + len(start):string.index(end)].strip()

def replace_unquoted(pattern, new, string):
    """
    Replaces occurrences of a pattern in a string, excluding quoted parts.
    Example: replace_unquoted("fox", "dog", "The quick brown fox jumped 'over the other fox') -> "The quick brown dog jumped 'over the other fox'"

    Args:
        pattern (str): The pattern to search for.
        new (str): The replacement string.
        string (str): The input string.

    Returns:
        str: The modified string.
    """
    return re.sub(r"(\"[^\"]*\")|('[^']*')|(" + pattern + ")", lambda x: x.group(1) if x.group(1) else x.group(2) if x.group(2) else new, string)

def space_non_base_table_slashes(string):
    """
    Adds spaces around division symbols, unless they are part of a base table definition. Used to differenciate when to handle a '/' as a division operator and when to handle it as a table definition.
    Example: space_non_base_table_slashes("13//base/table.value") -> "13 / /base/table.value"
    """

    return regex.sub(r"(\"[^\"]*\")|('[^']*')|((?<=(?:^|\s|\/))(?:\/[a-zA-Z0-9_]+)+)|(\/)", lambda x: x.group(1) if x.group(1) else x.group(2) if x.group(2) else x.group(3) if x.group(3) else " / ", string)



def find_bracket(string: str) -> str:
    """
    Traverses the string until the first open bracket is found, then consumes the string until the corresponding closing bracket is reached.
    Example: find_bracket("The {quick brown {fox jumped}} over the lazy dog.") -> "{quick brown {fox jumped}}"

    Args:
        string (str): The input string.

    Returns:
        str: The substring starting from the first open bracket.
    """
    depth, started = 0, False
    start_index, end_index = -1, -1

    other_quotes = {"'": '"', '"': "'"}
    toggles = {c: False for c in other_quotes}
    while (depth > 0 or not started) and end_index <= len(string) - 1:
        end_index += 1
        c = string[end_index]
        if c in toggles and not toggles[other_quotes[c]]:
            toggles[c] = not toggles[c]
        if toggles['"'] or toggles["'"]:
            continue
        if c == "{":
            if not started:
                start_index = end_index
            started = True
            depth += 1
        if c == "}":
            depth -= 1
    return string[start_index:end_index + 1]


def find_unquoted(pattern, string):
    """
    Finds the index of the first occurrence of a pattern in a string, excluding quoted parts.
    
    Args:
        pattern (str): The pattern to search for.
        string (str): The input string.

    Returns:
        int: The index of the first occurrence, or -1 if not found.
    """
    for group in re.finditer(r"(\"[^\"]*\")|('[^']*')|(" + pattern + ")", string):
        if not string[group.start(0)] in '"\'':
            return group.start(0)
    return -1

#TODO: Technically this does not work on double nested parenthesis and whatnot. We should fix that.
def find_unnested(pattern, string):
    """
    Finds the index of the first occurrence of a pattern in a string, excluding quoted and nested parts.
    A string is considered nested if it is inside parentheses, brackets, or curly braces.

    Args:
        pattern (str): The pattern to search for.
        string (str): The input string.

    Returns:
        int: The index of the first occurrence, or -1 if not found.
    """
    for group in re.finditer(r"(\"[^\"]*\")|('[^']*')|(\([^)]*\))|({[^}]*})|(" + pattern + ")", string):
        if not string[group.start(0)] in '"\'({':
            return group.start(0)

    return -1

def strip_opening_parenthesis(string):
    """
    Strips the opening parenthesis from a string, if present, as well as the corresponding closing parenthesis.
    Example: strip_opening_parenthesis("(a (b c) d) e f") -> "a (b c) d e f"
    
    Args:
        string (str): The input string.

    Returns:
        str: The modified string.
    """
    if not string.startswith("("):
        return string
    string, depth = string[1:], 0
    for i, char in enumerate(string):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if depth < 0:
            return replace_unquoted(r"\s+", " ", strip_opening_parenthesis((string[:i] + " " + string[i + 1:]).strip())).strip()
    return string.strip()

def strip_outer_parenthesis(string: str) -> str:
    """
    Strips the outermost pair of parentheses from a string, if present.
    Example: strip_outer_parenthesis("(a (b c) d e f)") -> "a (b c) d e f"
    
    Args:
        string (str): The input string.

    Returns:
        str: The modified string.
    """
    if not string.startswith("(") or not string.endswith(")"):
        return string
    
    depth, sub_string = 0, string
    while sub_string.startswith("(") and sub_string.endswith(")"):
        depth += 1
        sub_string = sub_string[1:-1].strip()

    min_depth = depth
    for c in sub_string:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if depth == 0:
            return string
        min_depth = min(min_depth, depth)

    for _ in range(min_depth):
        string = string[1:-1].strip()

    return string

def has_unquoted(pattern, string):
    """
    Checks if a string contains an unquoted occurrence of a pattern.

    Args:
        pattern (str): The pattern to search for.
        string (str): The input string.

    Returns:
        bool: True if an unquoted occurrence is found, False otherwise.
    """
    unquoted = re.sub(r"(\"[^\"]*\")|('[^']*')", "", string)
    return re.search(pattern, unquoted) != None

def parse_value(string: str, prefix: str = "") -> list[(str, str)]:
    """
    Parses a nested json-like string into a list of key-value pairs.
    Example: parse_value("{a: 1, b: {c: 2, d: 3}}") -> [("a", "1"), ("b.c", "2"), ("b.d", "3")]

    Args:
        string (str): The input string.
        prefix (str, optional): The prefix to prepend to each key. Defaults to "".

    Returns:
        list[(str, str)]: A list of key-value pairs.
    """
    string = string.strip()
    if len(string) == 0 or not string[0] == "{":
        return [(prefix, string)]
    
    properties = []
    groups = split_on_non_nested(string[1:-1], [", "])[0]
    for group in groups:
        tag, value = split_on_non_nested(group, [": "])[0] if ": " in group else (group, "")
        properties += parse_value(value, prefix + "." + tag)

    return properties
    