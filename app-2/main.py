from PyQt5.QtWidgets import *
from music import Ui_MusicApp


class ModernMusicPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUI(self)

        self.show()