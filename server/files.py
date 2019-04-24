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


def fileio_to_b64s(fileio):
    b64_bytes = base64.b64encode(fileio)
    return str(b64_bytes, encoding='utf-8')


def b64s_to_fileio(file_b64: str):
    image_bytes = base64.b64decode(file_b64)
    return io.BytesIO(image_bytes)


def create_zip_file(names: list, datas: list):
    out_file = io.BytesIO()
    with ZipFile(out_file, 'w') as f:
        for name, data in zip(names, datas):
            f.writestr(name, data)
    out_file.seek(0)
    return out_file


def create_base64zip_file(names: list, datas: list) -> str:
    out_file = io.BytesIO()
    with ZipFile(out_file, 'w') as f:
        for name, data in zip(names, datas):
            f.writestr(name, data)
    out_file.seek(0)
    return fileio_to_b64s(out_file)


def filenames_in_zip(zip_bytes) -> list:
    with ZipFile(zip_bytes, 'r') as f:
        names = f.namelist()
    return names


def files_from_zip(zip_bytes):
    with ZipFile(zip_bytes, 'r') as f:
        names = f.namelist()
        for name in names:
            file = zip_bytes.open(name, 'rb')
            yield name, file.read()
