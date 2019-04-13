
from flask import request, jsonify, send_file
from flask import Flask

app = Flask(__name__)


@app.route('/api/img/<img_id>', methods=["GET"])
def on_GET_img_by_id(img_id):
    if img_id == '1':
        filename = 'ok.gif'
    else:
        filename = 'error.gif'

    return send_file(filename, mimetype='image/gif')


app.run(debug=True)
