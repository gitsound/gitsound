# GitSound
Git for Music

## Setup

GitSound only supports python 3.

```sh
$ pip3 install spotipy
# pygit2 may require libgit2
$ pip3 install pygit2
$ pip3 install docopt==0.6.1
```

## CLI

```
$ cd backend/
```

To run the CLI

```
$ python3 cli.py <command>
```

[Docs](https://github.com/GitSound/GitSound/blob/master/backend/docs.md)

## Web

```
$ cd frontend/
```

To run the website run this, then visit `localhost:4200/`

```
$ ember s
```

All tests use [Mocha](https://mochajs.org/) and [Chai](http://chaijs.com/). To run the tests:

```
$ ember t -s
```

# License
MIT

Org. icon made by [Freepik](http://www.freepik.com) from [Flaticon](http://www.flaticon.com) licensed under [CC 3.0](http://creativecommons.org/licenses/by/3.0/)
