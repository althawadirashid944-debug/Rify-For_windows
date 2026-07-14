from pathlib import Path

def scan_music():
    music_folder = Path.home() / "Music" / "Artists"

    songs = []

    for file in music_folder.rglob("*.mp3"):
        songs.append({
            "title": file.stem,
            "path": str(file)
        })

    return songs 