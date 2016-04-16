__author__ = 'Michal'

import sqlite3
from config import DIR_DATABASE

class DBManager(object):
    def __init__(self):
        self.db = sqlite3.connect("speeches.db")
        c = self.db.cursor()
        c.execute("CREATE TABLE ARGUMENT (name text primary key, vote text, isRepublican text, mentionType text)")
        self.db.commit()

    def insertSpeech(self, filename, vote, party, mentionType):
        if vote:
            vote = "T"
        else:
            vote = "F"

        c = self.db.cursor()
        args = (filename.decode("utf-8").rstrip(), vote.decode("utf-8").rstrip(), party.decode("utf-8").rstrip(), mentionType.decode("utf-8").rstrip())
        try:
            c.execute("INSERT INTO ARGUMENT VALUES (?,?,?,?)", args)
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            c.close()
            self.db.commit()
