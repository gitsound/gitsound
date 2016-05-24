#! /usr/bin/env python3

import util
import json
import os
import sys

from pygit2 import Repository
import gitsound

USAGE_MESSAGE = """
GitSound

Usage:
  cli.py <command> [<argument>] [--help]

Command List:
  show [local | remote]    Show all playlists locally or form spotify
  select <playlist_id>     Set the current playlist
  clone <playlist_id>      Clone a playlist from spotify
  add <track_id>           Add a track by id to the current playlist
  remove <track_id>        Remove a track by id from the current playlist
  search <track>  Search for id of song on spotify
  pull                     Pull changes from spotify into current playlist
  push                     Push changes from local playlist to spotify
  status                   See all changes to be committed
  commit                   Commit all changes
"""

if __name__ == '__main__':

    # Simplify references to args
    try:
        cmd = sys.argv[1]
    except:
        print(USAGE_MESSAGE)

    arg = None
    try:
        arg = sys.argv[2]
    except:
        pass

    config = util.load_config()

    user = gitsound.SpotifyUser(
        config["uid"], config["client_id"], config["client_secret"],
        config["redirect_uri"])

    uid = config["current_playlist"]["uid"]
    pid = config["current_playlist"]["pid"]
    pname = config["current_playlist"]["name"]

    # Determine how to handle args
    if cmd == 'show':
        if arg == 'local':
            playlists = []
            git_dir = ".activePlaylists/" + user.username + "/"
            pids = [pid for pid in os.listdir(git_dir)]
            # gets playlist ids from git directory
            for pid in pids:
                playlist = user.get_playlist_from_id(pid)['name']
                playlists.append(playlist)
            for index, playlist in enumerate(playlists):
                print(str(index) + " |   " + playlist)
        elif (arg == 'remote'):
            playlists = user.get_playlist_names()
            for index, playlist in enumerate(playlists):
                print(str(index) + " |   " + playlist)
        else:
            print('Not yet implemented.')
            print('Show all playlists, local and remote')
    elif cmd == 'select' and arg is not None:
        ids = user.get_playlist_id(arg)
        config["current_playlist"]["uid"] = ids["uid"]
        config["current_playlist"]["pid"] = ids["pid"]
        config["current_playlist"]["name"] = user.get_playlist_name(arg)

        util.save_config(config)

        print('Set current playlist to ' + config["current_playlist"]["name"])
    elif cmd == 'clone' and arg is not None:
        ids = user.get_playlist_id(arg)
        config["current_playlist"]["uid"] = ids["uid"]
        config["current_playlist"]["pid"] = ids["pid"]
        config["current_playlist"]["name"] = user.get_playlist_name(arg)

        util.save_config(config)

        try:
            user.init_git_playlist(ids["uid"], ids["pid"])
            print('Cloned playlist ' + config["current_playlist"]["name"])
        except:
            print(config["current_playlist"]["name"] + ' already cloned.')
    elif cmd == 'add' and arg is not None:
        if not pid:
            print('Select a playlist first')
        else:
            user.add_song_to_playlist(uid, pid, arg)
            print('Added track with id ' + arg + ' to ' + pname)
    elif cmd == 'remove' and arg is not None:
        if (not pid):
            print('Select a playlist first')
        else:
            user.remove_song_from_playlist(uid, pid, arg)
            print('Removed track with id ' + arg + ' from ' + pname)
    elif cmd == 'commit':
        user.commit_changes_to_playlist(uid, pid)
        print('Committed all changes to ' + pname)
    elif cmd == 'pull':
        print('On playlist ' + pname + ":")
        print(user.pull_spotify_playlist(uid, pid))
    elif cmd == "push":
        print("On playlist {0} :".format(pname))
        print(user.push_spotify_playlist(uid, pid))
    elif cmd == 'status':
        print('Not yet implemented.')
        print('Show changes to commit')
    elif cmd == 'search' and arg is not None:
        search = user.song_lookup(name=arg)
        print('Track: ' + search["track"])
        # for now only print first artist
        print('Artist: ' + search["artists"][0])
        print('Track ID: ' + search["trackid"])
    else:
        print(USAGE_MESSAGE)
