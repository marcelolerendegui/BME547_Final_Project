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

import numpy as np
from skimage import data
from skimage import img_as_float
from skimage import util
from skimage import exposure
from PIL import Image
import io


def is_image(img_fio) -> bool:
    try:
        Image.open(img_fio)
        return True
    except:
        return False


def get_image_size(img_fio) -> str:
    img = Image.open(img_fio)
    width, height = img.size
    return str(width) + 'x' + str(height)


def get_image_format(img_fio) -> str:
    img = Image.open(img_fio)
    return img.format


def is_valid_algorithm(algorithm: str) -> bool:
    available_algorithms = [
        'Histogram Equalization',
        'Contrast Stretching',
        'Log Compression',
        'Contrast Invert',
        'No Algorithm',
    ]
    return algorithm in available_algorithms


def transform_image(img_fio, algorithm: str):
    if algorithm == 'Histogram Equalization':
        return img_fio
    elif algorithm == 'Contrast Stretching':
        return img_fio
    elif algorithm == 'Log Compression':
        return img_fio
    elif algorithm == 'Contrast Invert':
        return img_fio
    elif algorithm == 'No Algorithm':
        return img_fio
    else:
        return img_fio


def histogram_equalization(img_fio):
    img_output = exposure.equalize_hist(img_fio)
    return img_output


def contrast_stretch(image, lower_perc: int, higher_perc: int):
    pl, ph = np.percentile(image, (lower_perc, higher_perc))
    img_output = exposure.rescale_intensity(image, in_range=(pl, ph))
    return img_output


def log_compression(image):
    img_output = exposure.adjust_log(image, 1)
    return img_output


def contrast_invert(image):
    img_output = util.invert(image)
    return img_output


def format_convert(img_fio, im_format: str):
    # Create new file IO
    fio = io.BytesIO()

    # Open img_fio
    image = Image.open(img_fio)

    # Save with new format to fio
    image.save(fio, im_format)

    # Rewind and return
    fio.seek(0)
    return fio
