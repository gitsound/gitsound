#! /usr/bin/env python
"""
GitSound

Usage:
  cli.py <command> [<argument>] [--help]

options:
  -h, --help             Show this message.

Command List:
  show [local | remote]  Show all playlists locally or form spotify
  select <playlist_id>   Set the current playlist
  clone <playlist_id>    Clone a playlist from spotify
  add <track_id>         Add a track by id to the current playlist
  remove <track_id>      Remove a track by id from the current playlist
  pull                   Pull changes from spotify into current playlist
  status                 See all changes to be committed
  commit                 Commit all changes
"""

from docopt import docopt
from pygit2 import Repository
import gitSound
import json
import os

if __name__ == '__main__':

    # Initialize docopt and grab args
    args = docopt(__doc__)

    # Simplify references to args
    cmd = args['<command>']
    arg = args['<argument>']

    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py to reconfigure.")

    with open("config.json") as configFile:
        try:
            config = json.loads(configFile.read())
        except:
            raise RuntimeError("Improperly formatted config.json. Run setup.py to reconfigure.")

    user = gitSound.spotifyUser(
        config["user_id"], config["client_id"], config["client_secret"],
        config["redirect_uri"])

    # Determine how to handle args
    if (cmd == 'show'):
        if (arg == 'local'):
            print('Not yet implemented.')
            print('Show all local playlists')
        elif (arg == 'remote'):
            playlists = user.getPlaylistNames()
            for index, playlist in enumerate(playlists):
                print(str(index) + " |   " + playlist)
        else:
            print('Not yet implemented.')
            print('Show all playlists, local and remote')
    elif (cmd == 'select' and arg != None):
        config["current_pid"] = user.getPlaylistId(arg)
        config["current_pid_name"] = user.getPlaylistName(arg)
        with open('config.json', 'w') as f:
            print(json.dumps(config, indent=4), file=f)

        print('Set current playlist to ' + config["current_pid_name"])
    elif (cmd == 'clone' and arg != None):
        config["current_pid"] = user.getPlaylistId(arg)
        config["current_pid_name"] = user.getPlaylistName(arg)
        with open('config.json', 'w') as f:
            print(json.dumps(config, indent=4), file=f)

        try:
            user.initGitPlaylist(config["current_pid"])
            print('Cloned playlist ' + config["current_pid_name"])
        except:
            print(config["current_pid_name"] + ' already cloned.')
    elif (cmd == 'add' and arg != None):
        if (not config["current_pid"]):
            print('Select a playlist first')
        else:
            user.addSongToPlaylist(config["current_pid"], arg)
            print('Added track with id ' + arg + ' to ' + config["current_pid_name"])
    elif (cmd == 'remove' and arg != None):
        if (not config["current_pid"]):
            print('Select a playlist first')
        else:
            user.removeSongFromPlaylist(config["current_pid"], arg)
            print('Removed track with id ' + arg + ' from ' + config["current_pid_name"])
    elif (cmd == 'commit'):
        user.commitChangesToPlaylist(config["current_pid"])
        print('Committed all changes to ' + config["current_pid_name"])
    elif (cmd == 'pull'):
        print('On playlist ' + config["current_pid_name"] + ":")
        print(user.pullSpotifyPlaylist(config["current_pid"]))
    elif (cmd == 'status'):
        print('Not yet implemented.')
        print('Show changes to commit')
    else:
        print('Usage: cli.py <command> [<argument>]')
