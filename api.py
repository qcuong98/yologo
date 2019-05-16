"""
    Receive a multipart data with field file
    Return a json file has 5 field 
        ("objects" ("class", "conf", "bbox" ("x", "y", "w", "h")), "code", "description")
    curl -F "file=@image.png" 0.0.0.0:8000
"""
import os
import sys
import tempfile

import cv2
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'tif', 'tiff'])

app = Flask(__name__)
app.config['TEMP_FOLDER'] = '/tmp/'
app.secret_key = 'qcuong98 super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods = ["POST"])
def upload_file():
    if request.method == "POST":
        result = {
            "objects": [],
            "code": -1,
            "description": "Processing"
        }

        if 'file' not in request.files:
            result["code"] = 1
            result["description"] = "No 'file' field in request data"
            return jsonify(result), 400
        
        file = request.files['file']
        if allowed_file(file.filename):
            try:
                safe_name = secure_filename(file.filename)
                _, temp_name = tempfile.mkstemp(\
                                        prefix = safe_name.split('.')[-2] + "_", 
                                        suffix = "." + safe_name.split('.')[-1])
                file_dir = os.path.join(app.config['TEMP_FOLDER'], temp_name)
                file.save(file_dir)

                return file_dir, 200

                # if os.path.exists(file_dir):
                #     os.remove(file_dir)
                # return jsonify(result), 200
            except Exception as e:
                result["code"] = -1
                result["description"] = "Error: %s" % e
                return jsonify(result), 500
        else:
            result["code"] = 2
            result["description"] = "File extension isn't supported (bmp, png, jpg, jpeg, tif, tiff)"
            return jsonify(result), 400

if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 8000, debug = True)