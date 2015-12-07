import sqlite3


def validate_user(username, password):
    """Function to validate or create a user.
    :param username: username
    :type username: string
    :param password: password
    :type password: string
    :returns: boolean -- true if user is valid, false otherwise
    """

    conn = sqlite3.connect('./.gitsound.sqlite')
    c = conn.cursor()

    c.execute("SELECT * FROM {tn} WHERE {uf} = ?".
              format(tn='users', uf='username'), (username,))

    user = c.fetchone()

    if user != None:
        # user exists, check if password matches
        if (password == user[1]):
            success = True
        else:
            success = False

    else:
        # user doesn't exist, must be created
        c.execute("INSERT INTO {tn} ({uf}, {pf}) VALUES (?, ?)".
                  format(tn='users', uf='username', pf='password'), (username, password))

        success = True

    conn.commit()
    conn.close()

    return success

if __name__ == "__main__":
    print("login.py is a support libary, please run cli.py instead.")
