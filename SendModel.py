from shutil import make_archive
import requests

#make_archive('Images', 'zip', 'Samples')


url = "http://localhost:5000/upload"
filename = "Images.zip"

with open(filename, "rb") as file:
    files = {"file": file}
    response = requests.post(url, headers={'X-API-KEY' : 'secret'}, files=files)