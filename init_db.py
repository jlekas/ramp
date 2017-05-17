import sqlite3

sqlite_file = "Ramp.sqlite"
table_name1 = "Queries"

db = sqlite3.connect(sqlite_file)
c = db.cursor()

#make the queries table
c.execute('''
        CREATE TABLE queries(
            messageID int
            );
        ''')
c.execute('''
        CREATE TABLE messages(
            user TEXT,
            message TEXT
            time TIMESTAMP
            );
        ''')
db.commit()
db.close()
