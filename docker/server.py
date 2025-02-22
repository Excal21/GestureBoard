import os
from flask import Flask, request, jsonify, send_file
import shutil

from train import *

app = Flask(__name__)

# API kulcs beállítása
API_KEY = 'secret' #Ezt majd hashelni kell


# API-kulcs ellenőrzése
@app.before_request
def check_auth():
    if request.headers.get('X-API-KEY') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    if file and file.filename.endswith('.zip'):
        shutil.unpack_archive(file.filename, 'Samples')
        
    train()
    return jsonify({"message": "File uploaded successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
