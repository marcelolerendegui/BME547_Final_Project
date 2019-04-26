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

import pytest


@pytest.mark.parametrize(
    "val, expected",
    [
        ('2', True),
        ('4.0', False),
        ('4.7', False),
        ('3a', False),
        ('a', False),
        ('.11', False),
        ('1 2', False),
        ('1,2', False),
    ]
)
def test_is_int(val, expected):
    from client.verification import is_int
    assert is_int(val) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        ('1.0', True),
        ('1.023123124', True),
        ('11312.023123124', True),
        ('+11312.023123124', True),
        ('-11312.023123124', True),
        ('+11312.023123124E-3', True),
        ('-0.023123124E-4', True),
        ('1.0.1', False),
        ('1.0a23', False),
        ('g.01231', False),
        ('-+1.2', False),
        ('1.2E-+1', False),
        ('', False),
        (' ', False),
    ]
)
def test_is_float(val, expected):
    from client.verification import is_float
    assert is_float(val) == expected


@pytest.mark.parametrize(
    "s, c, open_chars, close_chars, splits",
    [
        (
            "1,2.0,'3','4.0'",
            ",",
            ["[", "{", "("],
            ["]", "}", ")"],
            ["1", "2.0", "'3'", "'4.0'"]
        ),
        (
            "1,(2.0,'3'),'4.0'",
            ",",
            ["[", "{", "("],
            ["]", "}", ")"],
            ["1", "(2.0,'3')", "'4.0'"]
        ),
        (
            "1,[2.0,'3'],'4.0'",
            ",",
            ["[", "{", "("],
            ["]", "}", ")"],
            ["1", "[2.0,'3']", "'4.0'"]
        ),
        (
            "1,{2.0,'3'},'4.0'",
            ",",
            ["[", "{", "("],
            ["]", "}", ")"],
            ["1", "{2.0,'3'}", "'4.0'"]
        ),
        (
            "1,{[2,3],3},[2],[2,{[1],[2]}],'str','strinng'",
            ",",
            ["[", "{", "("],
            ["]", "}", ")"],
            ["1", "{[2,3],3}", "[2]", "[2,{[1],[2]}]", "'str'", "'strinng'"]
        ),
    ]
)
def test_split_high_level(s, c, open_chars, close_chars, splits):
    from client.verification import split_high_level
    lst = split_high_level(s, c, open_chars, close_chars)
    for l, s in zip(lst, splits):
        assert l == s


@pytest.mark.parametrize(
    "s, exp1, exp2",
    [
        ('dict("key":str, "other_key":float)',
         'dict', '("key":str, "other_key":float)'),
        ('asdf$asdas',
         'asdf', '$asdas'),
        ('My_identifier1_{int}',
         'My_identifier1_', '{int}'),
    ]
)
def test_split_first_identifier(s, exp1, exp2):
    from client.verification import split_first_identifier
    t1, t2 = split_first_identifier(s)
    assert t1 == exp1 and t2 == exp2


@pytest.mark.parametrize(
    "s, key",
    [
        ("'key'", 'key'),
        ("'key '", 'key'),
        ("' key'", 'key'),
        ("' key '", 'key'),

        ('"key"', 'key'),
        ('"key "', 'key'),
        ('" key"', 'key'),
        ('" key "', 'key'),

        ('"key1"', 'key1'),
        ('"1key "', '1key'),
        ('" key2"', 'key2'),
        ('" 2key "', '2key'),

        ('1', 1),
        ('2 ', 2),
        (' 3', 3),
        (' 4 ', 4),

        ('-5', -5),
        ('-6 ', -6),
        (' -7', -7),
        (' -8 ', -8),

        ('1.0', 1.0),
        ('2.1 ', 2.1),
        (' 3.2', 3.2),
        (' 4.3 ', 4.3),

        ('-5.4', -5.4),
        ('-6.5 ', -6.5),
        (' -7.6', -7.6),
        (' -8.7 ', -8.7),
    ]
)
def test_str2key(s, key):
    from client.verification import str2key
    assert str2key(s) == key


