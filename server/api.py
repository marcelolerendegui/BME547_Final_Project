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
from core.files import *
from core.verification import is_type_ok
import core.img_proc_core as img_proc
import server.database as db


import logging
logger = logging.getLogger(__name__)


def upload_image(upload_img_dict: dict) -> dict:
    """ upload single image

    this function receives an image file in base64 string
    and adds it to the database.

    :param upload_img_dict: dictionary with all the info
    :type upload_img_dict: dict
    :return: dictionary with success(bool), error_msg(str)
    :rtype: dict
    """
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
            'success':	False,
            'error_msg': t_err,
        }

    # Create image file IO
    image_fio = b64s_to_fio(upload_img_dict['data'])

    # Verify that the received data is actually an image
    if img_proc.is_image(image_fio) is False:
        return {
            'success':	False,
            'error_msg':
            'image_data cant be identified as an base64 formatted image file',
        }
        
    # Extract size and format from image data
    im_size = img_proc.get_image_size(image_fio)
    im_format = img_proc.get_image_format(image_fio)
    im_filename = name_from_path(upload_img_dict['filename'])

    # Store the new image in the database
    result = db.add_image(
        filename=im_filename,
        img_format=im_format,
        description=upload_img_dict['description'],
        size=im_size,
        timestamp=datetime.now(),
        data=upload_img_dict['data'],
        user_hash=upload_img_dict['user_hash'],
    )

    if result is False:
        return {
            'success': False,
            'error_msg': 'Error adding image to database',
        }

    # If everything went well
    return {
        'success':	True,
        'error_msg': '',
    }



