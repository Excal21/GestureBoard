from time import sleep
import cv2
import os
import json
import keyboard

class Recorder():
    # Kamera inicializálása

    def __init__(self):
        self.url = ''
        
        self.width = 500
        self.height = 500
        self.img_counter = 0
        self.data = None

        self.__gesture_id = None
        self.__gesture_name = None
        self.cap = None


        self.settings_path = os.path.join(os.path.dirname(__file__), '../Config/UserSettings.json')


    def load(self):
        with open(self.settings_path, encoding='UTF-8') as f:
            data = dict(json.load(f))
        self.data = data

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print("loaded")
        self.__gesture_id = int(max(data.keys())) + 1 if data else 0


    def record_batch(self, gesture_name, imgcnt):
        self.img_counter
        self.__gesture_name = gesture_name

        gesture_dir = os.path.join(os.path.dirname(__file__), '../Data/Samples', str(self.__gesture_id))
        if not os.path.exists(gesture_dir):
            os.makedirs(gesture_dir)

        for i in range(imgcnt):
            # Kép közepének kivágása (320x240 pixel)
            ret, frame = self.cap.read()
            y, x, _ = frame.shape
            start_x = x // 2 - 160
            start_y = y // 2 - 120
            end_x = start_x + self.width
            end_y = start_y + self.height
            cropped_frame = frame[start_y:end_y, start_x:end_x]

            img_name = os.path.join(gesture_dir, f'{gesture_name}_{self.img_counter}.png')
            cv2.imwrite(img_name, cropped_frame)
            self.img_counter += 1
            sleep(0.02)


    def save(self):
        self.cap.release()
        gesture_entry = {self.__gesture_id : {'gesture' : self.__gesture_name, 'action' : None}}

        self.data.update(gesture_entry)


        with open(self.settings_path, 'w', encoding='UTF-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        