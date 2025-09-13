import requests
import sys
import os

API_KEY = '7fe4d89eeed500e650dcdd94cfe91cd202c6cca3bb1b9d36f2a366dd39af2965'

def test_status():
    response = requests.get("https://api.gestureboard.com/status", headers={'X-API-Key': API_KEY}, timeout=60)
    assert response.status_code == 200
    assert "status" in response.json()