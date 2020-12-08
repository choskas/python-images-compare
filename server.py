import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import cv2
import json
import numpy as np
import urllib.request as urllib
import requests
from flask_cors import CORS

#cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag, delete_resources
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary

app = Flask(__name__)
CORS(app)
project_folder = os.path.expanduser('~/images-compare')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

#CLOUDINARY function handler
cloudinary.config(
cloud_name = "choskas", 
api_key = API_KEY, 
api_secret = API_SECRET 
)


def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))

#API QUE CHECA LA PRIMERA IMAGEN
@app.route('/upload-image')
def upload_files():
    print("--- Upload a local file")
    isDifferent = False
    response = upload("img/escala.jpg", tags="")
    dump_response(response)
    url, options = cloudinary_url(
        response['public_id'],
        format=response['format'],
    )
    public_id = response['public_id']
    url_response = urllib.urlopen(url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    duplicate = cv2.imdecode(img_array, -1)
    originalUrl = "https://res.cloudinary.com/choskas/image/upload/v1607385168/cg9lnefzs5wbdslubtzz.jpg"
    url_response2 = urllib.urlopen(originalUrl)
    img_array2 = np.array(bytearray(url_response2.read()), dtype=np.uint8)
    original = cv2.imdecode(img_array2, -1)
    print(duplicate, original)
    # duplicate = cv2.imread(img)
    image1 = original.shape
    image2 = duplicate.shape
    print(image1, image2)
    if original.shape == duplicate.shape:
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
        print(b, g, r)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            print("Las imagenes son iguales")
            delete_resources(public_id)
            url = ""
        else:
            print("las imagenes son diferentes")
            print("mostando la imagen diferente ->")
            isDifferent = True
    return jsonify({"isComplete": True, "url": url, "isDifferent" : isDifferent})
##################################################

    

if __name__ == '__main__':
    app.run(debug=True, port=3000)
