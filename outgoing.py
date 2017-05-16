#!/usr/bin/python
import socket

out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = ""


def makeConnection(name,port):
  try:
    port = int(port)
  except:
    print 'bad port entry'

  try:
    out.connect(name,port)
    message = out.recv(1024)
    print message
  except:
    print 'could not connect'

def getMessage():
  return message
