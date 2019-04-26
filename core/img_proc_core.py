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
import io as IO
from skimage import data
from skimage import img_as_float
from skimage import util
from skimage import exposure
from skimage import io
from PIL import Image


def is_image(img_fio) -> bool:
    img_fio.seek(0)
    try:
        Image.open(img_fio)
        return True
    except:
        return False


def get_image_size(img_fio) -> str:
    img_fio.seek(0)
    img = Image.open(img_fio)
    width, height = img.size
    img_fio.seek(0)
    return str(width) + 'x' + str(height)


def get_image_format(img_fio) -> str:
    img_fio.seek(0)
    img = Image.open(img_fio)
    img_fio.seek(0)
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
    img_fio.seek(0)
    if algorithm == 'Histogram Equalization':
        return histogram_equalization(img_fio)
    elif algorithm == 'Contrast Stretching':
        return contrast_stretch(img_fio, 2, 98)
    elif algorithm == 'Log Compression':
        return log_compression(img_fio)
    elif algorithm == 'Contrast Invert':
        return contrast_invert(img_fio)
    elif algorithm == 'No Algorithm':
        return img_fio
    else:
        return img_fio


def histogram_equalization(img_fio):
    img_fio.seek(0)
    img = io.imread(img_fio)

    for channel in range(img.shape[2]):
        img[:, :, channel] = exposure.equalize_hist(img[:, :, channel])

    outimg = Image.fromarray(img)

    out_fio = IO.BytesIO()

    outimg.save(out_fio, get_image_format(img_fio))
    img_fio.seek(0)
    out_fio.seek(0)

    return out_fio


def contrast_stretch(img_fio, lower_perc: int, higher_perc: int):
    img_fio.seek(0)
    image = io.imread(img_fio)
    pl, ph = np.percentile(image, (lower_perc, higher_perc))
    img_output = exposure.rescale_intensity(image, in_range=(pl, ph))

    outimg = Image.fromarray(img_output)

    out_fio = IO.BytesIO()

    outimg.save(out_fio, get_image_format(img_fio))
    img_fio.seek(0)
    out_fio.seek(0)

    return out_fio


def log_compression(img_fio):
    img_fio.seek(0)
    image = io.imread(img_fio)

    img_output = exposure.adjust_log(image, 1)

    outimg = Image.fromarray(img_output)

    out_fio = IO.BytesIO()

    outimg.save(out_fio, get_image_format(img_fio))
    img_fio.seek(0)
    out_fio.seek(0)

    return out_fio


def contrast_invert(img_fio):
    img_fio.seek(0)
    image = io.imread(img_fio)

    img_output = util.invert(image)

    outimg = Image.fromarray(img_output)

    out_fio = IO.BytesIO()

    outimg.save(out_fio, get_image_format(img_fio))
    img_fio.seek(0)
    out_fio.seek(0)

    return out_fio


def format_convert(img_fio, im_format: str):
    img_fio.seek(0)

    # Create new file IO
    out_fio = IO.BytesIO()

    # Open img_fio
    image = Image.open(img_fio)

    # Save with new format to fio
    image.save(out_fio, im_format)

    # Rewind and return
    img_fio.seek(0)
    out_fio.seek(0)
    return out_fio
