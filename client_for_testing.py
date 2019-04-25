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

user_hash = 'test_user1234'


# UPLOAD SINGLE IMAGE
with open('img.jpg', 'rb') as f:
    img_b64s = fio_to_b64s(f)

d1 = {
    'filename': 'google_logo.jpg',
    'description': 'This is the Google Logo',
    'user_hash': user_hash,
    'data': img_b64s,
}

r1 = requests.post(server+"/api/upload/image", json=d1)


# GET IMAGES INFO
r2 = requests.get(server+"/api/image_info/"+user_hash)


# UPLOAD ZIP
with open('images.zip', 'rb') as f:
    zip_b64s = fio_to_b64s(f)


d3 = {
    'filename': 'all_images.zip',
    'user_hash': user_hash,
    'data': zip_b64s,
}
r3 = requests.post(server+"/api/upload/zip", json=d3)

# GET IMAGES INFO
r4 = requests.get(server+"/api/image_info/"+user_hash)


# DOWNLOAD SIGNLE IMAGE
d5 = {
    'image_ids': ['5cc20e864be36254d29598ee'],
    'format': 'PNG',
    'user_hash': user_hash
}

r5 = requests.get(server+"/api/download/", json=d5)

dout = json.loads(r5.text)

im_fio = b64s_to_fio(dout['data'])
image = Image.open(im_fio)
image.show()


d6 = {
    'image_id': '5cc1f6fd4be3623f1b8fbe07',
    'algorithm': 'No Algorithm',
    'out_image_format': 'PNG',
    'out_image_filename': 'Processed Google Logo',
    'user_hash': user_hash,
}
r6 = requests.post(server+"/api/image_process", json=d6)


# DOWNLOAD MULTIPLE IMAGE
d7 = {
    'image_ids': ['5cc1f1484be362389edd1a0e', '5cc20e864be36254d29598ed', '5cc20e864be36254d29598ee', '5cc20e874be36254d29598f3'],
    'format': 'PNG',
    'user_hash': user_hash
}

r7 = requests.get(server+"/api/download/", json=d7)

dout = json.loads(r7.text)

zip_fio = b64s_to_fio(dout['data'])

zip_fio.seek(0)

f = open("test.zip", 'wb+')
zip_b = fio_to_b(zip_fio)
f.write(zip_b)
f.close()