@pytest.mark.parametrize(
    "s, splits",
    [
        (
            "1,2.0,'3','4.0'",
            ["1", "2.0", "'3'", "'4.0'"]
        ),
        (
            "1,(2.0,'3'),'4.0'",
            ["1", "(2.0,'3')", "'4.0'"]
        ),
        (
            "1,[2.0,'3'],'4.0'",
            ["1", "[2.0,'3']", "'4.0'"]
        ),
        (
            "1,{2.0,'3'},'4.0'",
            ["1", "{2.0,'3'}", "'4.0'"]
        ),
        (
            "1,{[2,3],3},[2],[2,{[1],[2]}],'str','strinng'",
            ["1", "{[2,3],3}", "[2]", "[2,{[1],[2]}]", "'str'", "'strinng'"]
        ),
    ]
)
def test_separate_list_types(s, splits):
    from client.verification import separate_list_types
    lst = separate_list_types(s)
    for l, s in zip(lst, splits):
        assert l == s


@pytest.mark.parametrize(
    "s, ekeys, etypes",
    [
        (
            "'key1':type1,'key2':type2,'key3':type3,'key4':type4",
            ['key1', 'key2', 'key3', 'key4'],
            ["type1", "type2", "type3", "type4"],
        ),
        (
            "1:type1,2:type2,3:type3,4:type4",
            [1, 2, 3, 4],
            ["type1", "type2", "type3", "type4"],
        ),
        (
            "1.0:type1,2.0:type2,3.0:type3,4.0:type4",
            [1.0, 2.0, 3.0, 4.0],
            ["type1", "type2", "type3", "type4"],
        ),
        (
            "'key1':type1,2:type2,3.0:type3,'4.0':type4",
            ['key1', 2, 3.0, '4.0'],
            ["type1", "type2", "type3", "type4"],
        ),
    ]
)
def test_separate_keys(s, ekeys, etypes):
    from client.verification import separate_keys
    keys, types = separate_keys(s)
    for k, ek in zip(keys, ekeys):
        assert k == ek
    for t, et in zip(types, etypes):
        assert t == et


@pytest.mark.parametrize(
    "s, open_c, close_c, eout, eexc",
    [
        (
            "[1,2,3]",
            "[",
            "]",
            "1,2,3",
            False
        ),
        (
            "[1,[2],[3]]",
            "[",
            "]",
            "1,[2],[3]",
            False
        ),
        (
            "[1,[2],[3]]",
            "[",
            "]",
            "1,[2],[3]",
            False
        ),
        (
            "[1,[2],[3]]",
            "{",
            "}",
            None,
            True
        ),
    ]
)
def test_get_subblock(s, open_c, close_c, eout, eexc):
    from client.verification import get_subblock

    if eexc:
        with pytest.raises(Exception):
            out1, out2 = get_subblock(s, open_c, close_c)
    else:
        out1, out2 = get_subblock(s, open_c, close_c)
        assert out1 == eout


@pytest.mark.parametrize(
    "t, v, eexc",
    [
        ("int", 1, False),
        ("float", 1.0, False),
        ("str", '1.0', False),
        ("list", [1], False),
        ("dict", {1: 1, 2: 2}, False),
        ("int", 1.0, True),
        ("imt", 1.0, True),
        ("flout", 1.0, True),
    ]
)
def test_check_type(t, v, eexc):
    from client.verification import check_type
    if eexc:
        with pytest.raises(Exception):
            check_type(v, t)
    else:
        check_type(v, t)


