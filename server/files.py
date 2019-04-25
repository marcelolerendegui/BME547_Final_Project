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
import os
fileIO = io.IOBase


def s_to_b(s: str) -> bytes:
    b = s.encode('utf8')
    return b


def s_to_b64s(s: str) -> str:
    b64s = base64.b64encode(s.encode('utf8')).decode('utf8')
    return b64s


def s_to_fio(s: str) -> fileIO:
    fio = io.BytesIO(s.encode('utf8'))
    return fio


def b_to_s(b: bytes) -> str:
    s = b.decode('utf8')
    return s


def b_to_b64s(b: bytes) -> str:
    b64s = base64.b64encode(b).decode('utf8')
    return b64s


def b_to_fio(b: bytes):
    fio = io.BytesIO(b)
    return fio


def b64s_to_b(b64s: str) -> bytes:
    b = base64.b64decode(b64s.encode('utf8'))
    return b


def b64s_to_s(b64s: str) -> str:
    s = base64.b64decode(b64s.encode('utf8')).decode('utf8')
    return s


def b64s_to_fio(b64s: str) -> fileIO:
    fio = io.BytesIO(base64.b64decode(b64s.encode('utf8')))
    return fio


def fio_to_b(fio: fileIO) -> bytes:
    fio.seek(0)
    b = fio.read()
    return b


def fio_to_s(fio: fileIO) -> str:
    fio.seek(0)
    s = fio.read().decode('utf8')
    return s


def fio_to_b64s(fio: fileIO) -> str:
    fio.seek(0)
    b64s = base64.b64encode(fio.read()).decode('utf8')
    return b64s


def create_zip_fio(names: list, datas: list) -> fileIO:
    # Create empty bytesIO
    out_fio = io.BytesIO()
    # Open it as a zip
    with ZipFile(out_fio, 'w') as f:
        # Write each data to a file called name
        for name, data in zip(names, datas):
            f.writestr(name, s_to_b(data))
    # Don't forget to rewind
    out_fio.seek(0)
    return out_fio


def files_from_zip(zip_fio: fileIO):
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
    try:
        ZipFile(zip_fio, 'r')
        return True
    except:
        return False


def nameext_from_path(path: str) -> str:
    nameext = os.path.split(path)[-1]
    return nameext
