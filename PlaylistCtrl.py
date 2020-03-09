from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData, QMediaPlaylist
from PyQt5.QtWidgets import QHBoxLayout, QToolButton, QSlider, QWidget, QSpacerItem
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon


class PlaylistControls(QWidget):
    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    next = pyqtSignal()
    previous = pyqtSignal()
    changeVolume = pyqtSignal(int)
    muteVolume = pyqtSignal(bool)
    shuffle = pyqtSignal()
    repeatAll = pyqtSignal()
    repeatOne = pyqtSignal()

    def __init__(self, parent=None):
        super(PlaylistControls, self).__init__(parent)

        # Set the initial state of the player
        # Set initial state of player mute status
        self.playerState = QMediaPlayer.StoppedState
        self.playerMuted = False

        # Establish the Playlist Ctrl Buttons
        self.playButton = QToolButton(clicked=self.playPause)
        self.playButton.setIcon(QIcon('Images/001-play.png'))
        self.playButton.setFixedSize(32, 32)
        self.playButton.setIconSize(QSize(32, 32))

        self.stopButton = QToolButton(clicked=self.stop)
        self.stopButton.setIcon(QIcon('Images/002-stop.png'))

        self.nextButton = QToolButton(clicked=self.next)
        self.nextButton.setIcon(QIcon('Images/005-forward.png'))
        self.nextButton.setFixedSize(24, 24)
        self.nextButton.setIconSize(QSize(24, 24))

        self.previousButton = QToolButton(clicked=self.previous)
        self.previousButton.setIcon(QIcon('Images/004-rewind.png'))
        self.previousButton.setFixedSize(24, 24)
        self.previousButton.setIconSize(QSize(24, 24))

        self.muteButton = QToolButton(clicked=self.muteMedia)
        self.muteButton.setIcon(QIcon('Images/002-speaker.png'))

        self.shuffleButton = QToolButton(clicked=self.shuffleMedia)
        self.shuffleButton.setIcon(QIcon('Images/001-change.png'))

        self.repeatAllButton = QToolButton(clicked=self.repeatAllMedia)
        self.repeatAllButton.setIcon(QIcon('Images/media-repeat(all).png'))

        self.repeatOneButton = QToolButton(clicked=self.repeatOneMedia)
        self.repeatOneButton.setIcon(QIcon('Images/media-repeat(1).png'))

        self.volumeSlider = QSlider(Qt.Horizontal, sliderMoved=self.changeVolume)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(45)

        # Setup Layout from Playlist Ctrls
        PlaylistCtrl = QHBoxLayout()
        helpAdd(PlaylistCtrl, (self.shuffleButton, self.repeatAllButton, self.repeatOneButton, self.stopButton, self.previousButton,
                               self.playButton, self.nextButton, self.muteButton, self.volumeSlider))
        PlaylistCtrl.insertSpacing(3, 4)
        PlaylistCtrl.insertSpacing(8, 5)

        self.setLayout(PlaylistCtrl)

    def state(self):
        return self.playerState

    def setState(self, state):
        if state != self.playerState:
            self.playerState = state

            if state == QMediaPlayer.StoppedState:
                self.stopButton.setEnabled(False)
                self.playButton.setIcon(QIcon('Images/001-play.png'))
            elif state == QMediaPlayer.PlayingState:
                self.stopButton.setEnabled(True)
                self.playButton.setIcon(QIcon('Images/003-pause.png'))
            elif state == QMediaPlayer.PausedState:
                self.stopButton.setEnabled(True)
                self.playButton.setIcon(QIcon('Images/001-play.png'))

    def volume(self):
        return self.volumeSlider.value()

    def setVolume(self, volume):
        self.volumeSlider.setValue(volume)

    def isMuted(self):
        return self.playerMuted

    def setMuted(self, muted):
        if muted != self.playerMuted:
            self.playerMuted = muted

            if muted:
                self.muteButton.setIcon(QIcon('Images/001-mute.png'))
                self.volumeSlider.setValue(0)
            else:
                self.muteButton.setIcon(QIcon('Images/002-speaker.png'))
                self.volumeSlider.setValue(45)

    def playPause(self):
        if self.playerState == QMediaPlayer.PlayingState:
            self.pause.emit()
        else:
            self.play.emit()

    def muteMedia(self):
        self.muteVolume.emit(not self.playerMuted)

    def shuffleMedia(self):
        self.shuffle.emit()

    def repeatAllMedia(self):
        self.repeatAll.emit()

    def repeatOneMedia(self):
        self.repeatOne.emit()


def helpAdd(container, widget_list):
    for widget in widget_list:
        container.addWidget(widget)
