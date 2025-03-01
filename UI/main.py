import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from MainMenu import MainMenu
from OptionsMenu import OptionsMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureBoard")
        # self.setGeometry(100, 100, 800, 410)
        self.setFixedSize(800, 410)
        self.setStyleSheet("background-color: white;")  # Alap háttérszín

        # QStackedWidget létrehozása
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Nézetek létrehozása és hozzáadása
        self.main_menu = MainMenu(self.stacked_widget)
        self.options_menu = OptionsMenu(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.options_menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    

    window = MainWindow()
    window.show()
    sys.exit(app.exec())