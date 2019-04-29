# Copyright 2019:
#       Marcelo Lerendegui <marcelo@lerendegui.com>
#       WeiHsien Lee <weihsien.lee@duke.edu>
#       Yihang Xin <yihang.xin@duke.edu>
#
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
import io as IO
import os
fileIO = IO.IOBase


def s_to_b(s: str) -> bytes:
    """convert string to bytes

    :param s: input string
    :type s: str
    :return: output bytes
    :rtype: bytes
    """
    b = s.encode('utf8')
    return b


def s_to_b64s(s: str) -> str:
    """convert string to base 64 string

    :param s: input string
    :type s: str
    :return: output base 64 string
    :rtype: str
    """
    b64s = base64.b64encode(s.encode('utf8')).decode('utf8')
    return b64s


def s_to_fio(s: str) -> fileIO:
    """convert string to fileIO

    :param s: input string
    :type s: str
    :return: output fileIO
    :rtype: fileIO
    """
    fio = IO.BytesIO(s.encode('utf8'))
    fio.seek(0)
    return fio


def b_to_s(b: bytes) -> str:
    """convert bytes to string

    :param b: input bytes
    :type b: bytes
    :return: output string
    :rtype: str
    """
    s = b.decode('utf8')
    return s


def b_to_b64s(b: bytes) -> str:
    """convert bytes to base 64 string

    :param b: input bytes
    :type b: bytes
    :return: output base 64 string
    :rtype: str
    """
    b64s = base64.b64encode(b).decode('utf8')
    return b64s


def b_to_fio(b: bytes) -> fileIO:
    """convert bytes to fileIO

    :param b: input bytes
    :type b: bytes
    :return: output fileIO
    :rtype: fileIO
    """
    fio = IO.BytesIO(b)
    fio.seek(0)
    return fio


def b64s_to_b(b64s: str) -> bytes:
    """convert base 64 strting to bytes

    :param b64s: input base 64 string
    :type b64s: str
    :return: output bytes
    :rtype: bytes
    """
    b = base64.b64decode(b64s.encode('utf8'))
    return b


def b64s_to_s(b64s: str) -> str:
    """convert base 64 strting to string

    :param b64s: input base 64 string
    :type b64s: str
    :return: output string
    :rtype: str
    """
    s = base64.b64decode(b64s.encode('utf8')).decode('utf8')
    return s


def b64s_to_fio(b64s: str) -> fileIO:
    """convert base 64 strting to fileIO

    :param b64s: input base 64 string
    :type b64s: str
    :return: output fileIO
    :rtype: fileIO
    """
    fio = IO.BytesIO(base64.b64decode(b64s.encode('utf8')))
    fio.seek(0)
    return fio


def fio_to_b(fio: fileIO) -> bytes:
    """convert fileIO to bytes

    :param fio: input fileIO
    :type fio: fileIO
    :return: output bytes
    :rtype: bytes
    """
    fio.seek(0)
    b = fio.read()
    fio.seek(0)
    return b


def fio_to_s(fio: fileIO) -> str:
    """convert fileIO to string

    :param fio: input fileIO
    :type fio: fileIO
    :return: output string
    :rtype: str
    """
    fio.seek(0)
    s = fio.read().decode('utf8')
    fio.seek(0)
    return s


def fio_to_b64s(fio: fileIO) -> str:
    """convert fileIO to base 64 string

    :param fio: input fileIO
    :type fio: fileIO
    :return: output base 64 string
    :rtype: str
    """
    fio.seek(0)
    b64s = base64.b64encode(fio.read()).decode('utf8')
    fio.seek(0)
    return b64s


def create_zip_fio(names_s: list, datas_b64s: list) -> fileIO:
    """create a zip fileIO from filenames and datas

    this function creates a fileIO with a zip file containing
    all the input files specified by their filenames and their
    contents as base 64 strings.

    :param names_s: list of filenames to put in the zip
    :type names_s: list
    :param datas_b64s: list of file contents in base 64 string
    :type datas_b64s: list
    :return: output fileIO with a zip file inside
    :rtype: fileIO
    """
    # Create empty bytesIO
    out_fio = IO.BytesIO()
    # Open it as a zip
    with ZipFile(out_fio, 'w') as f:
        # Write each data to a file called name
        for name, data in zip(names_s, datas_b64s):
            f.writestr(name, b64s_to_b(data))
    # Don't forget to rewind
    out_fio.seek(0)
    return out_fio


def files_from_zip(zip_fio: fileIO):
    """ generator that yields files from zip

    This function returns a generator that yields:
        filename, fileIO

    for each file inside the input zip in fileIO

    :param zip_fio: zip fileIO
    :type zip_fio: fileIO
    """
    # Open zip file to read
    with ZipFile(zip_fio, 'r') as f:
        # Extract list of fullpath filenames
        names = f.namelist()
        for name in names:
            # Extract name and extension
            nameext = nameext_from_path(name)
            # If it's not a directory yield nameext and data
            if nameext != '':
                file = f.open(name, 'r')
                yield nameext, b_to_fio(file.read())


def is_zip(zip_fio: fileIO) -> bool:
    """check if fileIO is a zip

    :param zip_fio: fileIO to check
    :type zip_fio: fileIO
    :return: True if input fileIO is a zip, False othersise
    :rtype: bool
    """
    try:
        ZipFile(zip_fio, 'r')
        return True
    except:
        return False


def nameext_from_path(path: str) -> str:
    """extract name and extension from path

    :param path: full path to analyze
    :type path: str
    :return: name and extension: 'name.ext'
    :rtype: str
    """
    nameext = os.path.split(path)[-1]
    return nameext


def ext_from_path(path: str) -> str:
    """extract extension from path

    :param path: full path to analyze
    :type path: str
    :return: extension: '.ext'
    :rtype: str
    """
    ext = os.path.splitext(path)[-1]
    return ext


def name_from_path(path: str) -> str:
    """extract file name from path

    :param path: full path to analyze
    :type path: str
    :return: file name: 'name'
    :rtype: str
    """
    nameext = nameext_from_path(path)
    name = os.path.splitext(nameext)[0]
    return name
