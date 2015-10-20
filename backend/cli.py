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
  status                 See all changes to be committed
  commit                 Commit all changes
"""

from docopt import docopt

if __name__ == '__main__':
    # Initialize docopt and grab args
    args = docopt(__doc__)

    # Simplify references to args
    cmd = args['<command>']
    arg = args['<argument>']

    # Determine how to handle args
    if (cmd == 'show'):
        if (arg == 'local'):
            print('Show all local playlists')
        elif (arg == 'remote'):
            print('Show all remote playlists')
        else:
            print('Show all playlists, local and remote')
    elif (cmd == 'select' and arg != None):
        print('Select playlist with id ' + arg)
    elif (cmd == 'clone' and arg != None):
        print('Clone playlist with id ' + arg)
    elif (cmd == 'add' and arg != None):
        print('Add track with id ' + arg + ' to current playlist')
    elif (cmd == 'remove' and arg != None):
        print('Remove track with id ' + arg + ' from current playlist')
    elif (cmd == 'commit'):
        print('Commit all changes to current playlist')
    elif (cmd == 'status'):
        print('Show changes to commit')
    else:
        print('Usage: cli.py <command> [<argument>]')
