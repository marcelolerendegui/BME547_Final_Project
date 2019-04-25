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

from server import app
from flask import request, jsonify
import server.api as api


@app.route("/", methods=["GET"])
def server_on():
    return jsonify("Image Processing Server ON")


@app.route("/api/upload/image", methods=["POST"])
def on_POST_upload_image():
    return jsonify(api.upload_image(request.get_json()))


@app.route("/api/upload/zip", methods=["POST"])
def on_POST_upload_zip():
    return jsonify(api.upload_multiple_images(request.get_json()))


@app.route('/api/image_info/<user_hash>', methods=["GET"])
def on_GET_images_info(user_hash):
    return jsonify(api.get_image_info(user_hash))


@app.route('/api/edit/description', methods=["POST"])
def on_POST_edit_description():
    return jsonify(api.edit_image_description(request.get_json()))


@app.route('/api/edit/filename', methods=["POST"])
def on_POST_edit_filename():
    return jsonify(api.edit_image_filename(request.get_json()))


@app.route('/api/download/', methods=["GET"])
def on_GET_download():
    return jsonify(api.download(request.get_json()))


@app.route('/api/image_process', methods=["POST"])
def on_POST_image_process():
    return jsonify(api.image_process(request.get_json()))


@app.route("/api/log", methods=["GET"])
def on_GET_log():
    return jsonify(api.get_log())
