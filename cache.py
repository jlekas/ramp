#cache lookup by messageid containing dictionary of response and ip address
#only want to store messageid for certain period of time
#message id to be id of message to see if gotten message fom other peer
#different types of queries,
#message is actual search either specific file or things looking for
#could use database that stores messageid; num -1,1 indicating
#not found last, on friend; friend ip it looked last time

import os
import sqlite3

class query:
    def __init__(self, messageID, message):
        self.messageID = messageID
        self.message = message
        self.userID = userID

    def __repr__(self):
        return ("query{message: "+self.messageID+", userId: "+self.userID+"}")
    
    def alreadySeen(self):
        #returns -1 if not seen, 0 if seen 
        #connect to database and check if seen
        sqlite_file = "Ramp.sqlite"
        db = sqlite3.connect(sqlite_file)
        cursor = db.cursor()
        #look in database to see if query seen already
        cursor.execute(
            '''SELECT * FROM queries where messageID=?''', (self.messageID, )
            )
        q = cursor.fetchone()
        db.close()
        if (q == None):
            return -1
        #if not seen add query to table
        cursor.execute(
            '''INSERT INTO queries(messageID) VALUES(?)''', (self.messageID, )
            )
        #returns fountInt
        db.close()
        return 0

    def displayFiles(self, path):
        if (os.path.isdir(path) == False):
            return [path]
        else:
            files = []
            for file in os.listdir(path):
                files += self.displayFiles(path+ os.pathsep + file)
            return files

    def findLocal(self, privPub):
        #check if seen and if seen return -1 don't look in files
        seen = self.alreadySeen()
        if (seen == -1):
            return -1
        #query hasn't been seen so looks up query in public directory
        files = self.displayFiles("Public")
        if (privPub == "Private"):
            files += self.displayFiles("Private")
        #list of files that match query
        retFiles = []
        for file in files:
            if self.message in file:
                retFiles += [file]
        #if no files match criteria return 0 else return list of filenames
        if len(retFiles) == 0:
            return 0
        else:
            return retFiles

class fileQuery(query):

    def __init__(self, messageID, message):
        super().__init__(messageID, message)

    def findLocal(self, privPub):
        seen = self.alreadySeen()
        if (seen == -1):
            return -1
        #query hasn't been seen so looks up query in public directory
        files = self.displayFiles("Public")
        if (privPub == "Private"):
            files += self.displayFiles("Private")
        #list of files that match query
        retFiles = []
        for file in files:
            if self.message in file:
                retFiles += [file]
        #if no files match criteria return 0 else return list of filenames
        if len(retFiles) == 0:
            return 0
        else:
            return retFiles

