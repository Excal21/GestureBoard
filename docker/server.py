import os
import threading
from flask import Flask, request, jsonify, send_file, abort
import shutil
import zipfile

from train import *

app = Flask(__name__)
training_state = {'status': 'idle'}
t1 = None

UPLOAD_DIR = "uploads"

API_KEY = '7fe4d89eeed500e650dcdd94cfe91cd202c6cca3bb1b9d36f2a366dd39af2965'


def safe_unzip(zip_path, extract_to, max_size=400*1024*1024):
    deleteImages()

    base_abs = os.path.abspath(extract_to)
    os.makedirs(base_abs, exist_ok=True)

    PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
    total_size = 0


    with zipfile.ZipFile(zip_path, 'r') as z:
        for member in z.infolist():
            dest_abs = os.path.abspath(os.path.join(base_abs, member.filename))
            if not dest_abs.startswith(base_abs + os.sep):
                raise ValueError("Unsafe zip file: path traversal detected")

            parts = [p for p in member.filename.strip("/").split("/") if p]

            if not parts:
                continue

            if member.is_dir():
                #STRUCTURE
                if len(parts) != 1:
                    print(f"Invalid zip structure in {member.filename}: nested folders are not allowed")
                    raise ValueError("Invalid zip structure: nested folders are not allowed")
                continue

            #STRUCTURE
            if len(parts) != 2:
                print(f"Invalid zip structure in {member.filename}: files must be directly inside one subfolder")
                raise ValueError("Invalid zip structure: files must be directly inside one subfolder")

            #ZIP BOMB
            total_size += member.file_size
            if total_size > max_size:
                print(f"Unzipped data too large: {total_size} > {max_size}")
                raise ValueError("Unzipped data too large")

            #PNG MAGIC
            with z.open(member, 'r') as f:
                header = f.read(8)
                if header != PNG_MAGIC:
                    print(f"Invalid file type in {member.filename}: only PNG images are allowed (no extension expected)")
                    raise ValueError("Invalid file type: only PNG images are allowed (no extension expected)")

        z.extractall(base_abs)


@app.before_request
def check_auth():
    if request.headers.get('X-API-KEY') != API_KEY:
        abort(404)


@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    i = 0
    while True:
        save_path = os.path.join(UPLOAD_DIR, f"part_{i}")
        if not os.path.exists(save_path):
            break
        i += 1

    file.save(save_path)
    return jsonify({'message': f'part_{i} received'}), 200


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

    if final_filename.lower().endswith('.zip'):
        try:
            
            safe_unzip(final_path, 'Samples')
        except Exception as e:
            print(e)
            return jsonify({'error': f'Invalid ZIP'}), 400

    if os.path.exists('gesture_recognizer.task'):
        os.remove('gesture_recognizer.task')

    training_state['status'] = 'busy'

    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)

    return jsonify({'message': 'Chunks merged and training started'}), 200


@app.route('/train', methods=['GET'])
def train():
    try:
        ModelTrainer.train()
        training_state['status'] = 'idle'
        
        deleteImages()

        return send_file('gesture_recognizer.task', as_attachment=True)

    except Exception as e:
        training_state['status'] = 'idle'
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    if t1 is not None and t1.is_alive():
        training_state['status'] = 'busy'
    elif t1 is not None and not t1.is_alive() and training_state['status'] == 'busy':
        training_state['status'] = 'idle'
    return jsonify(training_state)


def deleteImages():
    if os.path.exists('Samples'):
        for item in os.listdir('Samples'):
            item_path = os.path.join('Samples', item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    
    if os.path.exists('Images.zip'):
        os.remove('Images.zip')

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
    app.run(host='0.0.0.0', port=5000)
