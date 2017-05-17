import sqlite3
import os

class chatMessage:
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def add_db(self):
        sqlite_file = "Ramp.sqlite"
        db = sqlite3.connect(sqlite_file)
        cursor = db.cursor()
        cursor.execute(
            '''INSERT INTO messages())
