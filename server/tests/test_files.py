from server.files import fio_to_b64s
from server.files import b64s_to_fio
from server.files import fio_to_s
from server.files import s_to_fio


import io


def test_conversion():
    in_message = 'This is a Message!'
    in_fio = s_to_fio(in_message)

    b64 = fio_to_b64s(in_fio)

    out_fio = b64s_to_fio(b64)
    out_message = fio_to_s(out_fio)

    assert out_message == in_message
