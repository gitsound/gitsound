"""File that runs tests against GitSound.

"""
# coding=utf-8
from __future__ import unicode_literals, print_function
import gitSound
import sys
import json
import os
import unittest


class test_spotifyUser(unittest.TestCase):
    """This class runs tests against the spotifyUser.

    """

    def setUp(self):
        """Function that sets up config file and checks vailidity of username.

        """

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
        """Function that is called when tests fail.

        """
        print("tearing down...")

    def test_init(self):
        """TestCase run against playlist initalization.

        """

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
        """TestCase to test playlist ID retrieval.

        Tests to make sure the function returns a list of playlist IDs and tests to ensure the list has two parts.

        """

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
