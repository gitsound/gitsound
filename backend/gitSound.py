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

        self.tree = None;
        self.repo = None;

    def getPlaylistIDs(self):
        ids = []
        for playlist in self.playlists:
            ids.append({"pid": playlist["id"], "uid": playlist["owner"]["id"]})

        # returns a list of ids in the following format '{"pid": foo, "uid": bar}'
        return ids

    def getPlaylistId(self, position):
        position = int(position)
        return {"pid": self.playlists[position]["id"], "uid": self.playlists[position]["owner"]["id"]}

    def getPlaylistNames(self):
        names = []
        for playlist in self.playlists:
            names.append(playlist["name"])

        return names

    def getPlaylistName(self, position):
        position = int(position)
        return self.playlists[position]["name"]

    def getPlaylistTracks(self, uid, pid):
        playlistInfo = self.sp.user_playlist(uid, pid)["tracks"]["items"]
        return playlistInfo

    def initGitPlaylist(self, uid, pid):

        playlistPath = uid + "/" + pid

        # gets the track list IDs
        trackList = self.getPlaylistTracks(uid, pid)

        # make sure that the directories exist, if not create them
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + playlistPath, exist_ok=True)

        if os.path.isfile(self.gitDir + playlistPath + "/index.txt"):
            raise RuntimeError("Tried to clone playlist when one of the " +
                               "same playlist has been cloned already.")

        with open(self.gitDir + playlistPath + "/index.txt", "w") as textFile:
            for track in trackList:
                if track["track"]["id"] != None:  # ignore local files
                    print(track["track"]["id"], file=textFile)

        # create repo and build tree
        newRepo = pygit2.init_repository(self.gitDir + playlistPath)
        newTree = newRepo.TreeBuilder().write()

        firstCom = newRepo.create_commit("HEAD", self.author, self.comitter,
                                         "Created master", newTree, [])

        # create blob for the index file
        fileBlob = newRepo.create_blob_fromdisk(
            self.gitDir + playlistPath + "/index.txt")

        # build tree again
        newTree = newRepo.TreeBuilder()

        # add our new index file
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + playlistPath + "/index.txt").st_mode)

        # build tree again
        self.tree = newTree.write()

        # add the index file to the repo
        newRepo.index.read()
        newRepo.index.add("index.txt")
        newRepo.index.write()

        # commit the file
        newRepo.create_commit(
            "HEAD", self.author, self.comitter, "Added index.txt", self.tree,
            [firstCom])

    def addSongToPlaylist(self, uid, pid, songid):

        playlistPath = uid + "/" + pid

        # make sure the directories exist
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + playlistPath, exist_ok=True)

        if os.path.isfile(self.gitDir + playlistPath + "/index.txt") == False:
            raise RuntimeError("Playlist has not been initiated.")

        with open(self.gitDir + playlistPath + "/index.txt", "r+") as textFile:
            songIds = []
            for line in textFile.readlines():
                line = line.strip()
                songIds.append(line)

                if songid == line:
                    raise RuntimeError("Song is already in playlist")
            print(songid, file=textFile)

        # get the repo
        self.repo = pygit2.Repository(self.gitDir + playlistPath)

        # create a new blob for our new index
        fileBlob = self.repo.create_blob_fromdisk(
            self.gitDir + playlistPath + "/index.txt")

        # build the tree
        newTree = self.repo.TreeBuilder()

        # add the index file
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + playlistPath + "/index.txt").st_mode)

        self.tree = newTree.write()

    def removeSongFromPlaylist(self, uid, pid, songid):

        playlistPath = uid + "/" + pid

        # check to see if the directories exist
        os.makedirs(self.gitDir, exist_ok=True)
        os.makedirs(self.gitDir + playlistPath, exist_ok=True)

        if os.path.isfile(self.gitDir + playlistPath + "/index.txt") == False:
            raise RuntimeError("Playlist has not been initiated.")

        with open(self.gitDir + playlistPath + "/index.txt", "r+") as textFile:
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

        self.repo = pygit2.Repository(self.gitDir + playlistPath)

        # create the file blob
        fileBlob = self.repo.create_blob_fromdisk(
            self.gitDir + playlistPath + "/index.txt")

        newTree = self.repo.TreeBuilder()

        # insert it into the tree
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + playlistPath + "/index.txt").st_mode)

        self.tree = newTree.write()

    def commitChangesToPlaylist(self, uid, pid):

        playlistPath = uid + "/" + pid

        # get the repo
        self.repo = pygit2.Repository(self.gitDir + playlistPath)

        # create the file blob
        fileBlob = self.repo.create_blob_fromdisk(
            self.gitDir + playlistPath + "/index.txt")

        newTree = self.repo.TreeBuilder()

        # insert it into the tree
        newTree.insert("index.txt", fileBlob,
                       os.stat(self.gitDir + playlistPath + "/index.txt").st_mode)

        self.tree = newTree.write()

        # add to commit
        self.repo.index.read()
        self.repo.index.add("index.txt")
        self.repo.index.write()

        # commit changes to playlist
        self.repo.create_commit("HEAD", self.author, self.comitter,
                           "Changes committed to " + playlistPath, self.tree, [self.repo.head.target])

    def pullSpotifyPlaylist(self, uid, pid):

        palylistPath = uid + "/" + pid

        # check if we have a git playlist before continuing
        if not os.path.isfile(self.gitDir + playlistPath + "/index.txt"):
            print('No git playlist found. Clone playlist first.')

        # grab tracks from spotify from pid
        results = self.sp.user_playlist_tracks(self.username, pid)
        results = results["items"]

        # get just a list of the track ids from the response
        remoteTracks = []
        for track in results:
            if track["track"]["id"] != None: # only take spotify tracks
                remoteTracks.append(track["track"]["id"])

        # get local track ids
        with open(self.gitDir + playlistPath + "/index.txt") as f:
            localTracks = f.read().splitlines()

        # merge tracks by adding if not added already. local takes precendence
        # does not preserve position of new remote tracks
        diff = False
        for remoteTrack in remoteTracks:
            if remoteTrack not in localTracks:
                localTracks.append(remoteTrack)
                diff = True

        # write tracks back to file
        with open(self.gitDir + palylistPath + "/index.txt", "w") as f:
            for track in localTracks:
                print(track, file=f)

        # commit playlist changes if needed
        if (diff == True):
            self.commitChangesToPlaylist(uid, pid)
            return 'Added and committed changes from remote.'
        return 'No changes committed, up to date with remote.'

    def songLookup(self, name=None, artist=None, limit=1):
        results = self.sp.search(q='track:' + name,
            type='track',
            limit=limit)

        if len(results['tracks']['items']) == 0: # if no songs found with that name
            print("No results found for " + name)
            return
            # not sure if we want the above to raise an error/warning or just print out
        else:
            songs = {}
            artists = results['tracks']['items'][0]['artists']
            artistNames = []
            for index, names in enumerate(artists):
                artistNames.append(names['name']) # stores main artist and all the featured artists
            songs['artists'] = artistNames
            songs['trackid'] = results['tracks']['items'][0]['id']
            songs['track'] = results['tracks']['items'][0]['name']
            print("Results for " + songs['track'] + ' by ' + songs['artists'][0])
            return songs # dictionary containing track name, artists, and track id


if __name__ == "__main__":
    print("gitSound.py is a support libary, please run main.py instead.")
