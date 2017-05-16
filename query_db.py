import sqlite3

sqlite_file = "Ramp.sqlite"
table_name1 = "Queries"

connect = sqlite3.connect(sqlite_file)
c = connect.cursor()

#make the queries table
c.execute('''
        CREATE TABLE queries(
            messageID varchar(255),
            foundInt int,
            localPath varchar(255),
            hostName varchar(255)
            );
        ''')
connect.commit()
connect.close()
