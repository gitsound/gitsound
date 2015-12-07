#! /usr/bin/env python

"""File that sets up a user's system upon running command line. 

Only need to run this file once when initally setting up GitSound.

.. note:: 
    User will need to obtain a client_id and client_secret from Spotify.

"""
from pygit2 import Repository
import gitsound
import json
import os

if __name__ == '__main__':
    if (os.path.isfile("config.json") == True):
        with open('config.json', 'r') as f:
            try:
                config = json.load(f)
            except:
                config = {}
    else:
        config = {}

    config["name"] = input("name: ")
    config["email"] = input("email: ")
    config["uid"] = input("spotify username: ")

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