def upload_multiple_images(upload_mult_img_dict: dict) -> dict:
    """ upload multiple images as a zip file

    this function receives a zip file in base64 string and
    extracts all the images from it and adds them to the
    database.

    :param upload_mult_img_dict: dictionary with all the info
    :type upload_mult_img_dict: dict
    :return: dictionary with success(bool), error_msg(str)
    :rtype: dict
    """
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
            'success':	False,
            'error_msg': t_err,
        }

    user_hash = upload_mult_img_dict['user_hash']

    zip_fio = b64s_to_fio(upload_mult_img_dict['data'])

    # Verify that the received data is actually a zip file
    if is_zip(zip_fio) is False:
        return {
            'success':	False,
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
        im_filename = name_from_path(name)
        # Store the new image in the database
        result = db.add_image(
            filename=im_filename,
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
        'success':	all(results),
        'error_msg': '\n'.join(errs),
    }


def get_image_info(user_hash: str) -> dict:
    """ get information of all the user images

    Get the following information:
    ['filename', 'img_format', 'timestamp', 'size', 'description']
    from all the images that belong the the user.

    TODO: Add this function to the client and protocol

    :param user_hash: hash that identifies a user
    :type user_hash: str
    :return: dictionary with success(bool), error_msg(str)
        or the images information
    :rtype: dict
    """
    # Verify input types
    t_ok, t_err = is_type_ok(
        user_hash,
        "str"
    )
    if t_ok is False:
        return {
            'success':	False,
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


def edit_image_description(edit_image_description_dict: dict) -> dict:
    """ edit the description of an image

    This function validates the input dict, fetches the image
    and changes its description.
    And returns a dicionary with success and error message
    TODO: Add this function to the client and protocol

    :param edit_image_description_dict: dictionary with all the
        required info (see protocol)
    :type edit_image_description_dict: dict
    :return: dictionary with
        success(bool), error_msg(str)
    :rtype: dict
    """
    # Verify input types
    t_ok, t_err = is_type_ok(
        edit_image_description_dict,
        """
        dict{
            'image_id': str,
            'description': str,
            'user_hash': str
        }
        """
    )

    if t_ok is False:
        return {
            'success':	False,
            'error_msg': t_err,
        }

    image_id = edit_image_description_dict['image_id']
    user_hash = edit_image_description_dict['user_hash']

    # Check if image id exists (and fetch it)
    result, errmsg, image = check_existance_and_fetch_image(
        image_id,
        user_hash
    )

    if result is False:
        return {
            'success': False,
            'error_msg': errmsg,
        }

    # Edit Description
    image.description = edit_image_description_dict['description']
    # Save image
    try:
        image.save()
    except:
        return {
            'success': False,
            'error_msg': 'Could not save edited image',
        }
    return {
        'success': True,
        'error_msg': '',
    }


def edit_image_filename(edit_image_filename_dict: dict) -> dict:
    """ edit the filename of an image

    This function validates the input dict, fetches the image
    and changes its filename.
    And returns a dicionary with success and error message
    TODO: Add this function to the client and protocol

    :param edit_image_filename_dict: dictionary with all the
        required info (see protocol)
    :type edit_image_filename_dict: dict
    :return: dictionary with
        success(bool), error_msg(str)
    :rtype: dict
    """
    # Verify input types
    t_ok, t_err = is_type_ok(
        edit_image_filename_dict,
        """
        dict{
            'image_id': str,
            'filename': str,
            'user_hash': str
        }
        """
    )

    if t_ok is False:
        return {
            'success':	False,
            'error_msg': t_err,
        }

    image_id = edit_image_filename_dict['image_id']
    user_hash = edit_image_filename_dict['user_hash']

    # Check if image id exists (and fetch it)
    result, errmsg, image = check_existance_and_fetch_image(
        image_id,
        user_hash
    )

    if result is False:
        return {
            'success': False,
            'error_msg': errmsg,
        }

    # Edit Description
    image.filename = edit_image_filename_dict['filename']
    # Save image
    try:
        image.save()
    except:
        return {
            'success': False,
            'error_msg': 'Could not save edited image',
        }
    return {
        'success': True,
        'error_msg': '',
    }


def download(download_images_dict: dict) -> dict:
    """ download single or multiple images

    To download a single or multiple images from the server,
    the user calls this api function through the RESTapi.
    This function validates the input dict and calls:
    download_signle_image or download_multiple_images
    And returns a dicionary with success and error message
    :param download_images_dict: dictionary with all the
        required info (see protocol)
    :type download_images_dict: dict
    :return: dictionary with
        success(bool), error_msg(str)
    :rtype: dict
    """
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
            'success':	False,
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
    """ download single image

    To download multiple image from the server, the user calls
    this api function through the RESTapi.
    This function validates input data, fetches the image,
    converts it, converts it into base64 string and returns it,


    :param image_ids: id of image to fetch
    :type image_ids: str
    :param image_format: download format for the image
    :type image_format: str
    :param user_hash: hash identifying the user
    :type user_hash: str
    :return: dictionary with
        success(bool), error_msg(str) and data(base64 str)
    :rtype: dict
    """
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
    image_ids: list,
    image_format: str,
    user_hash: str
) -> dict:
    """ download multiple images as a zip file

    To download multiple images from the server, the user calls
    this api function through the RESTapi.
    This function validates input data, fetches all images,
    converts all images, creates a zipfile and puts all images
    into it, converts it into base64 string and returns it,


    :param image_ids: list of all the image ids to fetch
    :type image_ids: list
    :param image_format: download format for the images
    :type image_format: str
    :param user_hash: hash identifying the user
    :type user_hash: str
    :return: dictionary with
        success(bool), error_msg(str) and data(base64 str)
    :rtype: dict
    """

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
        out_name = get_unique_filename(
            names,
            image.filename,
            image_format.lower()
        )
        names.append(out_name)

    # Create zip file using the saved names and data
    zip_fio = create_zip_fio(names, datas)

    # Retur the zipfile in b64s and errors
    return {
        'success': all(success),
        'error_msg': '\n'.join(error_msg),
        'data': fio_to_b64s(zip_fio),
    }


def get_unique_filename(names: list, name: str, ext: str) -> str:
    """ returns a filename not present in input names list

    When generating a new file, sometimes there are existing
    files with the same name, in that case, we want to create
    an unique filename: e.g. "name1.ext".
    This function does that!

    :param names: list of already taken names. WITH EXTENSIONS!
    :type names: list
    :param name: original name
    :type name: str
    :param ext: extension of the name. WHITHOUT THE DOT!
    :type ext: str
    :return: unique filename not present in names
    :rtype: str
    """

    out_name = '.'.join([name, ext])

    if out_name not in names:
        return out_name
    i = 1
    out_name = '.'.join([name + str(i), ext])
    while out_name in names:
        i += 1
        out_name = '.'.join([name + str(i), ext])
    return out_name


def image_process(image_process_dict: dict) -> dict:
    """ Apply processing algorithm to an image

    This function validates input data, fetches an image,
    applies a processing algorithm to it, converts it to
    a new format and stores it in the database as a new
    image with a new image filename,


    :param image_process_dict: dictionary with all the 
        required information
    :type image_process_dict: dict
    :return: dictionary with
        success(bool), error_msg(str)
    :rtype: dict
    """
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
            'success':	False,
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
            'success': False,
            'error_msg': errmsg,
            'processing_time': 0.0
        }

    # Start measuring ellapsed time
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

    # Stop measuring ellapsed time
    end_time = datetime.now()
    ellapsed_time = end_time-start_time

    return {
        'success': True,
        'error_msg': '',
        'processing_time': ellapsed_time.total_seconds()
    }


def get_log() -> dict:
    """ TODO: implement this function!!

    :return: [description]
    :rtype: [type]
    """
    pass


def check_existance_and_fetch_image(image_id: str, user_hash: str) -> tuple:
    """checks if the image_id is in the database for the user and returns it.


    :param image_id: image_id to find
    :type image_id: str
    :param user_hash: hash that identifies a user
    :type user_hash: str
    :return: Success, error message, Image
    :rtype: tuple
    """
    if db.image_exists(image_id, user_hash) is False:
        return False, 'No image id: ' + image_id + ' found for the user', None
    else:
        image = db.get_image(image_id, user_hash)
        if image is not None:
            return True, '', image
        else:
            return False, 'Error fetching image' + image_id, None
