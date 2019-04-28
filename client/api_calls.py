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
api_host = "http://127.0.0.1:5000"


def apply_algorithm(
    image_id: str,
    algorithm: str,
    im_format: str,
    out_filename: str,
    user_hash: str
):
    d = {
        'image_id': image_id,
        'algorithm': algorithm,
        'out_image_format': im_format,
        'out_image_filename': out_filename,
        'user_hash': user_hash,
    }
    r = requests.post(api_host+"/api/image_process", json=d)
    return json.loads(r.text)


def get_download_images(image_ids: str, im_format: str, user_hash: str):
    d = {
        'image_ids': image_ids,
        'format': im_format,
        'user_hash': user_hash
    }
    r = requests.get(api_host+"/api/download/", json=d)
    return json.loads(r.text)


def get_single_image(image_id: str, user_hash: str):
    d = {
        'image_ids': [image_id],
        'format': 'PNG',
        'user_hash': user_hash
    }
    r = requests.get(api_host+"/api/download/", json=d)
    return json.loads(r.text)


def get_images_info(user_hash: str):
    r = requests.get(api_host + '/api/image_info/' + user_hash)
    return json.loads(r.text)


def upload_image(image_b64s, filename, user_hash):
    d = {
        'filename': filename,
        'user_hash': user_hash,
        'description': filename,
        'data': image_b64s,
    }
    r = requests.post(api_host+"/api/upload/image", json=d)
    return json.loads(r.text)


def upload_zip(zip_b64s, filename, user_hash):
    d = {
        'filename': filename,
        'user_hash': user_hash,
        'data': zip_b64s,
    }
    r = requests.post(api_host+"/api/upload/zip", json=d)
    return json.loads(r.text)


def upload_multiple_images(filename, user_hash):
    image_dic = {
        "filename": filename,
        "user_hash": user_hash,
        "data": "The WHOLE zip file converted to a 64base string"
    }
    r = requests.post(api_host + '/api/upload/zip', json=image_dic)
    return r


def equalize_histogram(image_id, image_format, filename):
    data = {
        'image_id': image_id,
        'algorithm': 'Histogram Equalization',
        'out_image_format': image_format,
        'out_image_filename': filename
    }
    r = requests.post(api_host + '/api/img_proc', json=data)
    return r


def contrast_stretch(image_id, image_format, filename):
    data = {
        'image_id': image_id,
        'algorithm': 'Contrast Stretching',
        'out_image_format': image_format,
        'out_image_filename': filename
    }
    r = requests.post(api_host + '/api/img_proc', json=data)
    return r
    pass


def log_compress(image_id, image_format, filename):
    data = {
        'image_id': image_id,
        'algorithm': 'Log Compression',
        'out_image_format': image_format,
        'out_image_filename': filename
    }
    r = requests.post(api_host + '/api/img_proc', json=data)
    return r
    pass


def convert(image_id, image_format, filename):
    data = {
        'image_id': image_id,
        'algorithm': 'No Algorithm',
        'out_image_format': image_format,
        'out_image_filename': filename
    }
    r = requests.post(api_host + '/api/img_proc', json=data)
    return r
    pass


def contrast_invert(image_id, image_format, filename):
    data = {
        'image_id': image_id,
        'algorithm': 'contrast_invert',
        'out_image_format': image_format,
        'out_image_filename': filename
    }
    r = requests.post(api_host + '/api/img_proc', json=data)
    return r
    pass


def download_images(image_id, filename, image_format):
    r = requests.get(api_host + 'port/api/download/' + image_id)
    img = r.json()
    im = Image.open(BytesIO(base64.b64decode(img)))
    im.save(str(filename), str(image_format))
    return im
    pass


def edit_filename(image_id: str, new_fname: str, user_hash: str):
    data = {
        'image_id': image_id,
        'filename': new_fname,
        'user_hash': user_hash
    }
    r = requests.post(api_host + '/api/edit/filename', json=data)
    return json.loads(r.text)


def edit_description(image_id: str, new_desc: str, user_hash: str):
    data = {
        'image_id': image_id,
        'description': new_desc,
        'user_hash': user_hash
    }
    r = requests.post(api_host + '/api/edit/description', json=data)
    return json.loads(r.text)
