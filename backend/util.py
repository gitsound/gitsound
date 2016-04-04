import json
import os


def load_config():
    """Function to load the config file

    :returns: the config file
    :raises: RuntimeError

    """
    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py"
            " to reconfigure.")

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
    :param data: data to be written to the config file
    """
    if os.path.isfile("config.json") == False:
        raise RuntimeError(
            "Cannot find config.json. Ensure proper directory or run setup.py"
            "to reconfigure.")

    with open('config.json', 'w') as f:
        print(json.dumps(data, indent=4), file=f)


def check_if_git_playlist(gitDir, playlistPath):
    """Function to check if playlist path is valid

    :raises: RuntimeError
    :param gitDir: 
    :param playlistPath: 
    """
    absolute_playlist_path = os.path.join(gitDir, playlistPath)

    # make sure the directories exist
    os.makedirs(gitDir, exist_ok=True)
    os.makedirs(absolute_playlist_path, exist_ok=True)

    index_file = os.path.join(absolute_playlist_path, 'index.txt')
    if os.path.isfile(index_file) == False:
        raise RuntimeError("Playlist has not been initiated.")
