import os
import threading
from flask import Flask, request, jsonify, send_file
import shutil

from train import *

app = Flask(__name__)
training_state = {'status': 'idle'}
t1 = None

# API kulcs beállítása
API_KEY = 'secret' #Ezt majd hashelni kell

# API-kulcs ellenőrzése
@app.before_request
def check_auth():
    if request.headers.get('X-API-KEY') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

@app.route('/upload', methods=['POST'])
def upload():
    global t1
    file = request.files['file']
    file.save(file.filename)
    if file and file.filename.endswith('.zip'):
        shutil.unpack_archive(file.filename, 'Samples')
    
    t1 = threading.Thread(target=ModelTrainer.train)
    t1.start()
    training_state['status'] = 'busy'

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/status', methods=['GET'])
def status():
    if t1 is not None and t1.is_alive():
        training_state['status'] = 'busy'
        print('busy')
    elif t1 is not None and not t1.is_alive() and training_state['status'] == 'busy':
        training_state['status'] = 'idle'
        print('idle')
    return jsonify(training_state)

@app.route('/download', methods=['GET'])
def download():
    return send_file('gesture_recognizer.task', as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
