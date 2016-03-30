# GitSound

Git for Music

## Setup

GitSound only supports `python 3`. 

`$ git clone https://github.com/GitSound/GitSound && cd GitSound

#### Installing the requirements

`$ pip install -r requirements.txt`

To setup GitSound, run the setup script from your terminal. You will need to get a client id and client secret key from Spotify.

```
$ python3 setup.py
```

## Usage Examples

To run the CLI:

```
$ python3 cli.py <command>
```

#### Show all options/help
```
$ python3 cli.py -h
GitSound

Usage:
  cli.py <command> [<argument>] [--help]

options:
  -h, --help             Show this message.

Command List:
  show [local | remote]  Show all playlists locally or from spotify
  select <playlist_id>   Set the current playlist
  clone <playlist_id>    Clone a playlist from spotify
  add <track_id>         Add a track by id to the current playlist
  remove <track_id>      Remove a track by id from the current playlist
  pull                   Pull changes from spotify into current playlist
  status                 See all changes to be committed
  commit                 Commit all changes
```

#### Show all of your playlists from Spotify
```
$ python3 cli.py show remote
0 |   Rock
1 |   Pop
2 |   Blues
3 |   Starred
```

#### Select the first playlist by id
```
$ python3 cli.py select 0
Set current playlist to Rock
```

## How it works

When a playlist is initialized it will create a git version controlled playlist locally on your computer. This aheres to the following structure.

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

Using a structure of `userId/playlistId/index.txt` allows us to keep git functioning as it would out of the box, while version controlling many different playlists. A `playlistId` from Spotify is only guaranteed to be unique to each `userId` and a `userId` is always guaranteed to be unique. This allows GitSound to organize many different playlists without the risk of collision. Each playlist will be contained within an `index.txt` file that stores the `trackIds` of the given playlist. These files are what get version controlled, so we can take advantage of git features like history of commits, branching and more.

# License
MIT

Org. icon made by [Freepik](http://www.freepik.com) from [Flaticon](http://www.flaticon.com) licensed under [CC 3.0](http://creativecommons.org/licenses/by/3.0/)
