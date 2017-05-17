#!/usr/bin/python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def makeConnection(name,port):
  try:
    port = int(port)
  except:
    print 'bad port entry'

  addr = (name,port)
  buffer = 1024

#  try:
  s.connect(addr)

  
'''  except:
    print 'could not connect'
'''

def sendMessage(message):
  client.send(message)
