#! /usr/bin/env python

from pygit2 import Repository
import gitSound
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
    config["user_id"] = input("spotify username: ")

    if ("client_id" not in config):
        config["client_id"] = input("client id: ")
    if ("client_secret" not in config):
        config["client_secret"] = input("client_secret: ")

    config["redirect_uri"] = "http://localhost/callback"

    user = gitSound.spotifyUser(
        config["user_id"], config["client_id"], config["client_secret"],
        config["redirect_uri"])

    config["current_pid"] = user.getPlaylistIDs()[0]

    with open('config.json', 'w') as f:
        print(json.dumps(config, indent=4), file=f)
