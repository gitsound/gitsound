# coding=utf-8
from __future__ import unicode_literals, print_function
import spotipy
import spotipy.util as util
import os
import pygit2


class spotifyUser(object):

    def __init__(self, username, client_id, client_secret, redirect_uri):
        self.username = username

        # add the scope for things we need, can change over time if we need
        # less
        scope = "playlist-read-private "
        scope += "playlist-read-collaborative "
        scope += "playlist-modify-public "
        scope += "playlist-modify-private "

        # directory that the gitfiles will be stored in
        self.gitDir = ".activePlaylists/"

        # need to write more code to get the author (and comitter)
        # might want to change comitter to local git user
        self.author = pygit2.Signature("spotify username", "spotify email")
        self.comitter = pygit2.Signature("spotify username", "spotify email")

        # gets the token from the spotify api, can not do anything without this
        self.token = util.prompt_for_user_token(
            username, client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope)

        # error out if we don't have a token
        if self.token == None:
            raise RuntimeError("Cannot get token from " + username)

        # use the token to create a new spotify session
        self.sp = spotipy.Spotify(auth=self.token)

        # get the current spotify playlists
        self.playlists = self.sp.user_playlists(username)['items']

    def getPlaylistIDs(self):
        ids = []
        for playlist in self.playlists:
            ids.append(playlist["owner"]["id"] + "/" + playlist["id"])

        # returns a list of ids in the following format '{userID}/{playlistID}'
        return ids

    def getPlaylistTracks(self, pid):
        pid = pid.split("/")
        user = pid[0]
        playId = pid[1]
        playlistInfo = self.sp.user_playlist(user, playId)["tracks"]["items"]
        return playlistInfo

    def initGitPlaylist(self, pid):

        # gets the track list IDs
        trackList = self.getPlaylistTracks(pid)

        # make sure that the directories exist, if not create them
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + pid, exist_ok=True)

        if os.path.isfile(self.gitDir + pid + "/index.txt"):
            raise RuntimeError("Tried to init git playlist when one of the " +
                               "same playlist has been initiated already.")

        with open(self.gitDir + pid + "/index.txt", "w") as textFile:
            for track in trackList:
                if track["track"]["id"] != None:  # ignore local files
                    print(track["track"]["id"], file=textFile)

        # create repo and build tree
        newRepo = pygit2.init_repository(self.gitDir + pid)
        newTree = newRepo.TreeBuilder().write()

        firstCom = newRepo.create_commit("HEAD", self.author, self.comitter,
                                         "Created master", newTree, [])

        # create blob for the index file
        fileBlob = newRepo.create_blob_fromdisk(
            self.gitDir + pid + "/index.txt")

        # build tree again
        newTree = newRepo.TreeBuilder()

        # add our new index file
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + pid + "/index.txt").st_mode)

        # build tree again
        tree = newTree.write()

        # add the index file to the repo
        newRepo.index.read()
        newRepo.index.add("index.txt")
        newRepo.index.write()

        # commit the file
        newRepo.create_commit(
            "HEAD", self.author, self.comitter, "Added index.txt", tree,
            [firstCom])

    def addSongToPlaylist(self, pid, songid):

        # make sure the directories exist
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + pid, exist_ok=True)

        if os.path.isfile(self.gitDir + pid + "/index.txt") == False:
            raise RuntimeError("Playlist has not been initiated.")

        with open(self.gitDir + pid + "/index.txt", "r+") as textFile:
            songIds = []
            for line in textFile.readlines():
                line = line.strip()
                songIds.append(line)

                if songid == line:
                    raise RuntimeError("Song is already in playlist")
            print(songid, file=textFile)

        pidSplit = pid.split("/")
        user = pidSplit[0]
        playId = pidSplit[1]

        # get the repo
        repo = pygit2.Repository(self.gitDir + user + "/" + playId)

        # create a new blow for our new index
        fileBlob = repo.create_blob_fromdisk(
            self.gitDir + pid + "/index.txt")

        # build the tree
        newTree = repo.TreeBuilder()

        # add the index file
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + pid + "/index.txt").st_mode)

        tree = newTree.write()

        # add the new index file to the commit
        repo.index.read()
        repo.index.add("index.txt")
        repo.index.write()

        # commit the new file
        repo.create_commit("HEAD", self.author, self.comitter,
                           "Added " + songid, tree, [repo.head.target])

    def removeSongFromPlaylist(self, pid, songid):

        # check to see if the directories exist
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + pid, exist_ok=True)

        if os.path.isfile(self.gitDir + pid + "/index.txt") == False:
            raise RuntimeError("Playlist has not been initiated.")

        with open(self.gitDir + pid + "/index.txt", "r+") as textFile:
            songIds = []
            foundSong = False
            for line in textFile.readlines():
                line = line.strip()

                if songid == line:
                    foundSong = True
                else:
                    songIds.append(line)

            if foundSong == False:
                raise RuntimeError("playlist does not have song.")

            # go to the start of the text file
            textFile.seek(0)

            for ID in songIds:
                print(ID, file=textFile)

            # ignore the rest of the text file (parts that were already there)
            textFile.truncate()

        pidSplit = pid.split("/")
        user = pidSplit[0]
        playId = pidSplit[1]

        repo = pygit2.Repository(self.gitDir + user + "/" + playId)

        # create the file blob
        fileBlob = repo.create_blob_fromdisk(
            self.gitDir + pid + "/index.txt")

        newTree = repo.TreeBuilder()

        # insert it into the tree
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + pid + "/index.txt").st_mode)

        tree = newTree.write()

        # add it to the commit
        repo.index.read()
        repo.index.add("index.txt")
        repo.index.write()

        # commit
        repo.create_commit("HEAD", self.author, self.comitter,
                           "Removed " + songid, tree, [repo.head.target])


if __name__ == "__main__":
    print("gitSound.py is a support libary, please run main.py instead.")