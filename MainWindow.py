#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QAction, QMessageBox, QListWidget, QSlider, QLabel,
                             QHBoxLayout, QVBoxLayout, QWidget, QSplitter)

from PlaylistCtrl import PlaylistControls


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Tranquility Music Player")
        self.setWindowIcon(QIcon('Images/music.ico'))
        self.setGeometry(300, 300, 500, 400)

        # Create the menubar
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        playlistMenu = mainMenu.addMenu('Playlist')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')

        openFile = QAction('Open File', self)
        createPlaylist = QAction('Create Playlist', self)
        savePlaylist = QAction('Save Playlist', self)
        toggleTheme = QAction('Toggle Black/White Theme', self)
        colorTheme = QAction('Toggle Red/ Purple Theme', self)
        about = QAction('About Tranquility MP', self)

        # Establish Context Menu actions
        self.playlistAdd = QAction('Add to Playlist', self)
        self.playlistDel = QAction('Remove from Playlist', self)
        self.delPlaylist = QAction('Delete Playlist', self)

        fileMenu.addAction(openFile)
        playlistMenu.addAction(createPlaylist)
        playlistMenu.addAction(savePlaylist)
        viewMenu.addAction(toggleTheme)
        viewMenu.addAction(colorTheme)
        helpMenu.addAction(about)

        openFile.triggered.connect(self.open_file)
        createPlaylist.triggered.connect(self.createPlaylist)
        savePlaylist.triggered.connect(self.savePlaylist)
        colorTheme.triggered.connect(self.toggleColor)
        toggleTheme.triggered.connect(self.toggleTheme)
        about.triggered.connect(self.about)
        self.playlistAdd.triggered.connect(self.open_file)
        self.playlistDel.triggered.connect(self.removeFromPlaylist)
        self.delPlaylist.triggered.connect(self.deletePlaylist)

        self.show()

    def establishLayout(self):
        cWid = QWidget()
        self.setCentralWidget(cWid)

        self.currentPlaylist = QListWidget()
        self.currentPlaylist.setFocusPolicy(Qt.NoFocus)
        self.currentPlaylist.itemDoubleClicked.connect(self.currentSelection)
        self.currentPlaylist.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.currentPlaylist.addAction(self.playlistAdd)
        self.currentPlaylist.addAction(self.playlistDel)

        self.playlistView = QListWidget()
        self.playlistView.adjustSize()
        self.playlistView.setMaximumWidth(100)
        self.playlistView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.playlistView.addAction(self.delPlaylist)
        self.playlistView.itemDoubleClicked.connect(self.parsePlaylist)

        self.seekSlider = QSlider(Qt.Horizontal)
        self.currentTimeLabel = QLabel('00:00')
        self.totalTimeLabel = QLabel('00:00')
        self.seekSlider.setRange(0, self.mediaPlayer.duration() / 1000)
        self.seekSlider.sliderMoved.connect(self.seek)
        self.seekSlider.valueChanged.connect(self.mediaPlayer.setPosition)

        # Set up splitter layout to hold the display widgets
        displaySplitter = QSplitter()
        displaySplitter.addWidget(self.playlistView)
        displaySplitter.addWidget(self.currentPlaylist)

        # Set up layout to hold the splitter layout
        displayLayout = QHBoxLayout()
        displayLayout.addWidget(displaySplitter)

        # Set up layout for Playlist Controls
        controls = PlaylistControls()
        controls.setState(self.mediaPlayer.state())
        controls.setVolume(self.mediaPlayer.volume())
        controls.setMuted(self.mediaPlayer.isMuted())
        controls.play.connect(self.mediaPlayer.play)
        controls.pause.connect(self.mediaPlayer.pause)
        controls.stop.connect(self.mediaPlayer.stop)
        controls.next.connect(self.playlist.next)
        controls.previous.connect(self.previousMedia)
        controls.changeVolume.connect(self.mediaPlayer.setVolume)
        controls.muteVolume.connect(self.mediaPlayer.setMuted)
        controls.shuffle.connect(self.playlist.shuffle)
        controls.repeatAll.connect(self.setRepeatAll)
        controls.repeatOne.connect(self.setRepeatOne)

        self.mediaPlayer.stateChanged.connect(controls.setState)
        self.mediaPlayer.volumeChanged.connect(controls.setVolume)
        self.mediaPlayer.mutedChanged.connect(controls.setMuted)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(controls)

        # Set up layout for Seek controls
        seekLayout = QHBoxLayout()
        seekLayout.addWidget(self.currentTimeLabel)
        seekLayout.addWidget(self.seekSlider)
        seekLayout.addWidget(self.totalTimeLabel)

        mainLayout = QVBoxLayout()
        layoutHelp(mainLayout, (displayLayout, seekLayout, controlLayout))
        mainLayout.setSpacing(0)

        self.setLayout(mainLayout)
        cWid.setLayout(mainLayout)

        if not self.mediaPlayer.isAvailable():
            QMessageBox.warning(self, "Service not available")

            controls.setEnabled(False)
            self.currentPlaylist.setEnabled(False)

        self.metaDataChanged()
        self.statusBar()

    def open_file(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open Files", "C:\\Users\\dchtk\\Music", 'All Files(*.*)')
        self.addToPlaylist(fileNames)

    def currentSelection(self):
        currentSelection = self.currentPlaylist.currentRow()
        self.playlist.setCurrentIndex(currentSelection)
        self.mediaPlayer.play()

    def removeFromPlaylist(self):
        selectedTrack = self.currentPlaylist.currentRow()
        self.playlist.setCurrentIndex(selectedTrack)
        self.currentPlaylist.takeItem(selectedTrack)
        self.playlist.removeMedia(selectedTrack)

    def deletePlaylist(self):
        selectedPlaylist = self.playlistView.currentRow()
        self.playlistView.takeItem(selectedPlaylist)

    def parsePlaylist(self, lines=None):
        path = "C:\\Users\dchtk\\Music\\Playlists"
        arr = os.listdir(path)
        for x in arr:
            xpath = os.path.join(path, x)
            if self.playlistView.selectedItems()[0].text() in xpath:
                item = xpath
                plFile = open(item, 'r')
                if plFile.mode == "r":
                    songs = plFile.read()
                    if self.currentPlaylist.count() > 0:
                        self.currentPlaylist.clear()
                        self.currentPlaylist.addItem(songs)
                    else:
                        self.currentPlaylist.addItem(songs)

    def about(self):
        QMessageBox.information(self, "About Tranquility MP", "Tranquility Media Player Version 1.0,\n\n"
                                                              "Developed by: D. Chaitkin")


def layoutHelp(containers, container_list):
    for container in container_list:
        containers.addLayout(container)
