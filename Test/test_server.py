import io
import os
import zipfile
import pytest
import sys
import shutil
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docker')))

from docker.server import app, API_KEY, training_state


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def cleanup():
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")
    if os.path.exists("Samples"):
        shutil.rmtree("Samples")

def auth_headers():
    return {"X-API-KEY": API_KEY}


def test_auth(client):
    """API_KEY nélkül minden endpoint 404-et adjon"""
    response = client.get("/status")
    assert response.status_code == 404

def test_status(client):
    """Status endpoint adjon vissza busy/idle állapotot"""
    response = client.get("/status", headers=auth_headers())
    assert response.status_code == 200
    assert "status" in response.get_json()

def test_upload_nofile(client):
    """Ha nincs fájl, akkor 400-as hibakód"""
    response = client.post(
        "/upload_chunk",
        headers=auth_headers(),
        data={},
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No file uploaded'}

def test_upload_valid(client):
    zip_filename = os.path.join(os.path.dirname(__file__), 'zip_files', 'Images.zip')
    CHUNK_SIZE = 1024 * 512 * 1
    file_size = os.path.getsize(zip_filename)
    total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

    with open(zip_filename, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            data = {
                "file": (io.BytesIO(chunk_data), f"part_{i}.bin")
            }
            response = client.post(
                "/upload_chunk",
                headers=auth_headers(),
                data=data,
                content_type='multipart/form-data'
            )

            assert response.status_code == 200

    response = client.post(
        "/merge_chunks",
        headers=auth_headers(),
        json={"filename" : "Images.zip"}
    )
   
    cleanup()

    assert response.status_code == 200


def test_upload_file_outside(client):
    zip_filename = os.path.join(os.path.dirname(__file__), 'zip_files', 'BadStructure.zip')


    CHUNK_SIZE = 1024 * 1024 * 10
    file_size = os.path.getsize(zip_filename)
    total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

    with open(zip_filename, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            data = {
                "file": (io.BytesIO(chunk_data), f"part_{i}.bin")
            }
            response = client.post(
                "/upload_chunk",
                headers=auth_headers(),
                data=data,
                content_type='multipart/form-data'
            )

            assert response.status_code == 200

    response = client.post(
        "/merge_chunks",
        headers=auth_headers(),
        json={"filename" : "Images.zip"}
    )
   
    cleanup()

    assert response.json == {'error' : 'Invalid ZIP'}
    assert response.status_code == 400


def test_upload_nested_folder(client):
    zip_filename = os.path.join(os.path.dirname(__file__), 'zip_files', 'BadStructure2.zip')
    CHUNK_SIZE = 1024 * 1024 * 1
    file_size = os.path.getsize(zip_filename)
    total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

    with open(zip_filename, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            data = {
                "file": (io.BytesIO(chunk_data), f"part_{i}.bin")
            }
            response = client.post(
                "/upload_chunk",
                headers=auth_headers(),
                data=data,
                content_type='multipart/form-data'
            )

            assert response.status_code == 200

    response = client.post(
        "/merge_chunks",
        headers=auth_headers(),
        json={"filename" : "Images.zip"}
    )
   
    cleanup()
    
    assert response.json == {'error' : 'Invalid ZIP'}
    assert response.status_code == 400

def test_upload_ZipSlip(client):
    zip_filename = os.path.join(os.path.dirname(__file__), 'zip_files', 'ZipSlip.zip')
    CHUNK_SIZE = 1024 * 1024 * 10
    file_size = os.path.getsize(zip_filename)
    total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

    with open(zip_filename, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            data = {
                "file": (io.BytesIO(chunk_data), f"part_{i}.bin")
            }
            response = client.post(
                "/upload_chunk",
                headers=auth_headers(),
                data=data,
                content_type='multipart/form-data'
            )

            assert response.status_code == 200

    response = client.post(
        "/merge_chunks",
        headers=auth_headers(),
        json={"filename" : "Images.zip"}
    )
   
    cleanup()
    
    assert response.json == {'error' : 'Invalid ZIP'}
    assert response.status_code == 400


def test_upload_NotPNG(client):
    zip_filename = os.path.join(os.path.dirname(__file__), 'zip_files', 'NotPNG.zip')
    CHUNK_SIZE = 1024 * 1024 * 10
    file_size = os.path.getsize(zip_filename)
    total_chunks = (file_size // CHUNK_SIZE) + (1 if file_size % CHUNK_SIZE else 0)

    with open(zip_filename, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(CHUNK_SIZE)
            data = {
                "file": (io.BytesIO(chunk_data), f"part_{i}.bin")
            }
            response = client.post(
                "/upload_chunk",
                headers=auth_headers(),
                data=data,
                content_type='multipart/form-data'
            )

            assert response.status_code == 200

    response = client.post(
        "/merge_chunks",
        headers=auth_headers(),
        json={"filename" : "Images.zip"}
    )
   
    cleanup()
    
    assert response.json == {'error' : 'Invalid ZIP'}
    assert response.status_code == 400
