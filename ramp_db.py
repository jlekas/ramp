import sqlite3
import os
from datetime import date, datetime

class chatMessage:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def add_db(self):
        sqlite_file = "Ramp.sqlite"
        db = sqlite3.connect(sqlite_file,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cursor = db.cursor()
        n = datetime.now()
        cursor.execute(
            '''INSERT INTO messages(sender, receiver, message, message_time) VALUES(?,?,?,?)''', (self.sender, self.receiver, self.message, n)
            )
        db.commit()
        db.close()
        return


def getChats(sender, receiver):
    sqlite_file = "Ramp.sqlite"
    db = sqlite3.connect(sqlite_file,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = db.cursor() 
    cursor.execute(
        '''SELECT * FROM messages WHERE sender=? OR receiver=?''', (sender,receiver))
    log = cursor.fetchall()
    db.commit()
    db.close()
    print(log)
    return log
