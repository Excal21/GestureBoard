import os
from shutil import make_archive
from time import sleep
import requests
from PySide6.QtCore import QThread, Signal
from Models.RecognizerHandler import RecognizerHandler

CHUNK_SIZE = 30 * 1024 * 1024  # 30 MB
API_KEY = '7fe4d89eeed500e650dcdd94cfe91cd202c6cca3bb1b9d36f2a366dd39af2965'

class Trainer(QThread):
    progress = Signal(str)

    filename = 'Images.zip'

    def __init__(self):
        super().__init__()
        self.address = 'http://127.0.0.1:5000'
        self.filename = 'Images.zip'
        self.trained = False
    
    def run(self):
        try:
            response = requests.get(self.address + '/status', headers={'X-API-KEY': API_KEY}, timeout=60)
            if response.status_code == 200:
                if response.json()['status'] == 'idle':
                    if os.path.exists(self.filename):
                        os.remove(self.filename)
                    make_archive('Images', 'zip', 'Data/Samples')
                    
                    if self.upload_in_chunks(self.filename):
                        self.progress.emit('Fájlok sikeresen feltöltve')
                        sleep(1)
                        os.remove(self.filename)
                        self.train()
                    else:
                        self.progress.emit('A kiszolgáló elutasította a fájlokat')
                        sleep(1)
                else:
                    self.progress.emit('A kiszolgáló elfoglalt')
                    sleep(1)
                    self.finished.emit()
            else:
                self.progress.emit('Kiszolgálóhiba')
                sleep(1)
                self.finished.emit()
                return
        except (requests.exceptions.ConnectionError , requests.exceptions.InvalidURL) as e:
            print(e)
            self.progress.emit('Kiszolgáló nem elérhető')
            sleep(1)
            self.finished.emit()
            return

    def upload_in_chunks(self, filepath):
        file_size = os.path.getsize(filepath)
        total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

        with open(filepath, "rb") as f:
            for i in range(total_chunks):
                chunk_data = f.read(CHUNK_SIZE)
                files = {'file': (f"part_{i}", chunk_data)}
                response = requests.post(
                    self.address + '/upload_chunk',
                    headers={'X-API-KEY': API_KEY},
                    files=files
                )
                self.progress.emit(f'Fájlok feltöltése {i + 1}/{total_chunks}')
                
                if response.status_code != 200:
                    self.progress.emit(f"Hiba a {i}. szelet feltöltésekor")
                    return
        
        response = requests.post(self.address + '/merge_chunks',
                                 headers={'X-API-KEY': API_KEY},
                                 json={'filename': 'Images.zip'})
        if response.status_code != 200:
            print(response.json())
            return False

        return True

    def train(self):
        self.progress.emit('Tanítás folyamatban')
        response = requests.get(self.address + '/train', headers={'X-API-KEY': API_KEY})
        if response.status_code == 200:
            with open('Config/gesture_recognizer.task', 'wb') as f:
                f.write(response.content)
            RecognizerHandler.getInstance().reload()
            self.progress.emit('Modell elmentve')
            sleep(1)
            self.trained = True
        else:
            self.progress.emit('Hiba történt a modell letöltése közben')
            sleep(1)
