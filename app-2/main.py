from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from music import Ui_MusicApp
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

        #globals
        global stopped 
        global looped 
        global is_shuffled 

        stopped = False
        looped = True
        is_shuffled = False

        #create player
        self.player = QMediaPlayer()
        self.initial_volume = 20
        self.player.setVolume(self.initial_volume)
        self.volume_dial.setValue(self.initial_volume)
        self.volume_label.setText(f"{self.initial_volume}")

        


        #Intial position of the window
        self.initialPosition = self.pos()


        #connections
        #default page
        self.add_songs_btn.clicked.connect(self.add_songs)
        self.play_btn.clicked.connect(self.play_song())
        self.pause_btn.clicked.connect(self.pause_and_unpause)
        self.stop_btn.clicked.connect(self.stop_song)
        self.volume_dial.valueChanged.connect(lambda: self.volume_changed())

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

    #move slider
    def move_slider(self):
        if stopped:
            return 
        else: 
            #update
            if self.player.state() == QMediaPlayer.PlayingState:
                self.music_slider.setMinimum(0)
                self.music_slider.setMaximum(self.player.duration())
                slider_position = self.player.position()

                print(f"Duration:{self.player.duration()}")
                print(f"Current: {slider_position}")


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

            self.current_song_name.setText(f'{os.path.basename(current_song)}')
            self.current_song_path.setText(f'{os.path.dirname(current_song)}')
        except Exception as e:
            print(f"play song error {e}")


    #pause song
    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

#stop song
    def stop_song(self):
        try:
            
            self.player.stop()
        except Exception as e:
            print(f"stop song error {e}")

#func to change volume
    def volume_changed(self):
        try:
            self.initial_volume = self.volume_dial.value()
            self.player.setVolume(self.initial_volume)

        except Exception as e:
            print(f"volume change error: {e}")