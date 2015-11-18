#! /usr/bin/env python

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
    config["current_playlist"]["uid"] = ids["uid"]
    config["current_playlist"]["pid"] = ids["pid"]

    with open('config.json', 'w') as f:
        print(json.dumps(config, indent=4), file=f)
