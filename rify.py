import os
import shutil 
import yt_dlp
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3 
from pathlib import Path 

from scanning import scan_music
from player import Player 
songs = scan_music() 
player = Player() 






import uuid 
unique = str(uuid.uuid4()) 
folder =  Path.home() / "Music" / "Artists"
os.makedirs(folder, exist_ok=True)

def download_audio(url):
    file_container = {"path": None}

    def hook(d):
        if d["status"] == "finished":
            file_container["path"] = d["filename"]

    ydl_opts = {
        'format': 'bestaudio/best',
       'outtmpl': str(folder / '%(artist)s/%(album)s/%(track_number)s - %(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return file_container["path"], info 
def get_audio_metadata(info):
    
    return {
        'title': info.get('title') ,
        'artist': info.get('uploader') or info.get( 'artist') or "Unknown Artist",
        'album': info.get('album') or info.get ('playlist_title') or "Unknown Album",
        'genre': info.get('genre'),
        'date': info.get('date') or info.get('upload_date') or info.get('release_date') or "Unknown Date",
        'track': info.get('track') or info.get('track_number') or "Unknown Track",
    }
def organize_file(file_path, metadata):
    artist =  "".join(c for c in (metadata['artist'] or "Unknown") if c.isalnum() or c in " _-")
    artist_path = Path.home() / "Music" / "Artists" / artist 
    artist_path.mkdir(parents=True, exist_ok=True)

    new_path = artist_path / f"{unique}_{Path(file_path).name}" 

    shutil.move(file_path, new_path)

    return new_path 

def download_song(url):
    file_path, info = download_audio(url)

    metadata = get_audio_metadata(info)

    final_path = organize_file(
        file_path,
        metadata
    )

    return final_path 
current_index = 0
songs = []

def play_index(index):
     global current_index
     current_index = index
     player.play(songs[index]["path"]) 


def build_library(songs):
    library = {}

    for song in songs:
        path = Path(song["path"])

        artist = path.parent.parent.name
        album = path.parent.name

        library.setdefault(artist, {})
        library[artist].setdefault(album, [])

        library[artist][album].append(song)

    return library 





def get_songs():
    return scan_music()


def play_song(path):
    player.play(path) 