#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import QUrl, QFileInfo, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent, QMediaMetaData
from PyQt5.QtWidgets import (QApplication, QLineEdit, QInputDialog, QMainWindow)

from MainWindow import MainWindow


class TranquilityMP(QMainWindow, MainWindow):
    def __init__(self, playlist, parent=None):
        super(TranquilityMP, self).__init__(parent)
        self.statusInfo = ""
        self.trackInfo = ""
        self.theme = 0
        self.colorTheme = 0
        self.mediaPlayer = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)
        self.establishLayout()
        self.connectSignals()
        self.allPlaylists = self.loadPlaylists()
        self.toggleTheme()
        self.addToPlaylist(playlist)

    def connectSignals(self):
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.metaDataChanged.connect(self.metaDataChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.statusChanged)
        self.mediaPlayer.stateChanged.connect(self.stateChanged)

    def createPlaylist(self):
        root = QFileInfo(__file__).absolutePath()
        spot = (root + '/playlists/')
        playlistName = self.getText()
        completeName = os.path.join(spot, f'{playlistName}.m3u')
        file = open(completeName, 'w')
        file.close()
        self.playlistView.addItem(playlistName)
        self.allPlaylists = self.loadPlaylists()

    def savePlaylist(self):
        root = "C:\\Users\\dchtk\\Music\\Playlists"
        playlistName = self.getText()
        completeName = os.path.join(root, f'{playlistName}.m3u')
        file = open(completeName, 'a+')
        for i in range(self.currentPlaylist.count()):
            file.write(''.join([str(self.currentPlaylist.item(i).text()), '\n']))
        file.close()
        self.playlistView.addItem(playlistName)

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "New Playlist", "Playlist Name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

    def loadPlaylists(self):
        playlists = []
        root = "C:\\Users\\dchtk\\Music\\Playlists"
        songsPlaylist = os.listdir(root)
        for item in songsPlaylist:
            if str(item[-4:]) == '.m3u':
                self.playlistView.addItem(item[:-4])
                playlists.append(root + item)
        return playlists

    def addToPlaylist(self, fileNames):
        for name in fileNames:
            fileInfo = QFileInfo(name)
            songFileTitle = os.path.basename(name)
            if fileInfo.exists():
                url = QUrl.fromLocalFile(fileInfo.absoluteFilePath())
                if fileInfo.suffix().lower() == 'm3u':
                    self.playlist.load(url)
                else:
                    self.playlist.addMedia(QMediaContent(url))
                    self.currentPlaylist.addItem(songFileTitle)
            else:
                url = QUrl(name)
                if url.isValid():
                    self.playlist.addMedia(QMediaContent(url))
                    self.currentPlaylist.addItem(songFileTitle)

    def metaDataChanged(self):
        if self.mediaPlayer.isMetaDataAvailable():
            self.setTrackInfo("%s - %s" % (self.mediaPlayer.metaData(QMediaMetaData.AlbumArtist),
                                           self.mediaPlayer.metaData(QMediaMetaData.Title)))

    def previousMedia(self):
        if self.mediaPlayer.position() <= 5000:
            self.playlist.previous()
        else:
            self.playlist.setPosition(0)

    def setRepeatOne(self):
        if self.mediaPlayer.state == QMediaPlayer.PlayingState:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

    def setRepeatAll(self):
        if self.mediaPlayer.state == QMediaPlayer.PlayingState:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    def durationChanged(self, duration):
        self.duration = duration
        self.seekSlider.setMaximum(duration)
        if duration > 0:
            self.totalTimeLabel.setText(configureTime(self.duration))

    def positionChanged(self, position):
        if not self.seekSlider.isSliderDown():
            self.seekSlider.setValue(position)
        if position > 0:
            self.currentTimeLabel.setText(configureTime(position))

    def seek(self, seconds):
        if self.mediaPlayer.isSeekable():
            self.mediaPlayer.setPosition(seconds)

    def stateChanged(self):
        if self.mediaPlayer.state == QMediaPlayer.StoppedState:
            self.mediaPlayer.stop()

    def statusChanged(self, status):
        self.handleCursor(status)

        if status == QMediaPlayer.LoadingMedia:
            self.setStatusInfo("Loading")
        elif status == QMediaPlayer.LoadedMedia:
            self.setStatusInfo("Loaded")
            self.mediaPlayer.play()
        elif status == QMediaPlayer.BufferingMedia:
            self.setStatusInfo("Buffering")
        elif status == QMediaPlayer.EndOfMedia:
            QApplication.alert(self)
        elif status == (QMediaPlayer.InvalidMedia or QMediaPlayer.NoMedia):
            self.displayError()
        else:
            self.setStatusInfo("")

    def handleCursor(self, status):
        if status == QMediaPlayer.LoadingMedia:
            self.setCursor(Qt.BusyCursor)
        else:
            self.unsetCursor()

    def setTrackInfo(self, info):
        self.trackInfo = info

        if self.statusInfo != "":
            self.statusBar().showMessage("%s | %s" % (self.trackInfo, self.statusInfo))
        else:
            self.statusBar().showMessage(self.trackInfo)

    def setStatusInfo(self, info):
        self.statusInfo = info

        if self.statusInfo != "":
            self.statusBar().showMessage("%s | %s" % (self.trackInfo, self.statusInfo))
        else:
            self.statusBar().showMessage(self.trackInfo)

    def displayError(self):
        self.setStatusInfo(self.mediaPlayer.errorString())

    def toggleTheme(self):
        """ Fusion dark palette from https://gist.github.com/QuantumCD/6245215. Modified by D.C """
        app.setStyle("Fusion")
        palette = QPalette()
        if self.theme == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.theme = 1
        elif self.theme == 1:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.theme = 0

    def toggleColor(self):
        app.setStyle("Fusion")
        palette = QPalette()
        if self.colorTheme == 0:
            palette.setColor(QPalette.Window, QColor(178, 34, 34))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(128, 0, 0))
            palette.setColor(QPalette.AlternateBase, QColor(178, 34, 34))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(178, 34, 34))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.colorTheme = 1
        elif self.colorTheme == 1:
            palette.setColor(QPalette.Window, QColor(72, 61, 139))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(75, 0, 130))
            palette.setColor(QPalette.AlternateBase, QColor(72, 61, 139))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(72, 61, 139))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(53, 53, 53))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            app.setPalette(palette)
            self.colorTheme = 0


def configureTime(ms):
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%02d:%02d" % (m, s))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = TranquilityMP(sys.argv[1:])
    player.show()
    sys.exit(app.exec_())

