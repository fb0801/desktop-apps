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

        #slider timer
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider())


        #connections
        #default page
        self.music_slider.sliderMoved[int].connect(
            lambda: self.player.setPosition(self.music_slider.value())
        )
        self.add_songs_btn.clicked.connect(self.add_songs)
        self.play_btn.clicked.connect(self.play_song())
        self.pause_btn.clicked.connect(self.pause_and_unpause)
        self.stop_btn.clicked.connect(self.stop_song)
        self.next_btn.clicked.connect(self.next_song)
        self.previous_btn.clicked.connect(self.previous_song)
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
                self.music_slider.SetValue(slider_position)

                #change time lbls
                current_time = time.strftime("%H:%M:%S", time.localtime(self.player.position() / 1000))
                song_duration = time.strftime("%H:%M:%S", time.localtime(self.player.duration() / 1000))
                self.time_label.setText(f"{current_time} / {song_duration}")
                


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

    def default_next(self):
        try:
            if self.stackedWidget.currentIndex() == 0:
                current_media = self.player.media()
                current_song_url = current_media.canonicalUrl().path()[1:]

                song_index = songs.current_song_list.index(current_song_url)
                if song_index + 1 == len(songs.current_song_list):
                    next_index = 0
                else:
                    next_index = song_index + 1
                next_song = songs.current_song_list[next_index]
                self.loaded_songs_listWidget.setCurrentRow(next_index)
            elif self.stackedWidget.currentIndex() == 2:
                current_media = self.player.media()
                current_song_url = current_media.canonicalUrl().path()[1:]

                song_index = songs.favourites_songs_list.index(current_song_url)
                if song_index + 1 == len(songs.favourites_songs_list):
                    next_index = 0
                else:
                    next_index = song_index + 1
                next_song = songs.favourites_songs_list[next_index]
                self.favourites_listWidget.setCurrentRow(next_index)

            song_url = QMediaContent(QUrl.fromLocalFile(next_song))
            self.player.setMedia(song_url)
            self.player.play()

            self.current_song_name.setText(f'{os.path.basename(next_song)}')
            self.current_song_path.setText(f'{os.path.dirname(next_song)}')
        except Exception as e:
            print(f"Default Next error: {e}")

    def looped_next(self):
        try:
            if self.stackedWidget.currentIndex() == 0:
                current_media = self.player.media()
                current_song_url = current_media.canonicalUrl().path()[1:]

                song_index = songs.current_song_list.index(current_song_url)

                song = songs.current_song_list[song_index]
            elif self.stackedWidget.currentIndex() == 2:
                current_media = self.player.media()
                current_song_url = current_media.canonicalUrl().path()[1:]

                song_index = songs.favourites_songs_list.index(current_song_url)

                song = songs.favourites_songs_list[song_index]
            song_url = QMediaContent(QUrl.fromLocalFile(song))
            self.player.setMedia(song_url)
            self.player.play()
            self.loaded_songs_listWidget.setCurrentRow(song_index)

            self.current_song_name.setText(f'{os.path.basename(song)}')
            self.current_song_path.setText(f'{os.path.dirname(song)}')
        except Exception as e:
            print(f"Looped Next: {e}")

    
    def shuffled_next(self):
        try:
            if self.stackedWidget.currentIndex() == 0:
                next_index = random.randint(0, len(songs.current_song_list))
                next_song = songs.current_song_list[next_index]
                self.loaded_songs_listWidget.setCurrentRow(next_index)
            elif self.stackedWidget.currentIndex() == 2:
                next_index = random.randint(0, len(songs.favourites_songs_list))
                next_song = songs.favourites_songs_list[next_index]
                self.favourites_listWidget.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(next_song))
            self.player.setMedia(song_url)
            self.player.play()

            self.current_song_name.setText(f'{os.path.basename(next_song)}')
            self.current_song_path.setText(f'{os.path.dirname(next_song)}')
        except Exception as e:
            print(f"Shuffled next error: {e}")

#next song
    def next_song(self):
        try:
            global looped
            global is_shuffled

            if is_shuffled:
                self.shuffled_next()
            elif looped:
                self.looped_next()
            else:
                self.default_next()

        except Exception as e:
            print(f"Next Song error: {e}")

    #prev song
    def previous_song(self):
        try:
            current_media = self.player.media()
            current_song_url = current_media.canonicalUrl().path()[1:]
            song_index = songs.current_song_list.index(current_song_url)
            previous_index = song_index - 1
            previous_song = songs.current_song_list[previous_index]
            song_url = QMediaContent(QUrl.fromLocalFile(previous_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.loaded_songs_listWidget.setCurrentRow(previous_index)

            self.current_song_name.setText(f'{os.path.basename(previous_song)}')
            self.current_song_path.setText(f'{os.path.dirname(previous_song)}')
        except Exception as e:
            print(f"Next song error: {e}")