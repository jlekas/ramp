#cache lookup by messageid containing dictionary of response and ip address
#only want to store messageid for certain period of time
#message id to be id different for all queries
#could use database that stores messageid; num -1,0,1 indicating
#not found last, on local, on friend; local path; friend ip it looked last time

import os
import sqlite3

class query:
    def __init__(self, messageID, userID):
        self.messageId = messageID
        self.userID = userID

    def __repr__(self):
        return ("query{message: "+self.messageId+", userId: "+self.userID+"}")
    
    def alreadySeen(self):
        #look in database to see if query seen already
        return 0

    def displayFiles(path):
        if (os.path.isdir(path) == False):
            return [path]
        else:
            files = []
            for file in os.listdir(path):
                files += listFiles(path+ os.pathsep + file)
            return files

    def publicLookup(self):
        #looks up query in public directory
        files = listFiles("Public")
        return 0

    def privateLookup(self):
        #looks up query in private directory
        return 0
