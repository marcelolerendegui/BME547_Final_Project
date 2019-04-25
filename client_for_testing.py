from server.files import *
import requests
from zipfile import ZipFile
import base64
import io
from PIL import Image
from server.files import *
import json


server = "http://127.0.0.1:5000"
user = "username"
password = "password"
user_hash = '12345'


# # UPLOAD SINGLE IMAGE
# with open('img.jpg', 'rb') as f:
#     img_b64s = fio_to_b64s(f)
#
# d1 = {
#     'filename': 'test_string.jpg',
#     'description': 'This is a fake image file with a string in it',
#     'user_hash': user_hash,
#     'data': img_b64s,
# }
#
# r1 = requests.post(server+"/api/upload/image", json=d1)
#
#
# # GET IMAGES INFO
# r2 = requests.get(server+"/api/image_info/"+user_hash)
#
#
# # UPLOAD ZIP
# with open('images.zip', 'rb') as f:
#     zip_b64s = fio_to_b64s(f)
#
#
# d3 = {
#     'filename': 'images.zip',
#     'user_hash': user_hash,
#     'data': zip_b64s,
# }
# r3 = requests.post(server+"/api/upload/zip", json=d3)
#
# # GET IMAGES INFO
# r4 = requests.get(server+"/api/image_info/"+user_hash)


# DOWNLOAD SIGNLE IMAGE
d5 = {
    'image_ids': ['5cc11a534be3624bad079e23'],
    'format': 'PNG',
    'user_hash': user_hash
}

r5 = requests.get(server+"/api/download/", json=d5)

dout = json.loads(r5.text)

im_fio = b64s_to_fio(dout['data'])
image = Image.open(im_fio)
image.show()
