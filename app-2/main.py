from PyQt5.QtWidgets import *
from music import Ui_MusicApp
from PyQt5.QtCore import Qt


class ModernMusicPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUI(self)


        #remove default time bar
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.SetWindowFlags(Qt.FrameLessWindowHint)


        #Intial position of the window
        self.initialPosition = self.pos()

        def moveApp(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.initialPosition)
                self.initialPosition = event.globalPos()
                event.accept()

        self.title_frame.mouseMoveEvent = moveApp

        self.show()