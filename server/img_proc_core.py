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
import cv2
from skimage import data
from skimage import img_as_float
from skimage import util
from skimage import exposure
from PIL import Image
import io


def get_image_size():
    pass


def transform_image():
    pass


def histogram_equalization(image):
    img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
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


def format_convert(image, im_format: str):
    mem_file = io.BytesIO()
    image.save(mem_file, im_format)
    mem_file.seek(0)
    return mem_file.read()
