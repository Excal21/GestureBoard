from time import sleep
import cv2
import os
import json

class Recorder():
    def __init__(self):
        self.url = ''
        
        self.width = 500
        self.height = 500
        self.img_counter = 0
        self.saved_images = 0
        self.data = None
        self.camera = 0
        
        self.frame_counter = 0
        self.cap = None

    def loadCameraOnly(self, camera_idx):
        self.cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)

    def load(self):
        self.loadJSONSettings()

        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        print('loaded')

    def save(self, frame, gesture_id):
        if self.saved_images < 50:
            self.frame_counter += 1
            if self.frame_counter % 2 == 0:
                print('mentés')
                gesture_dir = os.path.join('Data/Samples', str(gesture_id))
                if not os.path.exists(gesture_dir):
                    os.makedirs(gesture_dir)

                img_name = os.path.join(gesture_dir, f'{gesture_id}_{self.img_counter}')
                self.img_counter += 1
                ret, buf = cv2.imencode('.png', frame)
                if ret:
                    with open(img_name, 'wb') as f:
                        f.write(buf.tobytes())
                    print(f'Kép mentve: {img_name}')
                    self.saved_images += 1

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
        if self.cap:
            self.cap.release()
        self.img_counter = 0


    def loadJSONSettings(self):
        with open('Config/CameraSettings.json', encoding='UTF-8') as f:
            data = dict(json.load(f))
        self.camera = data['Camera']
        self.hue_offset = data['HueOffset']


   