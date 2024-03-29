from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from music import Ui_MusicApp
from PyQt5.QtCore import Qt
import os.path
import songs
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


import random
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, QTimer




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
        self.play_btn.clicked.connect(self.play_song())

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

    #play song
    def play_song(self):
        try:
            current_selection = self.loaded_songs_listWidget.currentRow()
            current_song = songs.current_song_list[current_selection]

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
        except Exception as e:
            print(f"play song error {e}")