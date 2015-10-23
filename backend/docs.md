# CLI Documentation

Documentation for the backend of GitSound

## main.py

The main entry point for GitSound. Handles authenticating a user with spotify.

#### Steps to run main.py in terminal: <br/>
  0. Make sure the .activePlaylists directory is deleted in the backend folder <br/>
  1. In the terminal type: python3 main.py <br/>
  2. Enter in your Spotify username when prompted <br/>
  3. cd into .activePlaylists/../.. until you reach the file index.txt <br/>
  4. Open file to view changes made 

## cli.py

The CLI for gitSound. This is the way a user interacts with the program, and it kicks off other functions as needed. Has no functionality of its own other than parsing commands and calling the relevant functions.

## gitSound.py

The API for GitSound.

##### getPlaylistIDs():

Returns a list of ids for the users playlist in the following format `{userID}/{playlistID}`.

##### getPlaylistTracks(playlistId):

Returns all of the trackIds from the playlist.

##### initGitPlaylist(playlistId):

Initializes a new git playlist.

##### addSongToPlaylist(playlistId, trackId):

Adds the given track to the given playlist and commits the change.

##### removeSongFromPlaylist(playlistId, trackId):

Removes the given track from the given playlist and commits the change.
