# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Ben Williams <ben.williams@colorado.edu>
.. moduleauthor:: Michael Guida <michael.guida@colorado.edu>
.. moduleauthor:: Nicole Woyarowicz <nicole.woytarowicz@colorado.edu>
.. moduleauthor:: Kylie Dale <kylie.dale@colorado.edu>

"""

from __future__ import unicode_literals, print_function
import os
import util

import spotipy.util
import pygit2
import spotipy

class SpotifyUser(object):
    """
    A class that creates a Spotify user "self"
    """

    def __init__(self, username, client_id, client_secret, redirect_uri):
        """
        A class that creates a Spotify user "self"

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

        # add the scope for things we need, can change over time if we need
        # less
        scope = "playlist-read-private "
        scope += "playlist-read-collaborative "
        scope += "playlist-modify-public "
        scope += "playlist-modify-private "

        # directory that the gitfiles will be stored in
        self.git_dir = ".activePlaylists/"

        # need to write more code to get the author (and comitter)
        # might want to change comitter to local git user
        self.author = pygit2.Signature("spotify username", "spotify email")
        self.comitter = pygit2.Signature("spotify username", "spotify email")

        # gets the token from the spotify api, can not do anything without this
        self.token = spotipy.util.prompt_for_user_token(
                        username, client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope
                    )

        # error out if we don't have a token
        if self.token == None:
            raise RuntimeError("Cannot get token from " + username)

        # use the token to create a new spotify session
        self.sp = spotipy.Spotify(auth=self.token)

        # get the current spotify playlists
        self.playlists = self.sp.user_playlists(username)['items']

    def get_playlist_ids(self):
        """Funtion to get playlist ids of user

        :param self: Spotify user
        :returns: list -- list of ids in following format ''{"pid": foo, "uid": bar}''

        """
        ids = []
        for playlist in self.playlists:
            ids.append({"pid": playlist["id"], "uid": playlist["owner"]["id"]})

        return ids

    def get_playlist_id(self, position):
        """Function to get a single playlist's ID

        :param position: specifies what playlist to get
        :type position: string
        :returns: ID in following format '{"pid": foo, "uid": bar}'

        """
        position = int(position)
        return {"pid": self.playlists[position]["id"], "uid": self.playlists[position]["owner"]["id"]}

    def get_playlist_names(self):
        """Function to get all playlist names

        :returns: list -- of playlist names

        """
        names = []
        for playlist in self.playlists:
            names.append(playlist["name"])

        return names

    def get_playlist_from_id(self, pid):
        """Function that returns playlist name from pid

        :param pid: playlist ID
        :type pid: string
        :returns: playlist name

        """
        return self.sp.user_playlist(self.username, pid, fields="name")

    def get_playlist_name(self, position):
        """Function that returns playlist name from position

        :param position: specifies what playlist to get name from
        :type position: string
        :returns: playlist name

        """
        position = int(position)
        return self.playlists[position]["name"]

    def get_playlist_tracks(self, uid, pid):
        """Function to get tracks from pid

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID
        :type pid: string
        :returns: list -- tracks on playlist corresponding to pid

        """
        playlistInfo = self.sp.user_playlist(uid, pid)["tracks"]["items"]
        return playlistInfo

    def init_git_playlist(self, uid, pid):
        """Function to initialize playlist.

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID to initialize
        :type pid: string
        :raises: RuntimeError

        """
        playlist_path = os.path.join(uid, pid)

        # gets the track list IDs
        trackList = self.get_playlist_tracks(uid, pid)

        # make sure that the directories exist, if not create them
        os.makedirs(self.git_dir, exist_ok=True)
        os.makedirs(self.git_dir + playlist_path, exist_ok=True)

        if os.path.isfile(self.git_dir + playlist_path + "/index.txt"):
            raise RuntimeError("Tried to clone playlist when one of the " +
                               "same playlist has been cloned already.")

        with open(self.git_dir + playlist_path + "/index.txt", "w") as f:
            for track in trackList:
                if track["track"]["id"] != None:  # ignore local files
                    print(track["track"]["id"], file=f)

        # create repo and build tree
        new_repo = pygit2.init_repository(self.git_dir + playlist_path)
        new_tree = new_repo.TreeBuilder().write()

        first_commit = new_repo.create_commit(
            "HEAD", self.author, self.comitter, "Created master", new_tree, [])

        # create blob for the index file
        file_blob = new_repo.create_blob_fromdisk(
            os.path.join(self.git_dir, playlist_path, 'index.txt'))
        

        # build tree again
        new_tree = new_repo.TreeBuilder()

        # add our new index file
        new_tree.insert("index.txt", file_blob,
                os.stat(self.git_dir + playlist_path + "/index.txt").st_mode)

        # build tree again
        tree = new_tree.write()

        # add the index file to the repo
        new_repo.index.read()
        new_repo.index.add("index.txt")
        new_repo.index.write()

        # commit the file
        new_repo.create_commit(
            "HEAD", self.author, self.comitter, "Added index.txt", tree,
            [first_commit])

    def add_song_to_playlist(self, uid, pid, songid):
        """Function to add song to playlist

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID to add song to
        :type pid: string
        :param songid: ID of song to add
        :type songid: string
        :raises: RuntimeError

        """

        playlist_path = os.path.join(uid, pid)

        util.check_if_git_playlist(self.git_dir, playlist_path)

        with open(self.git_dir + playlist_path + "/index.txt", "r+") as f:
            songIds = []
            for line in f.readlines():
                line = line.strip()
                songIds.append(line)

                if songid == line:
                    raise RuntimeError("Song is already in playlist")
            print(songid, file=f)

        # get the repo
        repo = pygit2.Repository(self.git_dir + playlist_path)

        # create a new blob for our new index
        file_blob = repo.create_blob_fromdisk(
            self.git_dir + playlist_path + "/index.txt")

        # build the tree
        new_tree = repo.TreeBuilder()

        # add the index file
        new_tree.insert("index.txt", file_blob,
                        os.stat(self.git_dir + playlist_path + "/index.txt").st_mode)

        new_tree.write()

    def remove_song_from_playlist(self, uid, pid, songid):
        """Function to remove song from playlist

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID to remove song from
        :type pid: string
        :param songid: ID of song to remove
        :type songid: string
        :raises: RuntimeError

        """

        playlist_path = uid + "/" + pid

        util.check_if_git_playlist(self.git_dir, playlist_path)

        with open(self.git_dir + playlist_path + "/index.txt", "r+") as f:
            songIds = []
            found_song = False
            for line in f.readlines():
                line = line.strip()

                if songid == line:
                    found_song = True
                else:
                    songIds.append(line)

            if found_song == False:
                raise RuntimeError("playlist does not have song.")

            # go to the start of the text file
            f.seek(0)

            for ID in songIds:
                print(ID, file=f)

            # ignore the rest of the text file (parts that were already there)
            f.truncate()

        repo = pygit2.Repository(self.git_dir + playlist_path)

        # create the file blob
        file_blob = repo.create_blob_fromdisk(
            self.git_dir + playlist_path + "/index.txt")

        new_tree = repo.TreeBuilder()

        # insert it into the tree
        new_tree.insert("index.txt", file_blob,
                        os.stat(self.git_dir + playlist_path + "/index.txt").st_mode)

        new_tree.write()

    def commit_changes_to_playlist(self, uid, pid):
        """Function to commit changes to playlist

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID
        :type pid: string

        """

        playlist_path = uid + "/" + pid

        util.check_if_git_playlist(self.git_dir, playlist_path)

        # get the repo
        repo = pygit2.Repository(self.git_dir + playlist_path)

        # create the file blob
        file_blob = repo.create_blob_fromdisk(
            self.git_dir + playlist_path + "/index.txt")

        new_tree = repo.TreeBuilder()

        # insert it into the tree
        new_tree.insert("index.txt", file_blob,
                        os.stat(self.git_dir + playlist_path + "/index.txt").st_mode)

        tree = new_tree.write()

        # add to commit
        repo.index.read()
        repo.index.add("index.txt")
        repo.index.write()

        # commit changes to playlist
        repo.create_commit("HEAD", self.author, self.comitter,
                           "Changes committed to " + playlist_path, tree, [repo.head.target])

    def pull_spotify_playlist(self, uid, pid):
        """Function to pull playlist from Spotify

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID
        :type pid: string
        :returns: string -- stating status of pull (either successfull or not)

        """

        playlist_path = uid + "/" + pid

        util.check_if_git_playlist(self.git_dir, playlist_path)

        # grab tracks from spotify from pid
        results = self.sp.user_playlist_tracks(self.username, pid)
        results = results["items"]

        # get just a list of the track ids from the response
        remote_tracks = []
        for track in results:
            if track["track"]["id"] != None:  # only take spotify tracks
                remote_tracks.append(track["track"]["id"])

        # get local track ids
        with open(self.git_dir + playlist_path + "/index.txt") as f:
            local_tracks = f.read().splitlines()

        # merge tracks by adding if not added already. local takes precendence
        # does not preserve position of new remote tracks
        diff = False
        for remoteTrack in remote_tracks:
            if remoteTrack not in local_tracks:
                local_tracks.append(remoteTrack)
                diff = True

        # write tracks back to file
        with open(self.git_dir + playlist_path + "/index.txt", "w") as f:
            for track in local_tracks:
                print(track, file=f)

        # commit playlist changes if needed
        if diff:
            self.commit_changes_to_playlist(uid, pid)
            return 'Added and committed changes from remote.'
        return 'No changes committed, up to date with remote.'

    def push_spotify_playlist(self, uid, pid):
        """Function to push playlist to Spotify

        :param uid: user ID
        :type uid: string
        :param pid: playlist ID
        :type pid: string
        :returns: string -- stating status of pull (either successfull or not)

        """

        playlist_path = uid + "/" + pid

        util.check_if_git_playlist(self.git_dir, playlist_path)

        # grab tracks from spotify from pid
        results = self.sp.user_playlist_tracks(self.username, pid)
        results = results["items"]

        # get just a list of the track ids from the response
        remote_tracks = []
        for track in results:
            if track["track"]["id"] != None:  # only take spotify tracks
                remote_tracks.append(track["track"]["id"])

               # get local track ids
        with open(self.git_dir + playlist_path + "/index.txt") as f:
            local_tracks = f.read().splitlines()

        # merge tracks by adding if not added already. local takes precendence
        # does not preserve position of new remote tracks
        diff = False
        for remote_track in remote_tracks:
            if remote_track not in local_tracks:
                diff = True
                self.sp.user_playlist_remove_all_occurrences_of_tracks(
                    self.username, pid, [remote_track])

        for local_track in local_tracks:
            if local_track not in remote_tracks:
                diff = True
                self.sp.user_playlist_add_tracks(self.username, pid,
                                                 [local_track])
        if diff:
            return "Added and updated changes to the remote."
        return "No changes updated to the remote, remote and local are the same"

    def song_lookup(self, name=None, artist=None, limit=1):
        """Function to look up song

        :param name: name of song
        :type name: string
        :param artist: artist of song
        :type artist: string
        :param limit: max number of results to be returned
        :type limit: int
        :returns: dictionary -- with track name, artist, and ID

        """
        results = self.sp.search(q='track:' + name,
                                 type='track',
                                 limit=limit)

        if len(results['tracks']['items']) == 0:
            return "No results found for " + name
        else:
            songs = {}
            artists = results['tracks']['items'][0]['artists']
            artist_names = []
            for index, names in enumerate(artists):
                # stores main artist and all the featured artists
                artist_names.append(names['name'])
            songs['artists'] = artist_names
            songs['trackid'] = results['tracks']['items'][0]['id']
            songs['track'] = results['tracks']['items'][0]['name']

            # dictionary containing track name, artists, and track id
            return songs


if __name__ == "__main__":
    print("gitsound.py is a support libary, please run cli.py instead.")
