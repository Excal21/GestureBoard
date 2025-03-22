import os
import sys
from shutil import make_archive
from time import sleep
import requests
from PySide6.QtCore import QThread, Signal
from Models.RecognizerHandler import RecognizerHandler

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data")))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Models")))


class Trainer(QThread):
    finished = Signal()
    progress = Signal(str)

    filename = 'Images.zip'
    
    def __init__(self):
        super().__init__()
        self.ip = '127.0.0.1'
        self.port = '5000'
        self.filename = 'Images.zip'
    
    def run(self):
        make_archive('Images', 'zip', 'Data\\Samples')
        with open(self.filename, 'rb') as file:
            files = {'file': file}
            response = requests.post('http://' + self.ip + ':' + self.port + '/upload', headers={'X-API-KEY' : 'secret'}, files=files)
            if(response.status_code == 200):
                self.progress.emit('Fájlok sikeresen feltöltve')
                response = requests.get('http://' + self.ip + ':' + self.port + '/status', headers={'X-API-KEY': 'secret'})
                if response.json()['status'] == 'busy':
                    self.progress.emit('Tanítás folyamatban')
            
        os.remove(self.filename)
        trained = False
        while not trained:
            response = requests.get('http://' + self.ip + ':' + self.port + '/status', headers={'X-API-KEY': 'secret'})
            if response.json()['status'] == 'idle':
                trained = True
                self.progress.emit('Tanítás kész')
            else:
                sleep(5)

        if trained:
            response = requests.get('http://' + self.ip + ':' + self.port + '/download',
                        headers={'X-API-KEY': 'secret'})
            
            if response.status_code == 200:
                with open('Config\\gesture_recognizer.task', 'wb') as f:
                    f.write(response.content)
                RecognizerHandler.getInstance().reload()
                self.progress.emit('Modell elmentve')
            else:
                self.progress.emit('Hiba történt a modell letöltése közben')
            self.finished.emit()