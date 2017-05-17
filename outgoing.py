#!/usr/bin/python

import errno
import socket



def makeConnection(name,port):
  try:
    port = int(port)
  except:
    print 'bad port entry'

  addr = (name,port)
  buffer = 1024

#  try:
  try:
    client.connect(addr)
  except socket.error, e:
    print e
    if e.errno == errno.EISCONN: 
      client.close()  
      print 'reseting client socket'
     # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      makeConnection(name, port)
    else:
      print e
      print 'didnt pick up error 56'


  
'''  except:
    print 'could not connect'
'''

def sendMessage(name,port,message):
    port = int(port)
    addr = (name,port)
    buffer = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client.connect(addr)
        client.send(message)
        client.close()
    except socket.error, e:
        print(e, "e", socket.error, "sock")
