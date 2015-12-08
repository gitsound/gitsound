import json
import os


def load_config():
    """Function to load the config file

    :returns: the config file
    :raises: RuntimeError

    """
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
    """Function to save the config file

    :raises: RuntimeError

    """
    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py to reconfigure.")

    with open('config.json', 'w') as f:
        j = json.dumps(data, indent=4)
        print >> f, j


def check_if_git_playlist(gitDir, playlistPath):
    """Function to check if playlist path is valid

    :raises: RuntimeError

    """

    # make sure the directories exist
    os.makedirs(gitDir, exist_ok=True)
    os.makedirs(gitDir + playlistPath, exist_ok=True)

    if os.path.isfile(gitDir + playlistPath + "/index.txt") == False:
        raise RuntimeError("Playlist has not been initiated.")
