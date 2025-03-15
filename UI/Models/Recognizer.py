# A projekt a Google MediaPipe moduljára és a hozzá tartozó példakódok egyes elemeire épül.
# Bővebb információ Google MediaPiperól az alábbi linken érhető el:
# https://ai.google.dev/edge/mediapipe 

import os
import sys
import cv2
from mediapipe import solutions, Image, ImageFormat
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
import numpy as np
from datetime import datetime
import shutil
import pyautogui
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Config")))

class Recognizer:
  def __init__(self, task_file_path: str, config_path: str):
      self.MARGIN = 10  # pixels
      self.FONT_SIZE = 1
      self.FONT_THICKNESS = 1
      self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green
      self.__task_file_path = task_file_path

      self.mp_hands = solutions.hands
      self.mp_drawing = solutions.drawing_utils
      self.mp_drawing_styles = solutions.drawing_styles


      #Modelfájl betöltése és beállítása
      self.model_file = open(self.__task_file_path, "rb")
      self.model_data = self.model_file.read()
      self.model_file.close()
      self.base_options = python.BaseOptions(model_asset_buffer=self.model_data)

      self.options = python.vision.GestureRecognizerOptions(
          base_options=self.base_options,
          min_tracking_confidence=0.7,
          
          num_hands=4
          )
      self.recognizer = python.vision.GestureRecognizer.create_from_options(self.options)

      self.__camera = 0
      self.__confidence = 0.5
      self.__stop = False
      self.__commands = {}
      self.__camerafeed = True
      self.__framecount = 5
      self.__hueoffset = 0
      self.__delay = 1
      self.__error = False
      self.__configpath = config_path

#region Getterek Setterek
  @property
  def framecount(self):
    return self.__framecount
  @framecount.setter
  def framecount(self, value):
    self.__framecount = value


  @property
  def camera(self):
    return self.__camera
  
  @camera.setter
  def camera(self, value):
    if type(value) is str:
      self.__camera = 'http://' + value + ':8080/video'
    else:
      self.__camera = value

  @property
  def labels(self):
    return self.__labels

  @property
  def labels_with_alias(self):
    return self.__labels_with_alias

  @property
  def commands(self):
    return self.__commands
  @commands.setter
  def commands(self, value):
    self.__commands = value

  @property
  def confidence(self):
    return self.__confidence
  @confidence.setter
  def confidence(self, value):
    self.__confidence = value/100

  @property
  def camerafeed(self):
    return self.__camerafeed
  @camerafeed.setter
  def camerafeed(self, value):
    self.__camerafeed = value

  @property
  def error(self):
    return self.__error
  @error.setter
  def error(self, value):
    self.__error = value

#endregion

  def reloadModel(self):
      self.model_file = open(self.__task_file_path, "rb")
      self.model_data = self.model_file.read()
      self.model_file.close()
      self.base_options = python.BaseOptions(model_asset_buffer=self.model_data)

      self.options = python.vision.GestureRecognizerOptions(
          base_options=self.base_options,
          min_tracking_confidence=0.7,
          
          num_hands=4
          )
      self.recognizer = python.vision.GestureRecognizer.create_from_options(self.options)



#region Vizualizáció
  def draw_landmarks_on_image(self, rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    for idx in range(len(hand_landmarks_list)):
      hand_landmarks = hand_landmarks_list[idx]
      handedness = handedness_list[idx]

      #Érzékelt pontok megrajzolása
      hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
      hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
      ])
      solutions.drawing_utils.draw_landmarks(
        annotated_image,
        hand_landmarks_proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_utils.DrawingSpec(color=(33, 43, 53), thickness=2, circle_radius=4),
        solutions.drawing_utils.DrawingSpec(color=(156, 220, 254), thickness=2))

      height, width, _ = annotated_image.shape
      x_coordinates = [landmark.x for landmark in hand_landmarks]
      y_coordinates = [landmark.y for landmark in hand_landmarks]
      text_x = int(min(x_coordinates) * width)
      text_y = int(min(y_coordinates) * height) - self.MARGIN

      # Draw handedness (left or right hand) on the image.
      # cv2.putText(annotated_image, f"{handedness[0].category_name}",
      #             (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
      #             self.FONT_SIZE, (0, 0, 0), self.FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image
