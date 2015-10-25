import spotipy

def song_lookup(name=None, artist=None, limit=1):
    sp = spotipy.Spotify()
    results = sp.search(q='track:' + name, 
        type='track', 
        limit=limit)
    
    if len(results['tracks']['items']) == 0:
        print("No results found for " + name)
        return

    songs = {}
    artists = results['tracks']['items'][0]['artists']
    artist_names = []
    for index, names in enumerate(artists):
        artist_names.append(names['name'])
    songs['artists'] = artist_names
    songs['trackid'] = results['tracks']['items'][0]['id']
    songs['track'] = results['tracks']['items'][0]['name']
    print("Results for " + songs['track'] + ' by ' + songs['artists'][0])
    return songs

song_lookup('Diamonds From Sierra Leone - Remix - Album Version (Explicit)')
song_lookup('asdlkajsdlkajslaksjdlaksjdalksjdalksjd')