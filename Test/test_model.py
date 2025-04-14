import os
from mediapipe.tasks import python
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)

@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_modelFile():

    config_path = os.path.abspath(os.path.join(project_root, 'Config', 'gesture_recognizer.task'))
    assert os.path.exists(config_path), f'Modellfájl nem található {config_path}'

    try:
        with open(config_path, 'rb') as model_file:
            model_data = model_file.read()
            base_options = python.BaseOptions(model_asset_buffer=model_data)

            options = python.vision.GestureRecognizerOptions(base_options=base_options)
            recognizer = python.vision.GestureRecognizer.create_from_options(options)

        assert recognizer is not None, 'A Gesture Recognizer task fájlt nem lehetett betölteni'
    except Exception as e:
        assert False, f'A Gesture Recognizer task betöltésekor kivétel keletkezett: {e}'