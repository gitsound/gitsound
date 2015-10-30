# coding=utf-8
from __future__ import unicode_literals, print_function
import gitSound
import sys
import json
import os

if __name__ == "__main__":

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        askText = "please enter your spotify username: "
        try:  # python 2.7
            username = raw_input(askText)
        except:  # python 3.x
            username = input(askText)

    if os.path.isfile("gitSound_config.txt") == False:
        raise RuntimeError(
            "cannot find gitSound_config.txt in the working directory")

    with open("gitSound_config.txt") as configFile:
        configVars = json.loads(configFile.read())

    newUser = gitSound.spotifyUser(
        username, configVars["client_id"], configVars["client_secret"],
        "http://localhost/callback")

    playListIds = newUser.getPlaylistIDs()

    # Init playlist
    newUser.initGitPlaylist(playListIds[6])

    # add songs, commit
    newUser.addSongToPlaylist(playListIds[6], "pop")
    newUser.addSongToPlaylist(playListIds[6], "dog")
    newUser.commitChangesToPlaylist(playListIds[6], newUser.getTree())

    # remove songs, commit
    newUser.removeSongFromPlaylist(playListIds[6], "pop")
    newUser.removeSongFromPlaylist(playListIds[6], "dog")
    newUser.commitChangesToPlaylist(playListIds[6], newUser.getTree())

    # look up songs
    newUser.songLookup('Diamonds From Sierra Leone - Remix - Album Version (Explicit)')
    newUser.songLookup('asdlfjsdlkfjsldkfjsdlkfjlskdjf')
