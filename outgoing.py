#!/usr/bin/python
import socket

out = socket.socket()
message = ""


def makeConnection(name,port):
  try:
    port = int(port)
    out.connect(name,port)
    message = out.recv(1024)
    print message
  except:
    print 'could not connect'

def getMessage():
  return message
