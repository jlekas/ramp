#!/usr/bin/python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def makeConnection(name,port):
  client.close()



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
    print "error: %s" % (e)

  
'''  except:
    print 'could not connect'
'''

def sendMessage(message):
    try:
        client.send(message)
    except:
        print("oops")
