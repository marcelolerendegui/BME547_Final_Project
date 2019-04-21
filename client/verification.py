# Copyright 2019:
#       Marcelo Lerendegui <marcelo@lerendegui.com>
#       WeiHsien Lee <weihsien.lee@duke.edu>
#       Yihang Xin <yihang.xin@duke.edu>

# This file is part of BME547_Final_Project.
#
# BME547_Final_Project is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# BME547_Final_Project is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BME547_Final_Project.
# If not, see <https://www.gnu.org/licenses/>.

from typing import Union, List, Any, Dict, Generator
from functools import reduce
import string


def is_int(s: str) -> bool:
    """ Checks if input string can be turned into an integer

    Checks if input string can be turned into an integer

    :param s: input string
    :type s: str
    :return: True if input can be turned into an integer
        False otherwise
    :rtype: bool
    """

    try:
        out = int(s)
    except:
        return False
    return True


def is_float(s: str) -> bool:
    """ Checks if input string can be turned into an float

    Checks if input string can be turned into an float

    :param s: input string
    :type s: str
    :return: True if input can be turned into an float
        False otherwise
    :rtype: bool
    """

    try:
        out = float(s)
    except:
        return False
    return True


def split_high_level(s: str,
                     c: str,
                     open_chars: List[str],
                     close_chars: List[str]
                     ) -> List[str]:
    """Splits input string by delimiter c.

    Splits input string by delimiter c excluding occurences
    of character c that are between open_chars close_chars

    :param s: string to split
    :type s: str
    :param c: delimiter character
    :type c: str
    :param open_chars: list of block opening characters
    :type open_chars: List[str]
    :param close_chars: list of block closing characters
    :type close_chars: List[str]
    :return: list of strings containing the splitted blocks
    :rtype: List[str]
    """

    splits = []
    index = 0
    depth = 0
    start = 0
    while index < len(s) - 1:
        index += 1
        if s[index] in open_chars:
            depth += 1
        elif s[index] in close_chars:
            depth -= 1
        if depth == 0 and s[index] == c:
            splits.append(s[start:index:])
            start = index + 1
    else:
        if start < len(s) - 1:
            splits.append(s[start::])
    return splits


def split_first_identifier(s: str) -> (str, str):
    """splits sting into the first identifier and the rest

    Extracts the first substring that can be considered an identifier
    Returns the identifier and the rest

    :param s: string to split
    :type s: str
    :return: Returns two strings, first identifier and the rest
    :rtype: (str,str)
    """

    valid_chars = string.ascii_letters + string.digits + '_'
    index = 0
    while index < len(s) and s[index] in valid_chars:
        index += 1
    return s[:index:], s[index::]


def str2key(s: str) -> Union[int, float, str]:
    """turn a string into a possible dict key

    turn a string into a possible dict key

    :param s: input string
    :type s: str
    :return: out dict key. Can be either int, float or str
    :rtype: Union[int, float, str]
    """

    s = s.replace(' ', '')
    if is_float(s):
        if is_int(s):
            return int(s)
        else:
            return float(s)
    else:
        s = s.replace("'", "")
        s = s.replace('"', '')
        return s


def split_type_or_type(s: str) -> List[str]:
    """separates all possible types for a var

    separates all possible types for a var

    :param s: input string
    :type s: str
    :return: list of strings with types
    :rtype: List[str]
    """
    types = split_high_level(
        s,
        '|',
        ["(", "[", "{"],
        [")", "]", "}"]
    )
    return types


def separate_list_types(s: str) -> List[str]:
    """separate all types of a list type string

    separate all types of a list type string

    :param s: input string
    :type s: str
    :return: list of strings with types
    :rtype: List[str]
    """

    types = split_high_level(
        s,
        ',',
        ["(", "[", "{"],
        [")", "]", "}"]
    )
    return types


def separate_keys(s: str) -> (List[str], List[str]):
    """separate all keys and types of a dict type string

    separate all keys and types of a dict type string

    :param s: input string
    :type s: str
    :return: list of strings with keys, list of strings with types
    :rtype: List[str], List[str]
    """

    keys = []
    types = []
    dict_elements = split_high_level(
        s,
        ',',
        ["(", "[", "{"],
        [")", "]", "}"]
    )
    for dict_elem in dict_elements:
        key_type = split_high_level(
            dict_elem,
            ':',
            ["(", "[", "{"],
            [")", "]", "}"]
        )
        keys.append(str2key(key_type[0]))
        types.append(key_type[1])

    return keys, types


def get_subblock(s: str, open_c: str, close_c: str) -> (str, str):
    """returns a subblock enclosed by open_c and close_c

    returns a subblock enclosed by open_c and close_c

    :param s: input string
    :type s: str
    :param open_c: block opening character
    :type open_c: char
    :param close_c: block closing character
    :type close_c: char
    :raises Exception: when the first char is not an opening char
    :raises Exception: there is no closing char
    :return: block, rest of string
    :rtype: (str, str)
    """

    if s[0] != open_c:
        raise Exception(
            'Input string is expected to begin with opening character: ',
            open_c,
            'But it begins with ',
            s[0]
        )
    index = 1
    depth = 1
    while index < len(s):
        index += 1
        if s[index] == open_c:
            depth += 1
        elif s[index] == close_c:
            depth -= 1
        if depth == 0:
            break
    else:
        raise Exception('No closing', close_c, ' for opening',
                        open_c, 'in string: ', s)
    return s[1:index:], s[index + 1::]


