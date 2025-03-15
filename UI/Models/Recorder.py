from time import sleep
import cv2
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data')))

class Recorder():
    def __init__(self):
        self.url = ''
        
        self.width = 500
        self.height = 500
        self.img_counter = 0
        self.data = None
        self.camera = 0

        self.__gesture_id = None
        self.__gesture_name = None
        self.cap = None

    def loadCameraOnly(self, camera_idx):
        self.cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)

    def load(self, data):
        self.loadJSONSettings()

        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        self.__gesture_id = int(max(data.keys())) + 1 if len(data) > 0 else 0
        print('loaded')


    def record_batch(self, gesture_name, imgcnt):
        self.img_counter

        gesture_dir = os.path.join('Data/Samples', str(self.__gesture_id))
        if not os.path.exists(gesture_dir):
            os.makedirs(gesture_dir)

        for i in range(imgcnt):
            frame = self.getFrame()
            if frame is not None:
                h, w, _ = frame.shape

                center_x, center_y = w // 2, h // 2
                crop_width, crop_height = 500, 300
                x1, x2 = center_x - crop_width // 2, center_x + crop_width // 2
                y1, y2 = center_y - crop_height // 2, center_y + crop_height // 2

                cropped_frame = frame[y1:y2, x1:x2].copy()  # C-contiguous hiba elkerülése miatt

                img_name = os.path.join(gesture_dir, f'{gesture_name}_{self.img_counter}.png')
                cv2.imwrite(img_name, cropped_frame)
                self.img_counter += 1

                sleep(0.02)

    def getFrame(self, manual_hue_offset = -1):
        frame = self.cap.read()[1]
        if frame is not None:
            hue_offset = manual_hue_offset if manual_hue_offset != -1 else self.hue_offset
            if hue_offset != 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame[:, :, 0] += hue_offset
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        return frame


    def release(self):
        self.cap.release()
        self.img_counter = 0


    def loadJSONSettings(self):
        with open('Config/CameraSettings.json', encoding='UTF-8') as f:
            data = dict(json.load(f))
        self.camera = data['Camera']
        self.hue_offset = data['HueOffset']


    def getCameras(self):
        index = 0
        cameras = []
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                break
            cameras.append(index)
            cap.release()
            index += 1
        return cameras