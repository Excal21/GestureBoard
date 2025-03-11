from time import sleep
import cv2
import os
import json

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


        #self.settings_path = os.path.join(os.path.dirname(__file__), '../Config/UserSettings.json')


    def load(self, data):
        # with open(self.settings_path, encoding='UTF-8') as f:
        #     data = dict(json.load(f))
        self.data = data

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.__gesture_id = int(max(data.keys())) + 1 if len(data) > 0 else 0
        print('loaded')


    def record_batch(self, gesture_name, imgcnt):
        self.img_counter
        self.__gesture_name = gesture_name

        gesture_dir = os.path.join(os.path.dirname(__file__), '../Data/Samples', str(self.__gesture_id))
        if not os.path.exists(gesture_dir):
            os.makedirs(gesture_dir)

        for i in range(imgcnt):
            ret, frame = self.cap.read()
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


    def save(self):
        self.cap.release()
        # gesture_entry = {self.__gesture_id : {'gesture' : self.__gesture_name, 'action' : None}}

        # self.data.update(gesture_entry)


        # with open(self.settings_path, 'w', encoding='UTF-8') as f:
        #     json.dump(self.data, f, ensure_ascii=False, indent=4)


        