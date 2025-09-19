import ctypes

from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QWidget

class OverlayHandler(QWidget):
    _instance = None

    def __init__(self):
        
        super().__init__()
        self.index_finger_pos = QPoint(0, 0)
        self.circle_only = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        screen = QApplication.primaryScreen()
        size = screen.size()
        self.screen_width = size.width()
        self.screen_height = size.height()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setClickThrough()

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = OverlayHandler()

        return cls._instance

    def setClickThrough(widget):
        #Azért kell, hogy az átlátszó körön keresztül menjen a kattintás
        #Leírás: https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features
        hwnd = widget.winId()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE = -20
        style |= 0x20  # WS_EX_TRANSPARENT
        style |= 0x80000  # WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)

    def updatePosition(self, index_finger):
        fx = int(index_finger.x * self.screen_width)
        fy = int(index_finger.y * self.screen_height)
        self.index_finger_pos = QPoint(fx, fy)
        self.update()

    def setRadius(self, radius):
        self.radius = radius
        self.update()

    def setCircleOnly(self, circle_only):
        self.circle_only = circle_only
        self.update()

    def paintEvent(self, event):
        if not self.isVisible():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(80, 80, 80, 80), 40)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        painter.drawEllipse(center_x - self.radius, center_y - self.radius, self.radius * 2, self.radius * 2)

        if not self.circle_only:
            pen = QPen(QColor(100, 180, 255, 120), 15)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(self.index_finger_pos.x() - 30,
                                self.index_finger_pos.y() - 30,
                                60, 60)