def check_type(v: Any, t: str) -> None:
    """Checks if the input variable v is of type t

    Checks if the input variable v is of type t

    :param v: input variable
    :type v: Any
    :param t: input type
    :type t: str
    :raises Exception: when input variable v is NOT of type t
    :return: nothing
    :rtype: None
    """

    if v.__class__.__name__ != t:
        raise Exception(v, " is not of type ", t)


def check_complete_keys(keys: List[Any], dictionary: Dict):
    """checks if the input keys are complete for input dictionary

    checks if the input keys are complete for input dictionary

    :param keys: list of keys
    :type keys: List[Any]
    :param dictionary: input dictionary
    :type dictionary: Dict
    :raises Exception: when input keys are not complete for input dict
    """

    if set(keys) != set(dictionary.keys()):
        raise Exception(
            "type string doesn't have a complete set of keys for dict",
            dictionary
        )


def type_gen(types: List[str]) -> Generator[str, None, None]:
    """Generator that yields types from input type list, considering '...'

    Generator that yields types from input type list, considering '...'

    :param types: list of string types
    :type types: List[str]
    :return: yields type strings
    :rtype: Generator[str, None, None]
    """

    t_i = 0
    while t_i < len(types):
        if types[t_i] == '...':
            t_i = 0
            yield types[t_i]
            t_i += 1
        elif types[t_i][-3::] == '...':
            yield types[t_i][:-3:]
        else:
            yield types[t_i]
            t_i += 1
    # If reached the end, raise error
    yield('Type string "' + " , ".join(types) + '" is missing types')


def verify(var: Any, type_str: str) -> None:
    """veryfy variable type recursively

    check if input variable is of type type string.
    If not, an exception is risen

    then if var contains subtypes (e.g.: list of ints)
    descend into subbars and recursively call itself.

    :param var: variable to test
    :type var: Any
    :param type_str: string with complete types and subtypes to test
    :type type_str: str
    :raises Exception: when more subtypes are input
    :raises Exception: when extra types at the end are input
    :return: nothing
    :rtype: None
    """

    # Remove all spaces
    type_str = type_str.replace(' ', '')

    # Remove all new lines
    type_str = type_str.replace('\n', '')

    # Remove all tabs
    type_str = type_str.replace('\t', '')

    # Extract types
    types = split_type_or_type(type_str)
    if len(types) > 1:
        if any([verify_bool(var, t) for t in types]):
            return
        else:
            raise Exception(var, " is not of any of: ", types)

    # split the string into first word and rest of str
    curtype, rest = split_first_identifier(type_str)

    # Check that the input variable is of given type
    check_type(var, curtype)

    if curtype == 'dict' or (len(rest) > 0 and rest[0] == '{'):
        # Get subblock of type
        sub_block, rest = get_subblock(rest, '{', '}')

        # From the sub-block extract the keys and the expected types
        keys, types = separate_keys(sub_block)

        # Check if the set of keys are complete for the input dict
        check_complete_keys(keys, var)

        # For each key in input dict call verify recursively
        for key, val_type in zip(keys, types):
            verify(var[key], val_type)

    elif curtype == 'list' or (len(rest) > 0 and rest[0] == '['):
        # Get subblock of type
        sub_block, rest = get_subblock(rest, '[', ']')

        # Extract types
        types = separate_list_types(sub_block)

        # Check enough values for types
        min_len = reduce(lambda x, y: x + 1 if y != '...' else x, [0] + types)
        if len(var) < min_len:
            raise Exception(
                "More types defined in:\n    ", sub_block,
                "\nThat positions in variable:\n    ", var
            )

        # For each position call verify recursively
        # type_gen is a generator that returns types intelligently
        #     considering the '...' in the strings
        for v, t in zip(var, type_gen(types)):
            verify(v, t)

        # Raise exception if extra types present at the end
    elif len(rest) != 0:
        raise Exception(
            "End of typestring contains extra characters: ",
            rest
        )


def verify_bool(var: Any, type_str: str) -> bool:
    """Wrapper around veryfy to return bool

    check if input variable is of type type string.
    If not, False is returned

    :param var: variable to test
    :type var: Any
    :param type_str: string with complete types and subtypes to test
    :type type_str: str
    :return: True if variable is of typ type_str,
        False otherwise
    :rtype: bool
    """
    try:
        verify(var, type_str)
        return True
    except:
        return False


def is_type_ok(var: Any, type_str: str) -> (bool, str):
    """checks if type of variable is correct

    wrapper around validate that returns valid and error string

    :param var: variable to check
    :type var: Any
    :param type_str: string containing type to check
    :type type_str: str
    :return: (True, "") or (False, errorstr) if invalid type
    :rtype: (bool, str)
    """

    try:
        verify(var, type_str)
    except Exception as e:
        return False, str(e)

    return True, ""
