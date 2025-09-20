# A projekt a Google MediaPipe moduljára és a hozzá tartozó példakódok egyes elemeire épül.
# Bővebb információ Google MediaPiperól az alábbi linken érhető el:
# https://ai.google.dev/edge/mediapipe

import os
import sys
import cv2
import numpy as np
import shutil
import pyautogui
import json
from mediapipe import solutions, Image, ImageFormat
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from datetime import datetime
from collections import Counter, deque
from Models.MouseProcessor import MouseProcessor

class Recognizer:
    def __init__(self, task_file_path: str, config_path: str):
        self.MARGIN = 10
        self.FONT_SIZE = 1
        self.FONT_THICKNESS = 1
        self.__task_file_path = task_file_path

        self.mp_hands = solutions.hands
        self.mp_drawing = solutions.drawing_utils
        self.mp_drawing_styles = solutions.drawing_styles

        # Modelfájl betöltése és beállítása
        with open(self.__task_file_path, "rb") as model_file:
            self.model_data = model_file.read()
        self.base_options = python.BaseOptions(model_asset_buffer=self.model_data)

        self.options = python.vision.GestureRecognizerOptions(
            base_options=self.base_options,
            min_tracking_confidence=0.8,
            num_hands=4
        )
        self.recognizer = python.vision.GestureRecognizer.create_from_options(self.options)

        self.mouse_active = False
        self.framethrottling_prevstate = None

        self.mouse_processor = MouseProcessor()


        self.camera = 0
        self.confidence = 0.5
        self.stop = False
        self.commands = {}
        self.camerafeed = True
        self.framecount = 5
        self.hueoffset = 0
        self.distance = 500
        self.delay = 1
        self.error = False
        self.configpath = config_path

    def reloadModel(self):
        with open(self.__task_file_path, "rb") as model_file:
            self.model_data = model_file.read()
        self.base_options = python.BaseOptions(model_asset_buffer=self.model_data)

        self.options = python.vision.GestureRecognizerOptions(
            base_options=self.base_options,
            min_tracking_confidence=0.7,
            num_hands=4
        )
        self.recognizer = python.vision.GestureRecognizer.create_from_options(self.options)

    #region Markpont vizualicáció
    def draw_landmarks_on_image(self, rgb_image, detection_result):
        #FORRÁS: GOOGLE MEDIAPIPE HAND LANDMARKS VISUALIZATION UTILITIES

        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                ) for landmark in hand_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_utils.DrawingSpec(
                    color=(33, 43, 53), thickness=2, circle_radius=4
                ),
                solutions.drawing_utils.DrawingSpec(
                    color=(156, 220, 254), thickness=2
                )
            )
        return annotated_image
    #endregion

#region Annotáció
    def annotateImage(self, image, gestures=False, distance=500):
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_image = Image(image_format=ImageFormat.SRGB, data=img)

        result = self.recognizer.recognize(mp_image)

        if result.handedness:
            lm0 = result.hand_landmarks[0][0]   # 0. markpont
            lm9 = result.hand_landmarks[0][9]   # 9. markpont
            lm05 = result.hand_landmarks[0][5]  # 5. markpont
            lm17 = result.hand_landmarks[0][17] # 17. markpont

            distance_09 = ((lm0.x - lm9.x) ** 2 + (lm0.y - lm9.y) ** 2) ** 0.5
            distance_09 = 500 - int(distance_09 * 1000)

            distance_517 = ((lm05.x - lm17.x) ** 2 + (lm05.y - lm17.y) ** 2) ** 0.5
            distance_517 = 460 - int(distance_517 * 1000)  # Az 5-17 távolság kisebb, mint a 0-9

            #print(f'Távolság: {distance_09}, 5-17 távolság: {distance_517}')

            if distance_09 <= distance or distance_517 <= distance:
                annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), result)
                annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

                if gestures:
                    if len(result.gestures) >= 1:
                        gestureidx = result.gestures[0][0].category_name
                        if gestureidx and gestureidx != 'NONE':
                            return annotated_image, (gestureidx, round(result.gestures[0][0].score * 100, 2))

                return annotated_image, None

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB), None
#endregion

#region Konfiguráció betöltők
    def loadGestures(self):
        with open(self.configpath, "r", encoding='UTF-8') as file:
            data = dict(json.load(file))
        return data

    def loadCameraSettings(self):
        with open('Config/CameraSettings.json', encoding='UTF-8') as f:
            data = dict(json.load(f))
            self.camera = data['Camera']
            self.framecount = data['FrameCount']
            self.confidence = data['Confidence']
            self.hueoffset = data['HueOffset']
            self.distance = data['Distance']
            self.delay = data['Delay']
            self.framethrottling = data['FrameThrottling']
            self.mouse_processor.sensitivity = data['Sensitivity']
            self.mouse_processor.overlay_circle.setRadius(data['Drift'])
            self.mouse_processor.radius = data['Drift']
            self.mouse_processor.invert = data['InvertButtons']
#endregion