@pytest.mark.parametrize(
    "keys, dict, eexc",
    [
        (['key1', 'key2', 'key3'], {'key1': 1, 'key2': 2, 'key3': 3}, False),
        ([1, 2, 3], {1: 1, 2: 2, 3: 3}, False),
        ([1.0, 2.0, 3.0], {1.0: 1, 2.0: 2, 3.0: 3}, False),
        ([1, 2.0, '3.0'], {1: 1, 2.0: 2, '3.0': 3}, False),
        (['key1', 'key2', 'key3'], {'key1': 1, 'key2': 2}, True),
        (['key1', 'key2'], {'key1': 1, 'key2': 2, 'key3': 3}, True),
    ]
)
def test_check_complete_keys(keys, dict, eexc):
    from client.verification import check_complete_keys
    if eexc:
        with pytest.raises(Exception):
            check_complete_keys(keys, dict)
    else:
        check_complete_keys(keys, dict)


@pytest.mark.parametrize(
    "s, etypes, eexc",
    [
        # Correct
        # Single
        (["int"], ['int'], False),
        (["float"], ['float'], False),
        (["str"], ['str'], False),
        (["list[int]"], ['list[int]'], False),

        # Single repeated
        (["int..."], ['int']*100, False),
        (["float..."], ['float']*100, False),
        (["str..."], ['str']*100, False),
        (["list[int]..."], ['list[int]']*100, False),

        # Double
        (["int", "float"], ['int', 'float'], False),
        (["float", "str"], ['float', 'str'], False),
        (["str", "list[int]"], ['str', 'list[int]'], False),
        (["list[int]", "int"], ['list[int]', 'int'], False),

        # Double (last repeated)
        (["int", "float..."], ['int'] + ['float']*100, False),
        (["float", "str..."], ['float'] + ['str']*100, False),
        (["str", "list[int]..."], ['str'] + ['list[int]']*100, False),
        (["list[int]", "int..."], ['list[int]'] + ['int']*100, False),

        # Double (all repeated)
        (["int", "float", "..."], ['int', 'float']*100, False),
        (["float", "str", "..."], ['float', 'str']*100, False),
        (["str", "list[int]", "..."], ['str', 'list[int]']*100, False),
        (["list[int]", "int", "..."], ['list[int]', 'int']*100, False),

        # Multiple (last repeated)
        (
            ["int", "float", "str..."],
            ['int', 'float'] + ['str']*100,
            False,
        ),
        (
            ["float", "str", "list[int]..."],
            ['float', 'str'] + ['list[int]']*100,
            False,
        ),
        (
            ["str", "list[int]", "int..."],
            ['str', 'list[int]'] + ['int']*100,
            False,
        ),
        (["list[int]", "int", "float..."],
            ['list[int]', 'int'] + ['float']*100,
            False
         ),

        # Multiple (all repeated)
        (
            ["int", "float", "str", "..."],
            ['int', 'float', 'str']*100,
            False
        ),
        (
            ["float", "str", "list[int]", "..."],
            ['float', 'str', 'list[int]']*100,
            False
        ),
        (
            ["str", "list[int]", "int", "..."],
            ['str', 'list[int]', 'int']*100,
            False
        ),
        (["list[int]", "int", "float", "..."],
            ['list[int]', 'int', 'float']*100,
            False
         ),

        # Incorrect
        (["int"], ['int', 'float'], True),
    ]
)
def test_type_gen(s, etypes, eexc):
    from client.verification import type_gen
    if eexc:
        with pytest.raises(Exception):
            for t, et in zip(type_gen(s), etypes):
                assert t == et
    else:
        for t, et in zip(type_gen(s), etypes):
            assert t == et


class My_class_L(list):
    def __init__(self, *args):
        super(My_class_L, self).__init__(*args)

    def __getitem__(self, key):
        return super(My_class_L, self).__getitem__(key)


class My_class_D(dict):
    def __init__(self, *args):
        super(My_class_D, self).__init__(*args)

    def __getitem__(self, key):
        return super(My_class_D, self).__getitem__(key)


