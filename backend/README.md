# GitSound Backend

The python3 backend for GitSound.

When a playlist is initialized it will create a git version controlled playlist locally on your computer. This follows the following structure.

```
|-- .activePlaylists/
    |-- userId_01/
        |-- playlistId_01/
            |-- .git/
            |-- index.txt
        |-- playlistId_02/
            |-- .git/
            |-- index.txt
        |-- playlistId_03/
            |-- .git/
            |-- index.txt
    |-- userId_02/
        |-- playlistId_01/
            |-- .git/
            |-- index.txt
```

Using a structure of `userId/playlistId/index.txt` allows us to keep git functioning as it would out of the box, while version controlling many different playlists. A `playlistId` from spotify is only guaranteed to be unique to each `userId` and a `userId` is guaranteed to be unique. This allows GitSound to organize many different playlists without the risk of collision. Each playlist will be contained within an `index.txt` file that stores the `trackIds` of the given playlist. These files are what get version controlled, so we can take advantage of git features like history of commits, branching and more.

## Setup

To setup GitSound, run the setup script from your terminal. You will need to get a client id and client secret key from Spotify.

```
$ python3 setup.py
```

## Usage

To run the CLI

```
$ python3 cli.py <command>
```

## Documentation

[Docs](https://github.com/GitSound/GitSound/blob/master/backend/docs.md)
