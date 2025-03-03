from time import sleep
import cv2
import os
import json

# Kamera inicializálása
url = 'http://192.168.1.12:8080/video'
cap = cv2.VideoCapture(0)

width = 500
height = 500

img_counter = 0

def loadSettings():
    with open('UserSettings.json', encoding='UTF-8') as f:
        data = json.load(f)
    return data

def record_batch(gesture_name, imgcnt):
    global img_counter
    gestrue_name = gesture_name

    gesture_dir = os.path.join('Samples', gestrue_name)
    if not os.path.exists(gesture_dir):
        os.makedirs(gesture_dir)

    for i in range(imgcnt):
        # Kép közepének kivágása (320x240 pixel)
        ret, frame = cap.read()
        y, x, _ = frame.shape
        start_x = x // 2 - 160
        start_y = y // 2 - 120
        end_x = start_x + width
        end_y = start_y + height
        cropped_frame = frame[start_y:end_y, start_x:end_x]

        img_name = os.path.join(gesture_dir, f'{gestrue_name}_{img_counter}.png')
        cv2.imwrite(img_name, cropped_frame)
        img_counter += 1
        sleep(0.02)



def guide():
    data = loadSettings()
    gesture_id = len(data)
    gesture_name = None

    print('Írd be a gesztus nevét: ', end='')
    gesture_name = input()
    print('Tartsd a kezed a kamera előtt olyan pozícióban, amivel vezérelni szeretnéd a számítógépet!')
    print('Másik kezeddel nyomd meg az enter billentyűt és kövesd az utasításokat!')
    input()

    record_batch(gesture_name, 20)

    print('Most tartsd a kezed ugyanilyen pozícióban, de kicsit fordítsd el! Másik kezeddel nyomd meg az enter billentyűt!')
    input()
    
    record_batch(gesture_name, 20)
    print('Gesztus rögzítése befejeződött!')
    

    cv2.destroyAllWindows()

    gesture_entry = {gesture_id : {'gesture' : gesture_name, 'action' : None}}
    data.update(gesture_entry)
    with open('UserSettings.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    escape = False
    while not escape:
        guide()
        print('Szeretnél még egy gesztust rögzíteni? (y/n): ', end='')
        if input() == 'n':
            escape = True

cap.release()