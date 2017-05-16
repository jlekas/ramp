#cache lookup by messageid containing dictionary of response and ip address
#only want to store messageid for certain period of time
#message id to be id different for all queries
#could use database that stores messageid; num -1,1,2 indicating
#not found last, on local, on friend; local path; friend ip it looked last time

import os
import sqlite3


class query:
    def __init__(self, messageID, userID):
        self.messageID = messageID
        self.userID = userID

    def __repr__(self):
        return ("query{message: "+self.messageID+", userId: "+self.userID+"}")
    
    def alreadySeen(self):
        #returns 0 if not seen, -1 if seen and not found, 1 if found local,
        #2 if found on other peer
        #connect to database and check if seen
        sqlite_file = "Ramp.sqlite"
        db = sqlite3.connect(sqlite_file)
        cursor = db.cursor()
        #look in database to see if query seen already
        cursor.execute(
            '''SELECT foundInt, localPath, hostName FROM queries where
            messageID=?''', (self.messageID, )
            )
        q = cursor.fetchone()
        db.close()
        if (q == None):
            return 0
        return q[1]

    def displayFiles(self, path):
        if (os.path.isdir(path) == False):
            return [path]
        else:
            files = []
            for file in os.listdir(path):
                files += self.displayFiles(path+ os.pathsep + file)
            return files

    def publicLookup(self):
        #if message was looked for and not found return -1 to indicate 
        #that this peer looked for the query already and it/ its connections
        #didn't have what was looked for
        seen = self.alreadySeen()
        if (seen == -1):
            return -1
        #query hasn't been seen so looks up query in public directory
        files = self.displayFiles("Public")
        print(files)
        return 0

    def privateLookup(self):
        #if message was looked for and not found return -1 to indicate 
        #that this peer looked for the query already and it/ its connections
        #didn't have what was looked for
        seen = self.alreadySeen()
        if (seen == -1):
            return -1
        #query hasn't been seen so looks up query in public directory
        files = self.displayFiles("Public")
        files += self.displayFiles("Private")
        print(files)
        return 0

