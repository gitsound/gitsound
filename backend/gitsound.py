# coding=utf-8
from __future__ import unicode_literals, print_function
import spotipy
import spotipy.util as util
import os
import pygit2


class spotifyUser(object):

    def __init__(self, username, client_id, client_secret, redirect_uri):
        """A class that creates a Spotify user "self"

        :param username: Name of Spotify user
        :type username: string 
        :param client_id: ID given by Spotify to user
        :type client_id: string
        :param client_secret: Confirmation to use program
        :type client_secret: string
        :param redirect_uri: Another Confirmation to use program
        :type redirect_uri: string

        """
        self.username = username

        # add the scope for things we need, can change over time if we need less
        scope = "playlist-read-private "
        scope += "playlist-read-collaborative "
        scope += "playlist-modify-public "
        scope += "playlist-modify-private "

        # directory that the gitfiles will be stored in
        self.gitDir = ".activePlaylists/"

        # need to write more code to get the author (and committer)
        # might want to change committer to local git user
        self.author = pygit2.Signature("spotify username", "spotify email")
        self.committer = pygit2.Signature("spotify username", "spotify email")

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

        self.tree = None;
        self.repo = None;

    def getPlaylistIDs(self):
        """Funtion to get playlist ids of user

        :param self: Spotify user
        :returns: list -- list of ids in following format '{userID}/{playlistID}'

        """
        ids = []
        for playlist in self.playlists:
            ids.append(playlist["owner"]["id"] + "/" + playlist["id"])

        return ids

    def getPlaylistTracks(self, pid):
        """Function to get tracks from playlist ID

        :param pid: Playlist ID to retrieve tracks from
        :type pid: int 
        :returns: list -- tracks on playlist (pid)

        """
        pid = pid.split("/")
        user = pid[0]
        playId = pid[1]
        playlistInfo = self.sp.user_playlist(user, playId)["tracks"]["items"]
        return playlistInfo

    def getTree(self):
        return self.tree

    def getRepo(self):
        return self.repo

    def initGitPlaylist(self, pid):
        """Function to initialize playlist.

        :param pid: Playlist ID to initialize
        :type pid: int
        :raises: RuntimeError

        """

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

        firstCom = newRepo.create_commit("HEAD", self.author, self.committer,
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
        self.tree = newTree.write()

        # add the index file to the repo
        newRepo.index.read()
        newRepo.index.add("index.txt")
        newRepo.index.write()

        # commit the file
        newRepo.create_commit(
            "HEAD", self.author, self.committer, "Added index.txt", self.tree,
            [firstCom])

    def addSongToPlaylist(self, pid, songid):
        """Function to add song to playlist

        :param pid: Playlist ID to add song to
        :type pid: int
        :param songid: ID of song to add
        :type songid: int
        :raises: RuntimeError

        """

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
        self.repo = pygit2.Repository(self.gitDir + user + "/" + playId)

        # create a new blob for our new index
        fileBlob = self.repo.create_blob_fromdisk(
            self.gitDir + pid + "/index.txt")

        # build the tree
        newTree = self.repo.TreeBuilder()

        # add the index file
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + pid + "/index.txt").st_mode)

        self.tree = newTree.write()

    def removeSongFromPlaylist(self, pid, songid):
        """Function to remove song from playlist

        :param pid: Playlist ID to remove song from
        :type pid: int
        :param songid: ID of song to remove
        :type songid: int
        :raises: RuntimeError

        """

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

        self.repo = pygit2.Repository(self.gitDir + user + "/" + playId)

        # create the file blob
        fileBlob = self.repo.create_blob_fromdisk(
            self.gitDir + pid + "/index.txt")

        newTree = self.repo.TreeBuilder()

        # insert it into the tree
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + pid + "/index.txt").st_mode)

        self.tree = newTree.write()

    def commitChangesToPlaylist(self, pid, tree):
        """Function to commit changes to playlist locally

        :param pid: Playlist ID to commit changes to 
        :type pid: int
        :param tree: Tree to crete commit with 

        """
        
        # add to commit 
        self.repo.index.read()
        self.repo.index.add("index.txt")
        self.repo.index.write()

        # commit changes to playlist
        self.repo.create_commit("HEAD", self.author, self.committer,
                           "Changes committed to " + pid, tree, [self.repo.head.target])


if __name__ == "__main__":
    print("gitSound.py is a support libary, please run main.py instead.")
