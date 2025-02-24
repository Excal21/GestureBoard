import os
from shutil import make_archive
from time import sleep
import requests

make_archive('Images', 'zip', 'Samples')


url = 'http://localhost:5000/upload'
filename = 'Images.zip'

with open(filename, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, headers={'X-API-KEY' : 'secret'}, files=files)
    if(response.status_code == 200):
        print('File uploaded successfully')
        os.remove(filename)
        response = requests.get('http://localhost:5000/status', headers={'X-API-KEY': 'secret'})
        if response.json()['status'] == 'busy':
            print('Training started')
    
    trained = False
    while not trained:
        response = requests.get('http://localhost:5000/status', headers={'X-API-KEY': 'secret'})
        if response.json()['status'] == 'idle':
            trained = True
            print('Training finished')
        else:
            sleep(5)
    if trained:
        response = requests.get('http://localhost:5000/download',
                    headers={'X-API-KEY': 'secret'})
        
        if response.status_code == 200:
            with open('gesture_recognizer.task', 'wb') as f:
                f.write(response.content)
            print('Model received')
        else:
            print('Training failed')