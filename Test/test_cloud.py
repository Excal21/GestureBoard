import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App')))

from App.Models.Trainer import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App'))
os.chdir(project_root)


def test_status():
    response = requests.get("https://api.gestureboard.com/status", headers={'X-API-Key': API_KEY}, timeout=60)
    assert response.status_code == 200
    assert "status" in response.json()