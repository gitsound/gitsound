#! /usr/bin/env python


import sqlite3

# Connecting to the database file
conn = sqlite3.connect('gitsound.sqlite')
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'
          .format(tn='users', nf='username', ft='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"
          .format(tn='users', cn='password', ct='TEXT'))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
