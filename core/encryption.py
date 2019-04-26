from hashlib import sha256


def get_userhash(username: str, password: str) -> str:
    """
    generate a username/password combined MD5 hash for encryption
    :param username: login user name set by user
    :type username: str
    :param password: login password set by user
    :type password: str
    :return: encoded SHA256 hash for database
    :rtype: str
    """
    original_word = "".join([username, password]).encode('utf8').rstrip()
    return sha256(original_word).hexdigest()
