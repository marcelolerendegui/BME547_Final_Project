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
):
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


def get_download_images(image_ids: str, im_format: str, user_hash: str):

    # Validate image_ids type
    t_ok, t_err = is_type_ok(image_ids, "str")
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


def get_single_image(image_id: str, user_hash: str):

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


def get_images_info(user_hash: str):

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


def upload_image(image_b64s: str, filename: str, user_hash: str):

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


def upload_zip(zip_b64s: str, filename: str, user_hash: str):

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


def upload_multiple_images(filename, user_hash):

    # Validate filename type
    t_ok, t_err = is_type_ok(filename, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    # Validate user_hash type
    t_ok, t_err = is_type_ok(user_hash, "str")
    if t_ok is False:
        return {'success':	False, 'error_msg': t_err}

    image_dic = {
        "filename": filename,
        "user_hash": user_hash,
        "data": "The WHOLE zip file converted to a 64base string"
    }
    try:
        r = requests.post(api_host + '/api/upload/zip', json=image_dic)
        return r
    except:
        return {
            'success': False,
            'error_msg': 'Could not connect to server',
        }


def edit_filename(image_id: str, new_fname: str, user_hash: str):

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


def edit_description(image_id: str, new_desc: str, user_hash: str):

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
