#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message = "hello sending test"


def makeConnection(name,port):
  try:
    port = int(port)
  except:
    print 'bad port entry'

  addr = (name,port)
  buffer = 1024

#  try:
  s.connect(addr)
  s.send(mesesage)
  received = s.recv(buffer)
  s.close()

  
'''  except:
    print 'could not connect'
'''

def getMessage():
  return message
