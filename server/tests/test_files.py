from server.files import fio_to_b64s
from server.files import b64s_to_fio
from server.files import fio_to_s
from server.files import s_to_fio

import pytest


def test_conversion():
    in_message = 'This is a Message!'
    in_fio = s_to_fio(in_message)

    b64 = fio_to_b64s(in_fio)

    out_fio = b64s_to_fio(b64)
    out_message = fio_to_s(out_fio)

    assert out_message == in_message


@pytest.mark.parametrize(
    "in_s",
    [
        ('0123456789'),
        ('abcdefghijklmnopqrstuvwxyz'),
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        ('~!@#$%^&*()_+=[]{};:",.<>/?'),
        ("~!@#$%^&*()_+=[]{};:',.<>/?"),
        ('0123456789abcdefghijABCDEFGHIJ~!@#$%^&*(~!@#$%^&*('),
    ]
)
def test_s_b_s(in_s):
    from server.files import s_to_b
    from server.files import b_to_s

    b = s_to_b(in_s)
    out_s = b_to_s(b)

    assert out_s == in_s


def test_s_b64s_s():
    from server.files import s_to_b64s
    from server.files import b64s_to_s

    in_s = 'This is a Message!'
    b64s = s_to_b64s(in_s)
    out_s = b64s_to_s(b64s)

    assert out_s == in_s


def test_s_fio_s():
    from server.files import s_to_fio
    from server.files import fio_to_s

    in_s = 'This is a Message!'
    fio = s_to_fio(in_s)
    out_s = fio_to_s(fio)

    assert out_s == in_s


def test_s_b_b64s_b_s():
    from server.files import s_to_b
    from server.files import b_to_b64s
    from server.files import b64s_to_b
    from server.files import b_to_s

    in_s = 'This is a Message!'
    b = s_to_b(in_s)
    b64s = b_to_b64s(b)
    out_b = b64s_to_b(b64s)
    out_s = b_to_s(out_b)

    assert out_s == in_s


def test_s_b_b64s_fio_b64s_b_s():
    from server.files import s_to_b
    from server.files import b_to_b64s
    from server.files import b64s_to_fio
    from server.files import fio_to_b64s
    from server.files import b64s_to_b
    from server.files import b_to_s

    in_s = 'This is a Message!'
    b = s_to_b(in_s)
    b64s = b_to_b64s(b)
    fio = b64s_to_fio(b64s)
    out_b64s = fio_to_b64s(fio)
    out_b = b64s_to_b(out_b64s)
    out_s = b_to_s(out_b)

    assert out_s == in_s
