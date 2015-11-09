#! /usr/bin/env python

from pygit2 import Repository
import gitSound
import json
import os

def login():
    askText = "please enter your spotify username: "
    username = input(askText)

    if os.path.isfile("gitSound_config.txt") == False:
        raise RuntimeError(
            "cannot find gitSound_config.txt in the working directory")

    with open("gitSound_config.txt") as configFile:
        configVars = json.loads(configFile.read())

    newUser = gitSound.spotifyUser(
        username, configVars["client_id"], configVars["client_secret"],
        "http://localhost/callback")

    return newUser


if __name__ == '__main__':

    user = login()
    currentPID = user.getPlaylistIDs()[6]

    with open('data.json', 'r+') as f:
        data = json.load(f)
        data['user_id'] = user.username
        data['current_pid'] = currentPID
        f.seek(0)
        json.dump(data, f, indent=4)
