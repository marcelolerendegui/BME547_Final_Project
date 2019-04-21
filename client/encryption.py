from hashlib import sha256


def get_userhash(username: str, password: str) -> str:
    original_word = "".join([username, password]).encode('utf8').rstrip()
    return sha256(original_word).hexdigest()
