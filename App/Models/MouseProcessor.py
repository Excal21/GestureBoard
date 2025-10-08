import math
import sys
from pynput.mouse import Controller, Button

from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QWidget
from Models.OverlayHandler import OverlayHandler


#region Egérvezérlő
class MouseProcessor:
    def __init__(self, radius=250, sensitivity=15, y_offset=-200):
        self.radius = radius
        self.sensitivity = sensitivity
        self.y_offset = y_offset
        self.invert = False
        self.mouse = Controller()
        self.last_click_time = datetime.min
    
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

        screen = self.app.primaryScreen()
        size = screen.size()
        self.screen_width = size.width()
        self.screen_height = size.height()

        self.init_state = True

        self.prev_screen_x, self.prev_screen_y = None, None
        self.overlay_circle = OverlayHandler.getInstance()
        self.overlay_circle.setOffsetY(self.y_offset)


    def hideOverlay(self):
        self.overlay_circle.hide()

    def showOverlay(self):
        self.overlay_circle.show()
        self.initangles = None

    def calcAngle(self, v1, v2):
        product = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

        len1 = math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
        len2 = math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)

        cos_theta = product / (len1 * len2)
        cos_theta = max(min(cos_theta, 1.0), -1.0)  # float hülyeségek miatt

        angle = math.degrees(math.acos(cos_theta))
        return angle

    def process(self, hand_landmarks):
        lm08 = hand_landmarks[8]

        lm00 = hand_landmarks[0]

        lm01 = hand_landmarks[1] #Hüvelykujj alja
        lm03 = hand_landmarks[3] #Hüvelykujj közepe

        lm05 = hand_landmarks[5]
        lm17 = hand_landmarks[17]

        lm09 = hand_landmarks[9] #Középső ujj töve

        lm012 = hand_landmarks[12] #Középső ujj vége
        lm010 = hand_landmarks[10] #Középső ujj alsó része

        v1 = (lm09.x - lm00.x, lm09.y - lm00.y, lm09.z - lm00.z)
        v2 = (lm012.x - lm010.x, lm012.y - lm010.y, lm012.z - lm010.z)
        
        v3 = (lm03.x - lm01.x, lm03.y - lm01.y, lm03.z - lm01.z)
        v4 = (lm05.x - lm17.x, lm05.y - lm17.y, lm05.z - lm17.z)

        angle1 = self.calcAngle(v1, v2)
        angle2 = self.calcAngle(v3, v4)

        if self.init_state:
            if angle1 < 20 and angle2 < 50:
                self.init_state = False
            else:
                print('Szögek: ', angle1, angle2)
                return


        now = datetime.now()
        #Mutatóujj
        if angle1 > 45:
            if now - self.last_click_time > timedelta(seconds=0.4):
                self.mouse.press(Button.left if self.invert else Button.right)
                self.mouse.release(Button.left if self.invert else Button.right)
                self.last_click_time = now
            return
      
        #Hüvelykujj
        if angle2 > 70:
            if now - self.last_click_time > timedelta(seconds=0.4):
                self.mouse.press(Button.right if self.invert else Button.left)
                self.mouse.release(Button.right if self.invert else Button.left)
                self.last_click_time = now
            return

    #region EMA simítás
        alpha = 0.2

        if not hasattr(self, "smooth_idx_x"):
            self.smooth_idx_x, self.smooth_idx_y = lm08.x, lm08.y
        else:
            self.smooth_idx_x = alpha * lm08.x + (1 - alpha) * self.smooth_idx_x
            self.smooth_idx_y = alpha * lm08.y + (1 - alpha) * self.smooth_idx_y

        lm08.x = 1 - self.smooth_idx_x   # tükörflip
        lm08.y = self.smooth_idx_y

        screen_x = int(lm08.x * self.screen_width)
        screen_y = int(lm08.y * self.screen_height)

    #endregion

        self.overlay_circle.updatePosition(lm08)

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2 - self.y_offset
        dist = math.hypot(screen_x - center_x, screen_y - center_y)

        if dist <= self.radius:
            if self.prev_screen_x is not None and self.prev_screen_y is not None:
                dx = screen_x - self.prev_screen_x
                dy = screen_y - self.prev_screen_y

                screen_dx = int((dx / self.screen_width) * self.screen_width)
                screen_dy = int((dy / self.screen_height) * self.screen_height)

                self.mouse.move(screen_dx, screen_dy)

            self.prev_screen_x, self.prev_screen_y = screen_x, screen_y
        else:
            dx = screen_x - center_x
            dy = screen_y - center_y

            move_x = int((dx / self.radius) * self.sensitivity)
            move_y = int((dy / self.radius) * self.sensitivity)

            self.mouse.move(move_x, move_y)
            self.prev_screen_x, self.prev_screen_y = None, None

#endregion