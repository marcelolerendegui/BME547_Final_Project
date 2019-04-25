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
from server.verification import is_type_ok
import server.database as db
import server.img_proc_core as img_proc

import logging
logger = logging.getLogger(__name__)


def upload_image(upload_img_dict: dict) -> dict:

    # Verify input types
    t_ok, t_err = is_type_ok(
        upload_img_dict,
        """
        dict{
            'filename': str,
            'description': str,
            'data': str,
            'user_hash': str
        }
        """
    )

    if t_ok is False:
        return {
            'sucess':	False,
            'error_msg': t_err,
        }

    # Create image file IO
    image_fio = b64s_to_fio(upload_img_dict['data'])

    # Verify that the received data is actually an image
    if img_proc.is_image(image_fio) is False:
        return {
            'sucess':	False,
            'error_msg':
            'image_data cant be identified as an image file in base64 string format',
        }
    # Extract size and format from image data
    im_size = img_proc.get_image_size(image_fio)
    im_format = img_proc.get_image_format(image_fio)

    # Store the new image in the database
    result = db.add_image(
        filename=upload_img_dict['filename'],
        img_format=im_format,
        description=upload_img_dict['description'],
        size=im_size,
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


def upload_multiple_images(upload_mult_img_dict: dict) -> dict:

    # Verify input types
    t_ok, t_err = is_type_ok(
        upload_mult_img_dict,
        """
        dict{
            'filename': str,
            'user_hash': str,
            'data': str,
        }
        """
    )

    if t_ok is False:
        return {
            'sucess':	False,
            'error_msg': t_err,
        }

    user_hash = upload_mult_img_dict['user_hash']

    zip_fio = b64s_to_fio(upload_mult_img_dict['data'])

    # Verify that the received data is actually a zip file
    if is_zip(zip_fio) is False:
        return {
            'sucess':	False,
            'error_msg':
            'data cant be identified as a zip file in base64 string format',
        }

    # Process each file inside the zip
    results = []
    errs = []
    for name, image_fio in files_from_zip(zip_fio):
        # Verify that the current file is actually an image
        if img_proc.is_image(image_fio) is False:
            results.append(False)
            errs.append(
                name +
                'file can not be identified as an image. Ignored \n'
            )
            continue
        # Extract size and format from image data
        im_size = img_proc.get_image_size(image_fio)
        im_format = img_proc.get_image_format(image_fio)
        # Store the new image in the database
        result = db.add_image(
            filename=name,
            img_format=im_format,
            description="extracted from " + upload_mult_img_dict['filename'],
            size=im_size,
            timestamp=datetime.now(),
            data=fio_to_b64s(image_fio),
            user_hash=user_hash,
        )
        if result is False:
            results.append(False)
            errs.append(
                'Error adding image' +
                name +
                ' to database\n'
            )

    # return all the error messages
    return {
        'sucess':	all(results),
        'error_msg': '\n'.join(errs),
    }


def get_image_info(user_hash: str):
    # Verify input types
    t_ok, t_err = is_type_ok(
        user_hash,
        "str"
    )
    if t_ok is False:
        return {
            'sucess':	False,
            'error_msg': t_err,
        }

    images = db.get_all_user_images(user_hash)
    out_dict = {}
    if images is not None:
        for img in images:
            out_dict[str(img._id)] = {
                'filename': img.filename,
                'img_format': img.img_format,
                'timestamp': img.timestamp,
                'size': img.size,
                'description': img.description,
            }
    return out_dict


def edit_image_description(edit_image_description_dict: dict):
    # Verify input types
    # Check if image id exists (and fetch it)
    # Edit Description
    # Save image
    return 'EDIT IMAGE DESCRIPTION'


def edit_image_filename(edit_image_filename_dict: dict):
    # Verify input types
    # Check if image id exists (and fetch it)
    # Edit filename
    # Save image
    return 'EDIT IMAGE FILENAME'


def download(download_images_dict: dict):
    # Verify input types
    t_ok, t_err = is_type_ok(
        download_images_dict,
        """
        dict{
            'image_ids': list[str...],
            'format': str,
            'user_hash': str
        }
        """
    )
    if t_ok is False:
        return {
            'sucess':	False,
            'error_msg': t_err,
        }

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


def download_signle_image(
    image_id: str,
    image_format: str,
    user_hash: str
) -> dict:

    # Check if image id exists (and fetch it)
    result, errmsg, image = check_existance_and_fetch_image(
        image_id,
        user_hash
    )

    if result is False:
        return {
            'success': False,
            'error_msg': errmsg,
            'data': '',
        }

    image_fio = b64s_to_fio(image.data)
    converted_image_fio = img_proc.format_convert(image_fio, image_format)

    return {
        'success': True,
        'error_msg': '',
        'data': fio_to_b64s(converted_image_fio),
    }


def download_multiple_images(
    image_ids: str,
    image_format: str,
    user_hash: str
) -> dict:

    names = []
    datas = []
    success = []
    error_msg = []

    for img_id in image_ids:

        # Check if image id exists (and fetch it)
        result, errmsg, image = check_existance_and_fetch_image(
            img_id,
            user_hash
        )

        if result is False:
            success.append(False)
            error_msg.append(errmsg)
            continue

        # Convert image
        image_fio = b64s_to_fio(image.data)
        converted_image_fio = img_proc.format_convert(
            image_fio,
            image_format
        )
        image_b64s = fio_to_b64s(converted_image_fio)

        # Save data to generate zip file
        success.append(True)
        datas.append(image_b64s)
        names.append(image.filename)

    # Create zip file using the saved names and data
    zip_fio = create_zip_fio(names, datas)
    # Retur the zipfile in b64s and errors
    return {
        'success': all(success),
        'error_msg': '\n'.join(error_msg),
        'data': fio_to_b64s(zip_fio),
    }


def image_process(image_process_dict: dict) -> dict:
    # Verify input types
    t_ok, t_err = is_type_ok(
        image_process_dict,
        """
        dict{
            'image_id': str,
            'algorithm':str,
            'out_image_format': str,
            'out_image_filename':str,
            'user_hash': str,
        }
        """
    )
    if t_ok is False:
        return {
            'sucess':	False,
            'error_msg': t_err,
        }

    image_id = image_process_dict['image_id']
    algorithm = image_process_dict['algorithm']
    out_image_format = image_process_dict['out_image_format']
    out_image_filename = image_process_dict['out_image_filename']
    user_hash = image_process_dict['user_hash']

    # Check if algorithm is correct
    if img_proc.is_valid_algorithm(algorithm) is False:
        return {
            'success': False,
            'error_msg': 'Unknown algorithm: ' + algorithm,
            'processing_time': 0.0
        }

    # Check if image exists and fetch it
    result, errmsg, in_image = check_existance_and_fetch_image(
        image_id,
        user_hash
    )

    if result is False:
        return {
            'success': result,
            'error_msg': errmsg,
            'processing_time': 0.0
        }

    start_time = datetime.now()
    image_fio = b64s_to_fio(in_image.data)

    # Extract size from image data
    im_size = img_proc.get_image_size(image_fio)

    # Transform image using algorithm
    out_image_fio = img_proc.transform_image(image_fio, algorithm)

    # Convert image format
    out_image_fio = img_proc.format_convert(out_image_fio, out_image_format)

    result = db.add_image(
        filename=out_image_filename,
        img_format=out_image_format,
        description='created from ' + in_image.filename,
        size=im_size,
        timestamp=datetime.now(),
        data=fio_to_b64s(out_image_fio),
        user_hash=user_hash
    )

    if result is False:
        return {
            'success': False,
            'error_msg': 'Error adding image' +
            out_image_filename +
            ' to database\n',
            'processing_time': 0.0
        }

    end_time = datetime.now()
    ellapsed_time = end_time-start_time

    return {
        'success': True,
        'error_msg': '',
        'processing_time': ellapsed_time.total_seconds
    }


def get_log():
    return ''


def check_existance_and_fetch_image(image_id: str, user_hash: str):
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
