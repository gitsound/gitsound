import json
import os


def load_config():
    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py to reconfigure.")

    with open("config.json") as configFile:
        try:
            config = json.loads(configFile.read())
        except:
            raise RuntimeError(
                "Improperly formatted config.json. Run setup.py to reconfigure.")

    return config


def save_config(data):
    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py to reconfigure.")

    with open('config.json', 'w') as f:
        print(json.dumps(data, indent=4), file=f)


def check_if_git_playlist(gitDir, playlistPath):

    # make sure the directories exist
    os.makedirs(gitDir, exist_ok=True)
    os.makedirs(gitDir + playlistPath, exist_ok=True)

    if os.path.isfile(gitDir + playlistPath + "/index.txt") == False:
        raise RuntimeError("Playlist has not been initiated.")
