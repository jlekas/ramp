#!/usr/bin/python
import socket

def makeConnection(name,port):
  s = socket.socket()

  try:
    s.connect(name,port)
    connections[name] = s
  except:
    print 'could not connect'

  
