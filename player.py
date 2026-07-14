import mpv

class Player:
    def __init__(self):
        self.player = mpv.MPV()
        self.current_song = None

    def play(self, path):
        self.current_song = path
        self.player.play(path)

    def pause(self):
        self.player.pause=not self.player.pause 

    def stop(self):
        self.player.stop() 