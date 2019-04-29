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
import json
import requests
import base64
from PIL import Image
from io import BytesIO
from core.verification import is_type_ok

api_host = "http://127.0.0.1:5000"


def apply_algorithm(
    image_id: str,
    algorithm: str,
    im_format: str,
    out_filename: str,
    user_hash: str
) -> dict:
    """Apply an image processing algorithm ot an image

    :param image_id: id of the image to process
    :type image_id: str
    :param algorithm: algorithm to apply
    :type algorithm: str
    :param im_format: format of the output image
    :type im_format: str
    :param out_filename: name of the output image
    :type out_filename: str
    :param user_hash: hash identifying a user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate image_id type
    t_ok, t_err = is_type_ok(image_id, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate algorithm type
    t_ok, t_err = is_type_ok(algorithm, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate im_format type
    t_ok, t_err = is_type_ok(im_format, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate out_filename type
    t_ok, t_err = is_type_ok(out_filename, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    d = {
        'image_id': image_id,
        'algorithm': algorithm,
        'out_image_format': im_format,
        'out_image_filename': out_filename,
        'user_hash': user_hash,
    }
    try:
        r = requests.post(api_host+"/api/image_process", json=d)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def get_download_images(
    image_ids: list,
    im_format: str,
    user_hash: str
) -> dict:
    """run a get request to download images

    :param image_ids: list of ids to download
    :type image_ids: list
    :param im_format: format to download
    :type im_format: str
    :param user_hash: hash identifying user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate image_ids type
    t_ok, t_err = is_type_ok(image_ids, "list[str, ...]")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate im_format type
    t_ok, t_err = is_type_ok(im_format, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    d = {
        'image_ids': image_ids,
        'format': im_format,
        'user_hash': user_hash
    }
    try:
        r = requests.get(api_host+"/api/download/", json=d)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def get_single_image(image_id: str, user_hash: str) -> dict:
    """get single image from server

    :param image_id: id of the image to download
    :type image_id: str
    :param user_hash: hash identifying user
    :type user_hash: str
    :return: dictionary with the info. see protocol
    :rtype: dict
    """
    # Validate image_id type
    t_ok, t_err = is_type_ok(image_id, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    d = {
        'image_ids': [image_id],
        'format': 'PNG',
        'user_hash': user_hash
    }
    try:
        r = requests.get(api_host+"/api/download/", json=d)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def get_images_info(user_hash: str) -> dict:
    """get information of all the images that belong to the user

    :param user_hash: hash identifying a user
    :type user_hash: str
    :return: dictionary with all the info. see protocol
    :rtype: dict
    """
    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    try:
        r = requests.get(api_host + '/api/image_info/' + user_hash)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def upload_image(image_b64s: str, filename: str, user_hash: str) -> dict:
    """upload a single image to the server

    :param image_b64s: image data as a base 64 string
    :type image_b64s: str
    :param filename: filename for the image
    :type filename: str
    :param user_hash: hash identifying the user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate image_b64s type
    t_ok, t_err = is_type_ok(image_b64s, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate filename type
    t_ok, t_err = is_type_ok(filename, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    d = {
        'filename': filename,
        'user_hash': user_hash,
        'description': filename,
        'data': image_b64s,
    }
    try:
        r = requests.post(api_host+"/api/upload/image", json=d)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def upload_zip(zip_b64s: str, filename: str, user_hash: str) -> dict:
    """upload multiple images as a zip

    :param zip_b64s: zip file data as a base 64 string
    :type zip_b64s: str
    :param filename: filename of the zip
    :type filename: str
    :param user_hash: hash identifying a user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate zip_b64s type
    t_ok, t_err = is_type_ok(zip_b64s, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate filename type
    t_ok, t_err = is_type_ok(filename, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    d = {
        'filename': filename,
        'user_hash': user_hash,
        'data': zip_b64s,
    }
    try:
        r = requests.post(api_host+"/api/upload/zip", json=d)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def edit_filename(image_id: str, new_fname: str, user_hash: str) -> dict:
    """edit filename of an image

    :param image_id: id of the image to edit
    :type image_id: str
    :param new_fname: new filename for the image
    :type new_fname: str
    :param user_hash: hash identifying a user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate image_id type
    t_ok, t_err = is_type_ok(image_id, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate new_fname type
    t_ok, t_err = is_type_ok(new_fname, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    data = {
        'image_id': image_id,
        'filename': new_fname,
        'user_hash': user_hash
    }
    try:
        r = requests.post(api_host + '/api/edit/filename', json=data)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def edit_description(image_id: str, new_desc: str, user_hash: str) -> dict:
    """edit description of an image

    :param image_id: id of the image to edit
    :type image_id: str
    :param new_desc: new description for the image
    :type new_desc: str
    :param user_hash: hash identifying a user
    :type user_hash: str
    :return: dictionary with info. see protocol
    :rtype: dict
    """
    # Validate image_id type
    t_ok, t_err = is_type_ok(image_id, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate new_desc type
    t_ok, t_err = is_type_ok(new_desc, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    data = {
        'image_id': image_id,
        'description': new_desc,
        'user_hash': user_hash
    }
    try:
        r = requests.post(api_host + '/api/edit/description', json=data)
        return json.loads(r.text)
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }
