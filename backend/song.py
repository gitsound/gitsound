import spotipy

def song_lookup(name=None, artist=None, limit=1):
    sp = spotipy.Spotify()
    results = sp.search(q='track:' + name, 
    	type='track', 
    	limit=limit)
    return results

print(song_lookup('Diamonds From Sierra Leone - Remix - Album Version (Explicit)'))