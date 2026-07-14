import locale

locale.setlocale(locale.LC_NUMERIC, "C") 


import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLineEdit,
    QListWidget,
)
from PySide6.QtCore import Qt, QTimer

from rify import get_songs, download_song, build_library
from player import Player


class RifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rify")
        self.resize(700, 500)

        self.player = Player()

        self.updating_seek = False
        self.dragging = False

        self.songs = get_songs()
        print("Songs found:", len(self.songs))

        self.library = build_library(self.songs)

        root = QWidget()
        self.setCentralWidget(root)

        self.layout = QVBoxLayout(root)


        # Seek bar
        self.seek = QSlider(Qt.Horizontal)
        self.seek.setRange(0, 100)
        self.seek.sliderPressed.connect(
            self.drag_begin
        )
        self.seek.sliderReleased.connect(
            self.drag_end
        )
        self.seek.valueChanged.connect(
            self.on_seek
        )

        self.layout.addWidget(self.seek)


        # Controls
        self.play_button = QPushButton("▶ Play/Pause")
        self.stop_button = QPushButton("⏹ Stop")

        self.play_button.clicked.connect(
            self.toggle_pause
        )

        self.stop_button.clicked.connect(
            self.stop_song
        )

        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.stop_button)


        # Download
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText(
            "Paste music URL..."
        )

        self.download_button = QPushButton(
            "Download"
        )

        self.download_button.clicked.connect(
            self.download_clicked
        )

        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.download_button)


        # Library
        library_box = QHBoxLayout()

        self.artist_list = QListWidget()
        self.album_list = QListWidget()
        self.song_list = QListWidget()

        library_box.addWidget(
            self.artist_list
        )

        library_box.addWidget(
            self.album_list
        )

        library_box.addWidget(
            self.song_list
        )

        self.layout.addLayout(library_box)


        self.populate_artists()


        self.artist_list.itemClicked.connect(
            self.artist_selected 
        )

        self.album_list.itemClicked.connect(
            self.album_selected
        )

        self.song_list.itemActivated.connect(
            self.play_selected
        )


        # Update seek position
        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_seek
        )
        self.timer.start(500)


    def drag_begin(self):
        self.dragging = True


    def drag_end(self):
        self.dragging = False


    def on_seek(self):
        if not self.updating_seek:
            self.player.player.time_pos = (
                self.seek.value()
            )


    def update_seek(self):

        if self.dragging:
            return

        duration = self.player.player.duration
        position = self.player.player.time_pos

        if duration:
            self.seek.setMaximum(
                int(duration)
            )

        if position:
            self.updating_seek = True
            self.seek.setValue(
                int(position)
            )
            self.updating_seek = False


    def populate_artists(self):

        self.artist_list.clear()

        for artist in self.library:
            self.artist_list.addItem(
                artist
            )


    def download_clicked(self):

        url = self.url_entry.text()

        if url:
            download_song(url)

            self.songs = get_songs()
            self.library = build_library(
                self.songs
            )

            self.populate_artists()


    def artist_selected(self, item):

        self.selected_artist = (
            item.text()
        )

        self.album_list.clear()
        self.song_list.clear()

        for album in self.library[
            self.selected_artist
        ]:
            self.album_list.addItem(
                album
            )


    def album_selected(self, item):

        self.selected_album = (
            item.text()
        )

        self.song_list.clear()

        self.current_songs = (
            self.library[
                self.selected_artist
            ][
                self.selected_album
            ]
        )

        for song in self.current_songs:
            self.song_list.addItem(
                song["title"]
            )


    def play_selected(self, item):

        index = (
            self.song_list.row(item)
        )

        song = self.current_songs[index]

        self.player.play(
            song["path"]
        )


    def toggle_pause(self):
        self.player.pause()


    def stop_song(self):
        self.player.stop()



app = QApplication(sys.argv)

window = RifyWindow()
window.show()

sys.exit(
    app.exec()
) 