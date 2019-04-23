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

from zipfile import ZipFile
import base64
import io
from flask import Flask, jsonify, request
from datetime import datetime
import server.database as db
server.img_proc_core import as img_proc


def upload_image(upload_img_dict: dict) -> str:
    # TODO: VERIFY upload_img_dict
    # TODO: VERIFY upload_img_dict['data'] (correct type, etc)
    # TODO: extract size from upload_img_dict['data']

    #   'filename'	String with the name of the file
    #   'format'	String with the format of the file: PNG, JPEG or TIFF
    #   'user_hash'	A String with the user hash
    #   'data'	    The WHOLE file converted to a 64base string.

    result = db.add_image(
        filename=upload_img_dict['filename'],
        img_format=upload_img_dict['format'],
        description=upload_img_dict['description'],
        size=upload_img_dict['size'],
        timestamp=datetime.now(),
        data=upload_img_dict['data'],
        user_hash=upload_img_dict['user_hash'],
    )

    if result == True:
        return {
            'sucess':	True,
            'error_msg': '',
        }
    else:
        return {
            'sucess': False,
            'error_msg': 'Error adding image to database',
        }


def upload_multiple_images(upload_mult_img_dict: dict) -> str:
    # TODO: VERIFY upload_mult_img_dict
    # TODO: VERIFY upload_mult_img_dict['data'] (zip file with images)
    # TODO: extract imagesfrom upload_img_dict['data']
    # 'filename'	String with the name of the zip file
    # 'user_hash'	A String with the user hash
    # 'data'	The WHOLE zip file converted to a 64base string.
    zip_bytes = upload_mult_img_dict['data']

    result = []
    names = []
    for name, data in files_from_zip(zip_bytes):
        img_name = name
        img_data = data
        img_desc = "extracted from" + upload_mult_img_dict['filename']
        img_uhash = upload_mult_img_dict['user_hash']
        img_size = get_image_size()  # TODO
        img_format = get_image_format()  # TODO

        names.append(name)

        result.append = db.add_image(
            filename=img_name,
            img_format=img_format,
            description=img_desc,
            size=img_size,
            timestamp=datetime.now(),
            data=img_data,
            user_hash=img_uhash,
        )

    if any(result) == False:
        return {
            'sucess': False,
            'error_msg': 'Error adding: ' +
            ','.join([n for n, r in zip(name, result) if r]) +
            ' to database',
        }
    else:
        return {
            'sucess':	True,
            'error_msg': '',
        }


def get_image_info(user_hash: str):
    images = db.get_all_user_images(user_hash)
    out_dict = {}
    for img in images:
        out_dict[img.image_id] = {
            'filename': img.filename,
            'img_format': img.img_format,
            'timestamp': img.timestamp,
            'size': img.size,
            'description': img.description,
        }
    return out_dict


def download(download_images_dict: dict):
    #   'image_ids' List of Image IDs of the images to download
    #   'format'    Image format to download
    #   'user_hash' A String with the user hash
    img_ids = download_images_dict['image_ids']
    img_format = download_images_dict['format']
    user_hash = download_images_dict['user_hash']

    if len(img_ids) == 1:
        return download_signle_image(image_id=img_ids[0], image_format=img_format, user_hash=user_hash)
    else:
        pass


def download_signle_image(image_id: str, image_format: str, user_hash: str) -> dict:
    out_dict = {}
    if db.image_exists(image_id, user_hash) == False:
        out_dict['success'] = False
        out_dict['error_msg'] = 'No image id: '+image_id+' found for the user'
        out_dict['data'] = ''
    else:
        image = db.get_image(image_id, user_hash)
        if image is not None:
            out_dict['success'] = True
            out_dict['error_msg'] = ''
            img_bytes = b64str_to_fileio(image.data)
            converted_image = img_proc.format_convert(img_bytes, image_format)
            img_data = fileio_to_b64str(converted_image)
            out_dict['data'] = img_data
        else:
            out_dict['success'] = False
            out_dict['error_msg'] = 'Error fetching image'
            out_dict['data'] = ''
    return out_dict


def create_base64zip_file(names: list, datas: list) -> str:
    out_file = io.BytesIO()
    with ZipFile(out_file, 'w') as f:
        for name, data in zip(names, datas):
            f.writestr(name, data)
    out_file.seek(0)
    return out_file.read()


def fileio_to_b64str(fileio):
    b64_bytes = base64.b64encode(fileio)
    return str(b64_bytes, encoding='utf-8')


def b64str_to_fileio(file_b64: str):
    image_bytes = base64.b64decode(file_b64)
    return io.BytesIO(image_bytes)


def filenames_in_zip(zip_b64: str):
    zip_bytes = base64.b64decode(zip_b64)
    with ZipFile(zip_bytes, 'r') as f:
        names = f.namelist()
    return names


def files_from_zip(zip_b64: str):

    names = filenames_in_zip(zip_b64)

    zip_bytes = base64.b64decode(zip_b64)
    with ZipFile(zip_bytes, 'r') as f:
        for name in names:
            file = zip_bytes.open(name, 'rb')
            return name, file.read()
