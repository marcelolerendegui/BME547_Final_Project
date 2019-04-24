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


def s_to_fio(s):
    fio = io.BytesIO(s.encode('utf8'))
    return fio


def fio_to_s(fio):
    s = fio.read().decode('utf8')
    return s


def fio_to_b64s(fio):
    b64s = str(base64.b64encode(fio.read()), encoding='utf-8')
    return b64s


def b64s_to_fio(b64s: str):
    fio = io.BytesIO(base64.b64decode(b64s))
    return fio


def create_zip_fio(names: list, datas: list):
    out_fio = io.BytesIO()
    with ZipFile(out_fio, 'w') as f:
        for name, data in zip(names, datas):
            f.writestr(name, data)
    out_fio.seek(0)
    return out_fio


def files_from_zip(zip_bytes):
    with ZipFile(zip_bytes, 'r') as f:
        names = f.namelist()
        for name in names:
            file = zip_bytes.open(name, 'rb')
            yield name, file.read()
