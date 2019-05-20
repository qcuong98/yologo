"""
    Receive a multipart data with field file
    Return a json file has 3 field 
        ("objects" ("class", "conf", "bbox" ("x", "y", "w", "h")), "code", "description")
    curl -F "file=@image.png" 0.0.0.0:8080
"""
import os
import sys
import tempfile

import cv2
import matplotlib.pyplot as plt

from flask import Flask, request, jsonify, render_template
from werkzeug import secure_filename

import model

ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'tif', 'tiff'])

app = Flask(__name__)
app.config['TEMP_FOLDER'] = '/tmp/'
app.secret_key = 'qcuong98 super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def run_model(files, model_id):
    result = {
        "objects": [],
        "code": -1,
        "description": "Processing"
    }

    try:
        if 'file' not in files:
            result["code"] = 1
            result["description"] = "Invalid request data"
            return jsonify(result), 400
        
        file = files['file']
        if allowed_file(file.filename):    
            safe_name = secure_filename(file.filename)
            _, temp_name = tempfile.mkstemp(
                                    prefix = safe_name.split('.')[-2] + "_", 
                                    suffix = "." + safe_name.split('.')[-1])
            file_dir = os.path.join(app.config['TEMP_FOLDER'], temp_name)
            file.save(file_dir)

            image = cv2.imread(file_dir)

            if os.path.exists(file_dir):
                os.remove(file_dir)

            objs = model.detect(model_id, image)
            for obj in objs:
                x, y, w, h = obj[2]
                result["objects"].append({
                    "class": obj[0].decode('UTF-8'),
                    "conf": obj[1],
                    "bbox": {
                        "x": int(x - w/2),
                        "y": int(y - h/2),
                        "w": int(w),
                        "h": int(h)
                    }
                })
            result["code"] = 0
            result["description"] = "OK"
            return jsonify(result), 200
        else:
            result["code"] = 2
            result["description"] = "File extension isn't supported"
            return jsonify(result), 400

    except Exception as e:
            result["code"] = -1
            result["description"] = "Error: %s" % e
            return jsonify(result), 500


@app.route("/model_1", methods = ["POST"])
def use_model_1():
    return run_model(request.files, model_1)
    
@app.route("/model_2", methods = ["POST"])
def use_model_2():
    return run_model(request.files, model_2)

@app.route("/", methods = ["GET"])
def demo():
    return render_template('home.html')

model_1 = model.get_model("cfg/coco.data", "cfg/yolov3.cfg", "weights/yolov3.weights")
model_2 = model.get_model("cfg/yologo.data", "cfg/yologo.cfg", "weights/yologo.weights")

if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port = 8080)