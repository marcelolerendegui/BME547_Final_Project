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

from pymodm import connect, MongoModel, fields
import os
from server.database_model import Image
from bson import ObjectId


def init():
    """ connect to online database

    connect to online database

    """

    mdb_user = 'xinyihang1'  # os.environ.get('MONGODB_USER')
    mdb_pass = '19950301'  # os.environ.get('MONGODB_PASS')

    connection_str = "".join([
        "mongodb+srv://",
        mdb_user,
        ":",
        mdb_pass,
        "@bme547-q262c.mongodb.net/Database"
    ])
    connect(connection_str)


def add_image(
    filename: str = None,
    img_format: str = None,
    description: str = None,
    size: str = None,
    timestamp=None,
    data: str = None,
    user_hash: str = None
) -> bool:
    """add image to database

    add image to database

    :param u: image to add
    :type u: Image
    :return: True on success, False otherwise
    :rtype: bool
    """

    image_to_add = Image(
        filename=filename,
        img_format=img_format,
        description=description,
        size=size,
        timestamp=timestamp,
        data=data,
        user_hash=user_hash,
    )

    try:
        image_to_add.save()
    except:
        return False
    return True


def image_exists(image_id: str, user_hash: str) -> bool:
    """check if image already exists

    check if image already exists

    :param pid: image id to check
    :type pid: str
    :return: True if image exists, False otherwise
    :rtype: bool
    """

    image = get_image(image_id, user_hash)
    return image is not None


def get_image(image_id: str, user_hash: str) -> Image:
    """fetch image by image id

    fetch image by image id

    :param pid: image id to fetch
    :type pid: str
    :return: image on success, None otherwise
    :rtype: Image
    """

    try:
        image = Image.objects.raw({'_id': ObjectId(image_id)}).first()
        if image.user_hash != user_hash:
            image = None
    except:
        image = None
    return image


def get_all_user_images(user_hash: str):
    try:
        image = Image.objects.raw({'user_hash': user_hash})
    except:
        image = None
    return image
