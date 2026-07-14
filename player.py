from pathlib import Path
import sys


import mpv

def get_resource_path(relative):
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent
    return base / relative
class Player:
    def __init__(self):
        mpv_exe = get_resource_path(
            Path("mpv") / "mpv.exe"
        ) 
        self.player = mpv.MPV(
            executables=str(mpv_exe)
        )
       

    def play(self, path):
        self.current_song = path
        self.player.play(path)

    def pause(self):
        self.player.pause=not self.player.pause 

    def stop(self):
        self.player.stop() 