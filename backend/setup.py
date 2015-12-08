#! /usr/bin/env python

"""File that sets up a user's system upon running command line.

Only need to run this file once when initally setting up GitSound.

.. note::
    User will need to obtain a client_id and client_secret from Spotify.

"""
from pygit2 import Repository
import gitsound
import login
import json
import os
import sys
import getpass

if __name__ == '__main__':
    if (os.path.isfile("config.json") == True):
        with open('config.json', 'r') as f:
            try:
                config = json.load(f)
            except:
                config = {}
    else:
        config = {}

    config["uid"] = input("spotify username: ")
    password = getpass.getpass('create a password:')

    logged_in = login.validate_user(config["uid"], password)
    if (logged_in == False):
        print('Incorrect username/password combination.')
        sys.exit(1)

    config["name"] = input("name: ")
    config["email"] = input("email: ")

    if ("client_id" not in config):
        config["client_id"] = input("client id: ")
    if ("client_secret" not in config):
        config["client_secret"] = input("client_secret: ")

    config["redirect_uri"] = "http://localhost/callback"

    user = gitsound.SpotifyUser(
        config["uid"], config["client_id"], config["client_secret"],
        config["redirect_uri"])

    ids = user.get_playlist_ids()[0]

    if not config.get('current_playlist'):
        config["current_playlist"] = {}
    config["current_playlist"]["uid"] = ids["uid"]
    config["current_playlist"]["pid"] = ids["pid"]
    config["current_playlist"]["name"] = user.get_playlist_name(0)

    with open('config.json', 'w') as f:
        print(json.dumps(config, indent=4), file=f)
