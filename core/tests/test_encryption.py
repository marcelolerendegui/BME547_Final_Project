import pytest


# from https://emn178.github.io/online-tools/sha256.html
@pytest.mark.parametrize(
    "usr, psswrd, expected",
    [
        (
            'USER',
            'PASSWORD',
            'b6cc6e33521c51850051d61f00fa874fff308901608c1349552ac8b52ebe3c9a',
        ),
        (
            'u53RN4M3',
            '!mypasswordisthebest123',
            '9fc63750e3018c1d8ad12b174b6f2ce39e0ddf68f32edd2f6709519f8a7b073d',
        ),
        (
            '112131415161',
            'This is a password with spaces!',
            '1c212523910852de72cacee246fa80c7af0497ce3d0a7d7a85a95224fdc4af00',
        ),
        (
            """uSeR 1 23!@#$%^&*()_+][}'"{;:/.,?><""",
            """PaSs~!@#  $%^&*'';"'()_+~[]{}""",
            'e9df52db8290b9af33d9d299109d7360a426480b91e8a7465599f4430fa88e6d',
        ),
    ]
)
def test_get_userhash(usr, psswrd, expected):
    from core.encryption import get_userhash
    out = get_userhash(usr, psswrd)
    assert out == expected
