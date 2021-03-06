__author__ = 'Michal'

import sqlite3


class DBManager(object):
    def __init__(self):
        self.db = sqlite3.connect("speeches.db")

    def create(self):
        c = self.db.cursor()
        c.execute("DROP TABLE IF EXISTS ARGUMENT")
        c.execute("CREATE TABLE ARGUMENT (name text primary key, vote text, isRepublican text, mentionType text)")
        self.db.commit()

    def insert_speech(self, filename, vote, party, mention_type):
        if vote:
            vote = "T"
        else:
            vote = "F"

        c = self.db.cursor()
        args = (filename.decode("utf-8").rstrip(), vote.decode("utf-8").rstrip(), party.decode("utf-8").rstrip(), mention_type.decode("utf-8").rstrip())
        try:
            c.execute("INSERT INTO ARGUMENT VALUES (?,?,?,?)", args)
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            c.close()
            self.db.commit()

    def get_infos(self, count=None, vote=None):
        c = self.db.cursor()
        c.execute("SELECT * FROM ARGUMENT")
        self.db.commit()

        rows_outputted = 0

        for row in c:
            if count is not None:
                if rows_outputted >= count:
                    break

            if (vote == row[1]) or (vote is None):
                rows_outputted += 1
                yield {"filename": row[0], "vote_bool": row[1] == "T", "mention_type": row[2]}
