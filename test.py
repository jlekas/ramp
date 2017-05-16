#!/usr/bin/python  
#test
import sys
import socket
import thread

#socket for receiving 
recsock = socket.socket()    
myname = socket.gethostname()
recport = 1085
recsock.bind((myname, recport))  

s.listen(5)

print myname 

#socket for sending


recsock.listen()

while True:
   peer, addr = recsock.accept()
   print 'Got connection from', addr
   peer.send('Thank you for connecting')



   userin = raw_input()
   if(userin == 'connect')
     out = socket.socket()
     sendname = raw_input('hostname:')
     sendport = raw_input('port:')
     sendport = int(sendport)
     out.bind(sendname, sendport))
     thread.start_new_thread(

def main():

  



#if __name__ == '__main__':
#  main()
