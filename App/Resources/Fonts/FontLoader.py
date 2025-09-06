from PySide6.QtGui import QFontDatabase, QFont

class FontLoader:
    _font_family = None

    @classmethod
    def loadFont(cls, path='Resources/Fonts/Ubuntu-R.ttf'):
        if cls._font_family is None:
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                cls._font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                print('Font beolvasva')
            else:
                print('Hiba: Nem sikerült betölteni az Ubuntu fontot!')
                cls._font_family = QFont().family()

    @classmethod
    def getFont(cls, size=12, path='Resources/Fonts/Ubuntu-R.ttf'):
        cls.loadFont(path)
        return QFont(cls._font_family, size)