#region Felismerő
    def Run(self):
        print('Recognizer started')
        self.loadCameraSettings()
        gesture_mappings = self.loadGestures()
        self.stop = False
        cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        cap.setExceptionMode(True)

        if not cap.isOpened():
            cap.open(self.camera)

        if not cap.isOpened():
            print("Nem sikerült megnyitni a kamerát")
            self.error = True
            return

        cap.set(cv2.CAP_PROP_FPS, 30)

        last_gestures = deque(maxlen=self.framecount)
        last_gesture_time = datetime.now()

        skip_frames = False
        frame_index = 0
        no_gesture_count = 0

        mouse_gesture = next((key for key, value in gesture_mappings.items() if value.get('action') == 'self.toggleMouseMode()'), None)

        #region Fő ciklus
        while not self.stop and not self.error:
            frame_index += 1
            if self.framethrottling and not self.mouse_active and skip_frames and frame_index % 2 != 0:
                cv2.waitKey(int(1000 / 30))
                continue

            ret, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if self.hueoffset != 0:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                img[:, :, 0] += self.hueoffset
                img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

            if cv2.waitKey(1) == 27:
                self.stop = True
            mp_image = Image(image_format=ImageFormat.SRGB, data=img)

            result = self.recognizer.recognize(mp_image)
            gesture_detected = False
            #region Távolságszámítás és időablakos detektálás
            if len(result.hand_landmarks) >= 1:
                distances = {}
                for i, landmarks in enumerate(result.hand_landmarks):
                    lm0 = landmarks[0]
                    lm9 = landmarks[9]
                    lm05 = landmarks[5]
                    lm17 = landmarks[17]
                    distance_09 = ((lm0.x - lm9.x) ** 2 + (lm0.y - lm9.y) ** 2) ** 0.5
                    distance_09 = 500 - int(distance_09 * 1000)

                    distance_517 = ((lm05.x - lm17.x) ** 2 + (lm05.y - lm17.y) ** 2) ** 0.5
                    distance_517 = 460 - int(distance_517 * 1000)

                    distances[i] = (distance_09, distance_517)

                closest_hand = min(distances, key=lambda x: sum(distances[x]))

                if (
                    self.mouse_active
                    and len(last_gestures) > 0
                    and last_gestures[-1][0] != mouse_gesture
                    and distances[closest_hand][0] <= self.distance
                ):
                    self.mouse_processor.process(result.hand_landmarks[closest_hand])

                if len(result.gestures) >= 1:
                    gesture = result.gestures[closest_hand]
                    name = gesture[0].category_name
                    score = gesture[0].score
                    if name != 'NONE' and name != '':
                        if score > (self.confidence - 0.2):
                            if (distances[closest_hand][0] <= self.distance or
                                    distances[closest_hand][1] <= self.distance):
                                last_gestures.append((name, score))
                                gesture_detected = True
                                #print(f"Gesture: {name}, Score: {score:.2f}, Distance: {distance_09}, 5-17 Distance: {distance_517}")
                        else:
                            last_gestures.append(("NONE", 0.0))
                    else:
                        last_gestures.append(("NONE", 0.0))
                else:
                    last_gestures.append(("NONE", 0.0))
            #endregion

            #region Majority voting
            if len(last_gestures) >= self.framecount:
                counts = Counter([g[0] for g in last_gestures])
                majority_gesture, majority_count = counts.most_common(1)[0]

                if (majority_count / self.framecount) >= 0.6 and majority_gesture != 'NONE':
                    majority_confidences = [g[1] for g in last_gestures if g[0] == majority_gesture]
                    avg_confidence = sum(majority_confidences) / len(majority_confidences)

            #endregion

            #region Parancsvégrehajtás
                    if avg_confidence >= self.confidence and (datetime.now() - last_gesture_time).total_seconds() > self.delay:
                        print(majority_gesture)
                        if majority_gesture in gesture_mappings.keys():
                            print(majority_gesture)
                            try:
                                if self.mouse_active and gesture_mappings[majority_gesture]['action'] == 'self.toggleMouseMode()':
                                    self.toggleMouseMode()
                                elif not self.mouse_active:
                                    exec(gesture_mappings[majority_gesture]['action'])
                            except Exception as e:
                                print("Hiba történt a parancs végrehajtásakor: ", e)
                            print(f"last_gesture: {majority_gesture}, avg confidence: {avg_confidence:.2f}")
                        last_gesture_time = datetime.now()

                last_gestures.clear()
            #endregion           

            #region FrameThrottling
            if self.framethrottling:
                if gesture_detected:
                    no_gesture_count = 0
                    skip_frames = False
                else:
                    no_gesture_count += 1
                    if no_gesture_count >= 3:
                        skip_frames = True
            #endregion

            if self.camerafeed:
                annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), result)
                annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                cv2.imshow('Annotated Image', annotated_image)

        #endregion


        cv2.destroyAllWindows()
    #region Egér mód
    def toggleMouseMode(self):
        if self.mouse_active:
            self.mouse_active = False
            self.framethrottling = self.framethrottling_prevstate
            self.mouse_processor.hideOverlay()
        else:
            self.mouse_active = True
            self.framethrottling_prevstate = self.framethrottling
            self.framethrottling = False
            self.mouse_processor.init_state = True
            self.mouse_processor.overlay_circle.setCircleOnly(False)
            self.mouse_processor.showOverlay()
    #endregion

#endregion

if __name__ == '__main__':
    taskFile = "gesture_recognizer.task"
    recognizer = Recognizer("gesture_recognizer.task", "Config/Gestures.json")

    recognizer.confidence = 0.6
    recognizer.camera = 0
    recognizer.camerafeed = True
    recognizer.Run()
