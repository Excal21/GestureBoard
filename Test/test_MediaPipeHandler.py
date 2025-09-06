import pytest
import sys
from App.Models.MediaPipeHandler import MediapipeLoader

def test_module_imports():
    loader = MediapipeLoader()
    loader.run()

    assert 'os' in sys.modules
    assert 'cv2' in sys.modules
    assert 'mediapipe' in sys.modules
    assert 'mediapipe.framework.formats.landmark_pb2' in sys.modules
    assert 'mediapipe.tasks.python' in sys.modules
    assert 'numpy' in sys.modules
    assert 'datetime' in sys.modules
    assert 'shutil' in sys.modules
    assert 'pyautogui' in sys.modules