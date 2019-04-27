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
