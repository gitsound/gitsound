# coding=utf-8
from __future__ import unicode_literals, print_function
import gitSound
import sys
import json
import os
import unittest


class test_spotifyUser(unittest.TestCase):

    def setUp(self):

        if os.path.isfile("test_config.txt") == False:
            raise RuntimeError(
                "cannot find test_config.txt in the current working directory")

        with open("test_config.txt") as configFile:
            self.testVars = json.loads(configFile.read())

        if "username" not in self.testVars or self.testVars["username"] == "":
            raise RuntimeError("did not find 'username' in test_config.txt")

        if os.path.isfile("gitSound_config.txt") == False:
            raise RuntimeError(
                "cannot find gitSound_config.txt in the" +
                "current working directory")

        with open("gitSound_config.txt") as configFile:
            self.configVars = json.loads(configFile.read())

    def tearDown(self):
        print("tearing down...")

    def test_init(self):

        newUser = gitSound.spotifyUser(
            self.testVars["username"], self.configVars[
                "client_id"], self.configVars["client_secret"],
            self.configVars["redirect_uri"])

        self.assertEqual(newUser.author.name, newUser.comitter.name,
                         "Author and Comitter name are not the same")

        self.assertEqual(newUser.username, self.testVars[
                         "username"], "Username not assigned correctly")

        self.spotifyUser = newUser

    def test_getPlaylistIDs(self):

        newUser = gitSound.spotifyUser(
            self.testVars["username"], self.configVars[
                "client_id"], self.configVars["client_secret"],
            self.configVars["redirect_uri"])

        playlists = newUser.getPlaylistIDs()

        self.assertEqual(type(playlists), list, "did not return a list")

        for item in playlists:
            items = item.split("/")
            self.assertEqual(
                len(items), 2, "Playlist ID does not have two parts")


if __name__ == "__main__":
    fooSuite = unittest.main()
