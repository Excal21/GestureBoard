from time import sleep
import cv2
import os

# Kamera inicializálása
url = 'http://192.168.1.12:8080/video'
cap = cv2.VideoCapture(0)

width = 250
height = 250

img_counter = 0

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


    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         print('Nem sikerült képet rögzíteni a kamerából')
    #         break

    #     # Kép közepének kivágása (320x240 pixel)
    #     y, x, _ = frame.shape
    #     start_x = x // 2 - 160
    #     start_y = y // 2 - 120
    #     end_x = start_x + width
    #     end_y = start_y + height
    #     cropped_frame = frame[start_y:end_y, start_x:end_x]

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
        
    #     #cv2.imshow('Kamera', cropped_frame)
    #     gesture_dir = os.path.join('Samples', gestrue_name)
    #     if not os.path.exists(gesture_dir):
    #         os.makedirs(gesture_dir)

    #     if cv2.waitKey(1) & 0xFF == ord('g'):
    #         for i in range(imgcnt):
    #             img_name = os.path.join(gesture_dir, f'{gestrue_name}_{img_counter}.png')
    #             cv2.imwrite(img_name, cropped_frame)
    #             img_counter += 1
    #             sleep(0.02)
    #         break

def guide():
    print('Írd be az új gesztus azonosítóját (Angol nagybetűk szóköz nélkül, lehet benne szám): ', end='')
    gestrue_name = input()
    print('Tartsd a kezed a kamera előtt olyan pozícióban, amivel vezérelni szeretnéd a számítógépet!')
    print('Másik kezeddel nyomd meg az enter billentyűt és kövesd az utasításokat!')
    input()

    record_batch(gestrue_name, 20)

    print('Most tartsd a kezed ugyanilyen pozícióban, de kicsit fordítsd el! Másik kezeddel nyomd meg az enter billentyűt!')
    input()
    
    record_batch(gestrue_name, 20)
    print('Gesztus rögzítése befejeződött!')
    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    escape = False
    while not escape:
        guide()
        print('Szeretnél még egy gesztust rögzíteni? (y/n): ', end='')
        if input() == 'n':
            escape = True

cap.release()