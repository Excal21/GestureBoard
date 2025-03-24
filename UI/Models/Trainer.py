import os
import sys
from shutil import make_archive
from time import sleep
import requests
from PySide6.QtCore import QThread, Signal
from Models.RecognizerHandler import RecognizerHandler

class Trainer(QThread):
    progress = Signal(str)

    filename = 'Images.zip'



    def __init__(self):
        super().__init__()
        self.ip = '127.0.0.1'
        self.filename = 'Images.zip'
        self.trained = False
    
    def run(self):
        try:
            response = requests.get('http://' + self.ip + '/status', headers={'X-API-KEY': 'secret'})
            if response.status_code == 200:
                if response.json()['status'] == 'idle':
                    if os.path.exists(self.filename):
                        os.remove(self.filename)
                    make_archive('Images', 'zip', 'Data\\Samples')
                    with open(self.filename, 'rb') as file:
                        files = {'file': file}
                        response = requests.post('http://' + self.ip + '/upload', headers={'X-API-KEY' : 'secret'}, files=files)
                    if(response.status_code == 200):
                        self.progress.emit('Fájlok sikeresen feltöltve')
                        #response = requests.get('http://' + self.ip + ':' + self.port + '/status', headers={'X-API-KEY': 'secret'})
                        sleep(1)
                        os.remove(self.filename)
                        self.train()
                else:
                    self.progress.emit('A kiszolgáló elfoglalt')
                    sleep(1)
                    self.finished.emit()

            else:
                self.progress.emit('Kiszolgálóhiba')
                print('Kiszolgálóhiba')
                sleep(1)
                self.finished.emit()
                return
        except (requests.exceptions.ConnectionError , requests.exceptions.InvalidURL):
            print('Kiszolgáló nem elérhető')
            self.progress.emit('Kiszolgáló nem elérhető')
            sleep(1)
            self.finished.emit()
            return

    def train(self):
        while not self.trained:
            response = requests.get('http://' + self.ip + '/status', headers={'X-API-KEY': 'secret'})
            if response.json()['status'] == 'idle':
                self.trained = True
                self.progress.emit('Tanítás kész')
                sleep(1)
            elif response.json()['status'] == 'busy':
                self.progress.emit('Tanítás folyamatban')
                sleep(5)

        if self.trained:
            response = requests.get('http://' + self.ip + '/download',
                        headers={'X-API-KEY': 'secret'})
            
            if response.status_code == 200:
                with open('Config\\gesture_recognizer.task', 'wb') as f:
                    f.write(response.content)
                RecognizerHandler.getInstance().reload()
                self.progress.emit('Modell elmentve')
                self.trained = True
                #self.finished.emit()
            else:
                self.progress.emit('Hiba történt a modell letöltése közben')
                sleep(1)
                #self.finished.emit()