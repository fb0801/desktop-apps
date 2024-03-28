from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from music import Ui_MusicApp
from PyQt5.QtCore import Qt
import os.path
import songs

class ModernMusicPlayer(QMainWindow, Ui_MusicApp):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUI(self)


        #remove default time bar
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.SetWindowFlags(Qt.FrameLessWindowHint)

        #create player
        self.player = QMediaPlayer()
        


        #Intial position of the window
        self.initialPosition = self.pos()


        #connections
        #default page
        self.add_songs_btn.clicked.connect(self.add_songs)

        self.show()

        def moveApp(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.initialPosition)
                self.initialPosition = event.globalPos()
                event.accept()

        self.title_frame.mouseMoveEvent = moveApp


    # func to handle mouse pos
    def mousePressEvent(self, event):
        self.initialPosition = event.globalPos()

    # add songs
    def add_songs(self):
        files = QFileDialog.getOpenFileNames(
            self, caption='Add songs', directory=':\\',
            filter='supported files (mp3, mpeg, ogg, m4a, ,p3, wma, ac, amr)'
        )
        if files:
           for file in files:
               songs.current_song_list.append(file)
               self.loaded_songs_listWidget.addItem(
                   QListWidget(
                       QIcon(':/img/utils/images/MusicListItem.png'),
                       os.path.basename(file)

                   )
               )

