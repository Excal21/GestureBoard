import os
import threading
from flask import Flask, request, jsonify, send_file
import shutil

from train import *

app = Flask(__name__)
training_state = {'status': 'idle'}
t1 = None

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

API_KEY = 'secret'

@app.before_request
def check_auth():
    if request.headers.get('X-API-KEY') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    file = request.files['file']
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)
    return jsonify({'message': f'{file.filename} received'}), 200

@app.route('/merge_chunks', methods=['POST'])
def merge_chunks():
    data = request.get_json()
    final_filename = data.get('filename', 'Images.zip')
    final_path = os.path.join(UPLOAD_DIR, final_filename)

    with open(final_path, "wb") as outfile:
        i = 0
        while True:
            part_path = os.path.join(UPLOAD_DIR, f"part_{i}")
            if not os.path.exists(part_path):
                break
            with open(part_path, "rb") as infile:
                shutil.copyfileobj(infile, outfile)
            i += 1

    if final_filename.endswith('.zip'):
        shutil.unpack_archive(final_path, 'Samples')

    global t1
    t1 = threading.Thread(target=ModelTrainer.train)
    t1.start()
    training_state['status'] = 'busy'

    return jsonify({'message': 'Chunks merged and training started'}), 200

@app.route('/status', methods=['GET'])
def status():
    if t1 is not None and t1.is_alive():
        training_state['status'] = 'busy'
    elif t1 is not None and not t1.is_alive() and training_state['status'] == 'busy':
        training_state['status'] = 'idle'
    return jsonify(training_state)

@app.route('/download', methods=['GET'])
def download():
    return send_file('gesture_recognizer.task', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
