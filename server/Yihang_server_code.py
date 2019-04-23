#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
import sys
import os
import logging
import json
import numpy as np
import base64
import io
import time
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import cv2
import PIL
from PIL import Image
from bson.objectid import ObjectId
from logging import getLogger
from skimage import data, img_as_float
from skimage import exposure
from skimage import util
connect("mongodb+srv://xinyihang1:19950301@bme547-q262c.mongodb.net/Database")
app = Flask(__name__)


# In[2]:


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


# In[3]:


def view_b64_image(base64_string):
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = mpimg.imread(image_buf, format='JPG')
    return i


# In[4]:


@app.route("/", methods=["GET"])
def server_on():
    server_on = "Imgae Process Server is On"
    return server_on


# In[5]:


class image_data(MongoModel):
    user_name = fields.CharField()
    image_name = fields.CharField()
    image_base64 = fields.CharField()
    process_time = fields.FloatField()
    image_size = fields.ListField()
    timestamp = fields.DateTimeField()


# In[6]:


@app.route("/api/upload_image", methods=["POST"])
def add_new_image():
    r = request.get_json()
    p = image_data(image_name=r['image_name'], image_base64=r['image'])
    imgdata = base64.b64decode(p.image_base64)
    im = Image.open(io.BytesIO(imgdata))
    p.image_size = list(im.size)
    p.timestamp = datetime.now()
    p.save()
    return str(200)


# In[7]:


@app.route("/api/show_image/<image_id>", methods=["GET"])
def show_image(image_id):
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    plt.imshow(image64)
    plt.show()
    return str(200)


# In[8]:


@app.route("/api/Histogram_Equalization/<image_id>", methods=["GET"])
def Histogram_Equalization(image_id):
    start = time.time()
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    img_yuv = cv2.cvtColor(image64, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    plt.imshow(img_output)
    plt.show()
    end = time.time()
    pt = (end - start)
    im = Image.fromarray(img_output)
    im.save("your_file.jpeg")
    Histogram_Equalization1 = read_file_as_b64("your_file.jpeg")
    p = image_data(image_name=str(image_id) + "_Histogram_Equalization",
                   image_base64=Histogram_Equalization1,
                   process_time=pt,
                   image_size=f.image_size,
                   timestamp=datetime.now())
    p.save()
    return str(200)


# In[ ]:


@app.route("/api/Contrast_Stretching/<image_id>", methods=["GET"])
def Contrast_Stretching(image_id):
    start = time.time()
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    p2, p98 = np.percentile(image64, (2, 98))
    img_rescale = exposure.rescale_intensity(image64, in_range=(p2, p98))
    plt.imshow(img_rescale)
    plt.show()
    end = time.time()
    pt = (end - start)
    im = Image.fromarray(img_rescale)
    im.save("your_file.jpeg")
    Contrast_Stretching1 = read_file_as_b64("your_file.jpeg")
    p = image_data(image_name=str(image_id) + "_Contrast_Stretching",
                   image_base64=Contrast_Stretching1,
                   process_time=pt,
                   image_size=f.image_size,
                   timestamp=datetime.now())
    p.save()
    return str(200)


# In[ ]:


@app.route("/api/Log_Compression/<image_id>", methods=["GET"])
def Log_Compression(image_id):
    start = time.time()
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    logarithmic_corrected = exposure.adjust_log(image64, 1)
    plt.imshow(logarithmic_corrected)
    plt.show()
    end = time.time()
    pt = (end - start)
    im = Image.fromarray(logarithmic_corrected)
    im.save("your_file.jpeg")
    Log_Compression1 = read_file_as_b64("your_file.jpeg")
    p = image_data(image_name=str(image_id) + "_Log_Compression",
                   image_base64=Log_Compression1,
                   process_time=pt,
                   image_size=f.image_size,
                   timestamp=datetime.now())
    p.save()
    return str(200)


# In[ ]:


@app.route("/api/Reverse_Video/<image_id>", methods=["GET"])
def Reverse_Video(image_id):
    start = time.time()
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    inverted_img = util.invert(image64)
    plt.imshow(inverted_img)
    plt.show()
    end = time.time()
    pt = (end - start)
    im = Image.fromarray(inverted_img)
    im.save("your_file.jpeg")
    Reverse_Video1 = read_file_as_b64("your_file.jpeg")
    p = image_data(image_name=str(image_id) + "_Reverse_Video",
                   image_base64=Reverse_Video1,
                   process_time=pt,
                   image_size=f.image_size,
                   timestamp=datetime.now())
    p.save()
    return str(200)


# In[ ]:


@app.route("/api/Compare/<image_id>", methods=["GET"])
def Compare(image_id):
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    f1 = image_data.objects.raw(
        {'image_name': str(image_id) + "_Contrast_Stretching"}).first()
    image641 = view_b64_image(f1.image_base64)
    f2 = image_data.objects.raw(
        {'image_name': str(image_id) + "_Log_Compression"}).first()
    image642 = view_b64_image(f2.image_base64)
    f3 = image_data.objects.raw(
        {'image_name': str(image_id) + "_Reverse_Video"}).first()
    image643 = view_b64_image(f3.image_base64)
    plt.figure(1)
    plt.subplot(221)
    plt.imshow(image64)
    plt.subplot(222)
    plt.imshow(image641)
    plt.subplot(223)
    plt.imshow(image642)
    plt.subplot(224)
    plt.imshow(image643)
    plt.show()
    return str(200)


# In[ ]:


@app.route("/api/Color_Histogram/<image_id>", methods=["GET"])
def Color_Histogram(image_id):
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    image64 = view_b64_image(f.image_base64)
    img = image64
    color = ('b', 'g', 'r')
    for channel, col in enumerate(color):
        histr = cv2.calcHist([img], [channel], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title('Histogram for color scale picture')
    plt.show()
    return str(200)


# In[ ]:


@app.route("/api/Download/<image_id>", methods=["GET"])
def Download(image_id):
    f = image_data.objects.raw({'image_name': str(image_id)}).first()
    data = f.image_base64
    return jsonify(data)


# In[ ]:


if __name__ == '__main__':
    app.run(host='0.0.0.0')