#endregion


  def annotateImage(self, image):
    #img = cv2.flip(img, 1)
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_image = Image(image_format=ImageFormat.SRGB, data=img)

    result = self.recognizer.recognize(mp_image)
    annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), result)
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    return annotated_image


  def loadGestures(self):
    with open(self.__configpath, "r") as file:
      data = dict(json.load(file))
    return data

  def loadCameraSettings(self):
    with open('Config/CameraSettings.json', encoding='UTF-8') as f:
      data = dict(json.load(f))
      self.__camera = data['Camera']
      self.__framecount = data['FrameCount']
      self.__confidence = data['Confidence']
      self.__hueoffset = data['HueOffset']
      self.__delay = data['Delay']

  def Run(self):
    print('Recognizer started')
    self.loadCameraSettings()
    gesture_mappings = self.loadGestures()


    self.__stop = False
    cap = cv2.VideoCapture()  # Próbálj meg csatlakozni a megadott IP-címhez
    cap.setExceptionMode(True)

    try:
      if type(self.__camera) == int:
        cap.open(self.__camera, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FPS, 30)
      else:
        cap.open(self.__camera,  apiPreference=cv2.CAP_FFMPEG,
        params=[cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 500])
    except:
      self.__error = True
    

    last_gestures = []
    last_gesture_time = datetime.now()



    while not self.__stop and not self.__error: 
      #Beépített kamera
      ret, img = cap.read()
      #img = cv2.flip(img, 1)
      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
      
      if self.__hueoffset != 0:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[:, :, 0] += self.__hueoffset
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
      
      
      #Kilépés ESC gombra
      if cv2.waitKey(1) == 27: 
          self.__stop = True
      mp_image = Image(image_format=ImageFormat.SRGB, data=img)


      #Ha lát valamit a program, akkor adott konfidencia felett elkezdi halmozni listába
      result = self.recognizer.recognize(mp_image)
      if len(result.gestures) >= 1:
        for gesture in result.gestures:
            if gesture[0].category_name != 'NONE' and gesture[0].category_name != '':
              if gesture[0].score > self.confidence:
          #      print(f"{gesture[0].category_name} Confidence: {gesture[0].score:.2f}")
                last_gestures.append(gesture[0].category_name)



      #Ha a halmozás eredménye az, hogy self.__framecount db ugyanolyan gesztus van, akkor biztos, hogy valamit akar a user
      if len(last_gestures) >= self.__framecount:
        if all(gesture == last_gestures[0] for gesture in last_gestures) and (datetime.now() - last_gesture_time).total_seconds() > self.__delay and last_gestures[0]  != '':
          print(last_gestures[0])
          if last_gestures[0] in gesture_mappings.keys():
            print(last_gestures[0])
            exec(gesture_mappings[last_gestures[0]]['action'])
            print("last_gesture: {0}, confidence: {1:2f}".format(last_gestures[0], gesture[0].score))
          last_gesture_time = datetime.now()
        last_gestures.clear()

      if self.__camerafeed:
        annotated_image = self.draw_landmarks_on_image(mp_image.numpy_view(), result)

        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        cv2.imshow('Annotated Image', annotated_image)

    cv2.destroyAllWindows()

  def Stop(self):
    self.__stop = True


if __name__ == '__main__':
  taskFile = "gesture_recognizer.task"
  recognizer = Recognizer("gesture_recognizer.task")

  recognizer.confidence = 0.6
  recognizer.camera = 0
  recognizer.camerafeed = True
  recognizer.Run()


  