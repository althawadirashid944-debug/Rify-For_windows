from rapidfuzz import process

def search(query, songs):
    if not query:
        return songs

    choices = [
        f"{song['artist']} {song['title']}"
        for song in songs
    ]

    matches = process.extract(query, choices, limit=20)

    return [songs[index] for _, _, index in matches] 