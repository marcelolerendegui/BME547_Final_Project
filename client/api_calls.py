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
import requests
import base64
from PIL import Image
from io import BytesIO
api_host = "http://127.0.0.1:5000"


def Get_images_info(user_hash: str):
    r = requests.get(api_host + '/api/image_info/' + user_hash)
    return r
    pass


def upload_image(image_id, filename):
    image_dic = {
        "image_id": image_id,
        "out_image_filename": filename
    }
    r = requests.post(api_host + 'api/upload/image',
                      json=image_dic)
    return r
    pass


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
    pass


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
