#! /usr/bin/env python
"""
GitSound

Usage:
  cli.py show (local | remote) Show all playlists locally or form spotify
  cli.py select <playlist_id>  Set the current playlist
  cli.py clone <playlist_id>   Clone a playlist from spotify
  cli.py add <track_id>        Add a track by id to the current playlist
  cli.py remove <track_id>     Remove a track by id from the current playlist
  cli.py status                See all changes to be committed
  cli.py commit                Commit all changes

Options:
  -h --help                    Show this screen.
"""

from docopt import docopt

if __name__ == '__main__':

    args = docopt(__doc__, options_first=True)

    if (args['show']):
        if (args['local']):
            print('Show all local playlists')
        elif (args['remote']):
            print('Show all remote playlists')
    elif (args['select'] and args['<playlist_id>']):
        print('Select playlist with id ' + args['<playlist_id>'])
    elif (args['clone'] and args['<playlist_id>']):
        print('Clone playlist with id ' + args['<playlist_id>'])
    elif (args['add'] and args['<track_id>']):
        print('Add track with id ' + args['<track_id>'] + ' to current playlist')
    elif (args['remove'] and args['<track_id>']):
        print('Remove track with id ' + args['<track_id>'] + ' from current playlist')
    elif (args['commit']):
        print('Commit all changes to current playlist')
    elif (args['status']):
        print('Show changes to commit')
