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

from flask import Flask, jsonify, request
from datetime import datetime
from server.files import *
import server.database as db
import server.img_proc_core as img_proc

import logging
logger = logging.getLogger(__name__)


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

    if result is True:
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

    if any(result) is False:
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
    # TODO: VERIFY download_images_dict

    #   'image_ids' List of Image IDs of the images to download
    #   'format'    Image format to download
    #   'user_hash' A String with the user hash
    img_ids = download_images_dict['image_ids']
    img_format = download_images_dict['format']
    user_hash = download_images_dict['user_hash']

    if len(img_ids) == 1:
        return download_signle_image(
            image_id=img_ids[0],
            image_format=img_format,
            user_hash=user_hash
        )
    else:
        return download_multiple_images(
            image_ids=img_ids,
            image_format=img_format,
            user_hash=user_hash
        )


def download_multiple_images(
    image_ids: str,
    image_format: str,
    user_hash: str
) -> dict:
    names = []
    datas = []
    success = []
    error_msg = []
    out_dict = {}

    for img_id in image_ids:
        if db.image_exists(img_id, user_hash) is False:
            success.append(False)
            error_msg.append(
                'No image id: ' +
                img_id +
                ' found for the user'
            )
        else:
            image = db.get_image(img_id, user_hash)
            if image is not None:
                success.append(True)
                img_bytes = b64s_to_fileio(image.data)
                converted_image = img_proc.format_convert(
                    img_bytes, image_format)
                img_data = fileio_to_b64s(converted_image)
                datas.append(img_data)
                names.append(image.filename)
            else:
                success.append(False)
                error_msg.append('Error fetching image')

    zip_fio = create_zip_fio(names, datas)
    out_dict = {
        'success': any(success is False),
        'error_msg': '\n'.join(error_msg),
        'data': fio_to_b64(zip_fio),
    }


def download_signle_image(
    image_id: str,
    image_format: str,
    user_hash: str
) -> dict:
    out_dict = {}
    if db.image_exists(image_id, user_hash) is False:
        out_dict['success'] = False
        out_dict['error_msg'] = 'No image id: '+image_id+' found for the user'
        out_dict['data'] = ''
    else:
        image = db.get_image(image_id, user_hash)
        if image is not None:
            out_dict['success'] = True
            out_dict['error_msg'] = ''
            img_bytes = b64s_to_fileio(image.data)
            converted_image = img_proc.format_convert(img_bytes, image_format)
            img_data = fileio_to_b64s(converted_image)
            out_dict['data'] = img_data
        else:
            out_dict['success'] = False
            out_dict['error_msg'] = 'Error fetching image'
            out_dict['data'] = ''
    return out_dict


def image_process(image_process_dict: dict) -> dict:
    # TODO: VERIFY image_process_dict
    # TODO: VERIFY algorithm

    # 'image_id'	Image IDs of the images to process
    # 'algorithm'	Algorithm to apply to the image
    # 'out_image_format'	Format of the output processed image
    # 'out_image_filename'	Filename of the output processed image

    image_id = image_process_dict['image_process_dict']
    algorithm = image_process_dict['algorithm']
    out_image_format = image_process_dict['out_image_format']
    out_image_filename = image_process_dict['out_image_filename']
    user_hash = image_process_dict['user_hash']

    success, errmsg, in_image = check_existance_and_fetch_image(
        image_id,
        user_hash
    )

    if success is False:
        return {
            'success': success,
            'error_msg': errmsg,
            'processing_time': 0.0
        }

    start_time = datetime.now()
    in_image_data = b64s_to_fileio(in_image.data)
    out_image = img_proc.transform_image(in_image_data, algorithm)
    out_image = img_proc.format_convert(out_image, out_image_format)

    db.add_image(
        filename=out_image_filename,
        img_format=out_image_format,
        description='created from ' + in_image.filename,
        size=get_image_size(out_image),
        timestamp=datetime.now(),
        data=fileio_to_b64s(out_image),
        user_hash=user_hash
    )
    end_time = datetime.now()
    ellapsed_time = end_time-start_time

    return {
        'success': success,
        'error_msg': errmsg,
        'processing_time': ellapsed_time.total_seconds
    }


def check_existance_and_fetch_image(image_id: str, user_hash: str):
    out_dict = {}
    if db.image_exists(image_id, user_hash) is False:
        return False,
        'No image id: ' + image_id + ' found for the user',
        None
    else:
        image = db.get_image(image_id, user_hash)
        if image is not None:
            return True,
            '',
            image
        else:
            return False,
            'Error fetching image' + image_id,
            None


def b64_convert_image_b64(b64s_image: str, out_format: str):
    img_bytes = b64s_to_fileio(b64s_image)
    converted_image = img_proc.format_convert(img_bytes, out_format)
    return fileio_to_b64s(converted_image)
