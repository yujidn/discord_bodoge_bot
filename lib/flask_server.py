#
# hello.py
#
from flask import Flask, request
from flask_cors import CORS, cross_origin
import ssl
import base64
import cv2
import numpy as np


app = Flask(__name__)
CORS(app)

CERTFILE = "./localhost.pem"


@app.route("/")
def __hello():
    return "Hello World!"


@app.route("/ping")
def __ping():
    return "pong"


@app.route("/image", methods=["POST"])
def __get_image():
    try:
        b64_image = request.form["image"]
    except KeyError:
        return "image not found"

    buf_image = base64.b64decode(b64_image)
    np_image = np.frombuffer(buf_image, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    cv2.imwrite("test.jpg", image)
    return "ok"


def flask_run(port=4433):
    print(f"flask_run port:{port}")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERTFILE)
    app.run(ssl_context=context, host="0.0.0.0", port=port)