@pytest.mark.parametrize(
    "str_type, var, must_raise",
    [
        # Correct Calls
        # Built in basic
        ("int",     1,      False),
        ("float",   1.0,    False),
        ("str",     '1',    False),

        # Lists
        (
            "list[int]",
            [1],
            False,
        ),
        (
            "list[int, float]",
            [1, 2.0],
            False,
        ),
        (
            "list[int, float, str]",
            [1, 2.0, '3.0'],
            False,
        ),
        (
            "list[int...]",
            [1, 2, 3],
            False,
        ),
        (
            "list[int, float...]",
            [1, 2.0, 3.0],
            False,
        ),
        (
            "list[int, float, str...]",
            [1, 2.0, '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0'],
            False,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0, '3.0', 4, 5.0, '6.0', 7, 8.0, '9.0', 10, 11.0, '12,0'],
            False,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0, '3.0', 4, 5.0, '6.0', 7, 8.0, '9.0', 10, 11.0],
            False,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0, '3.0', 4, 5.0, '6.0', 7, 8.0, '9.0', 10],
            False,
        ),
        (
            "list[list[int...], list[float...], list[str...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], ['1.0', '2.0', '3.0'], [
                4, 5, 6], [4.0, 5.0, 6.0], ['4.0', '5.0', '6.0']],
            False,
        ),
        (
            "list[list[int...], list[float...], list[str...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], ['1.0', '2.0', '3.0'],
                [4, 5, 6], [4.0, 5.0, 6.0]],
            False,
        ),
        (
            "list[list[int...], list[float...], list[str...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], ['1.0', '2.0', '3.0'], [4, 5, 6]],
            False,
        ),

        # Dicts
        (
            "dict{1:int, 2.0:float, '3':str}",
            {1: 123, 2.0: 3.1415, '3': 'string '},
            False,
        ),
        (
            "dict{1:list[int...], 2.0:list[float...], 'three':list[str...]}",
            {1: [1, 2, 3], 2.0:[1.0, 2.0, 3.0],
                'three':['one', 'two', 'three']},
            False,
        ),

        # User Defined types
        (
            "My_class_L",
            My_class_L(),
            False,
        ),
        (
            "My_class_L[int,...]",
            My_class_L([1, 2, 3, 4]),
            False,
        ),
        (
            "My_class_L[int, float...]",
            My_class_L([1, 2.0, 3.0, 4.0]),
            False,
        ),
        (
            "My_class_L[int,My_class_L[int...]]",
            My_class_L([1, My_class_L([2, 3, 4])]),
            False,
        ),

        (
            "My_class_D",
            My_class_D([]),
            False,
        ),

        (
            "My_class_D{'1':str, 'two':int, 3:float}",
            My_class_D({'1': 'one', 'two': 2, 3: 3.0}),
            False,
        ),

        (
            """
            My_class_D{
                'key1': My_class_D{'k1':int,'k2':float,'k3':str},
                'key2': My_class_D{'k1':str,'k2':int,'k3':float},
                'key3': My_class_D{'k1':float,'k2':str,'k3':int},
                3:float
            }
            """,
            My_class_D({
                'key1': My_class_D({'k1': 1, 'k2': 2.0, 'k3': 'three'}),
                'key2': My_class_D({'k1': 'one', 'k2': 2, 'k3': 3.0}),
                'key3': My_class_D({'k1': 1.0, 'k2': 'two', 'k3': 3}),
                3: 123.4
            }),
            False
        ),

        # Multiple types
        (
            "list[int, float|str...]",
            [1, 2.0, 3.0, 4.0, 5.0],
            False,
        ),

        (
            "list[int, float|str...]",
            [1, '2.0', '3.0', '4.0', '5.0'],
            False,
        ),

        (
            "list[int, float|str...]",
            [1, 2.0, 3.0, '4', 5.0, '6.0', '7.0', 8.0, 9.0, '10'],
            False,
        ),

        (
            "list[int, str...] | list[int, float...]",
            [1, '2.0', '3.0', '4.0', '5.0'],
            False,
        ),

        (
            "list[int, str...] | list[int, float...]",
            [1, 2.0, 3.0, 4.0, 5.0],
            False,
        ),

        (
            "list[int, str...] | list[int, float...]",
            [1, 2.0, 3, '4', 5, '6.0', 7, 8.0, 9, '10'],
            True,
        ),

        # Complex nested types
        (
            """
            dict {
                1 : dict{
                        "first_key" : list [int...],
                        "second_key" : str,
                        3 : list[int, str, float, str...]
                    },
                2: list[int, list[float...], ...] ,
                'tres': My_class_L[float]
            }
            """,
            {
                1: {
                    "first_key": [1, 2, 3, 4, ],
                    "second_key": '2key',
                    3: [1, '2', 3.0, 'h', 'e', 'll', 'oooo', ],
                },
                2: [
                    1, [1.0],
                    2, [1.0, 2.0],
                    3, [1.0, 2.0, 3.0],
                    4, [1.0, 2.0, 3.0, 4.0],
                ],
                'tres': My_class_L([3.1415])
            },
            False,
        ),



        # Incorrect Calls
        # Wrong type
        ("int",     1.0,      True),
        ("float",   '1',    True),
        ("str",     1,    True),

        # Lists
        # Missing types
        (
            "list[int]",
            [1, 1, 1],
            True,
        ),
        (
            "list[int, float]",
            [1, 2.0, '1'],
            True,
        ),
        (
            "list[int, float, str]",
            [1, 2.0, '3.0', 'string'],
            True,
        ),
        (
            "list[int...]",
            [1, 2, 3.0],
            True,
        ),
        (
            "list[int, float...]",
            [1, '1', 2.0, 3],
            True,
        ),
        (
            "list[int, float, str...]",
            [1, 2.0, '3.0', '4.0', '5.0', '6.0', 7.0, '8.0', '9.0'],
            True,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0, '3.0', 4, 5.0, '6.0', 7, 8.0, '9.0', 10.0, 11, '12,0'],
            True,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0, '3.0', 4, 5.0, '6.0', 7, 8.0, '9.0', 10, 11.0, 12.0],
            True,
        ),
        (
            "list[int, float, str, ...]",
            [1, 2.0],
            True,
        ),
        (
            "list[list[int...], list[float...], list[str...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], [1.0, '2.0', '3.0'], [
                4, 5, 6], [4.0, 5.0, 6.0], ['4.0', '5.0', '6.0']],
            True,
        ),

        # Type Typo
        (
            "list[list[int...], list[floats...], list[str...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], ['1.0', '2.0', '3.0'],
                [4, 5, 6], [4.0, 5.0, 6.0]],
            True,
        ),
        (
            "list[list[imt...], list[float...], list[stiring...], ...]",
            [[1, 2, 3], [1.0, 2.0, 3.0], ['1.0', '2.0', '3.0'], [4, 5, 6]],
            True,
        ),

        # Dicts
        # Wrong Keys
        (
            "dict{1:int, 2.0:float, '3':str}",
            {1: 123, 2.0: 3.1415, 3: 'string '},
            True,
        ),
        (
            "dict{1:list[int...], 2.0:list[float...], 'three':list[str...]}",
            {1: [1, 2, 3], '2.0':[1.0, 2.0, 3.0],
                'three':['one', 'two', 'three']},
            True,
        ),

    ]
)
def test_verify(str_type, var, must_raise):
    from client.verification import verify

    if must_raise:
        with pytest.raises(Exception):
            verify(var, str_type)
    else:
        verify(var, str_type)


@pytest.mark.parametrize(
    "str_type, var, expected",
    [
        (
            "My_class_D{'1':str, 'two':int, 3:float}",
            My_class_D({'1': 'one', 'two': 2, 3: 3.0}),
            True,
        ),
    ]
)
def test_is_type_ok(str_type, var, expected):
    from client.verification import is_type_ok
    valid, errorstr = is_type_ok(var, str_type)
    assert valid == expected
