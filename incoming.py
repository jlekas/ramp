#!/usr/bin/python
import socket
import thread
import ramp_db

def init(server):
  if server != None:
    server.close()
    server = None
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) 
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  myIP = get_address()
  port = 1085
  server.bind((myIP,port))
  server.listen(5)
  thread.start_new_thread(findClients,(1,server))

def myName():
  return get_address() 

def myPort():
  return "1085"

def findClients(a, server):
  while a:
    user, address = server.accept()
    #print "Connection from %s %s" % (user, address)
    thread.start_new_thread(recClient, (user, address))
  server.close()

def recClient(name, address):
  while 1:
    try:
      message = name.recv(1024) #magic number size of rec message
      if not message:
        break
      print message
      m = ramp_db.chatMessage(address[0], message)
      m.add_db()
    except Exception, e:
      print(e)
      break
  name.close()


def get_address(): #this function was taken from user wmcbrine on
#ubuntuforums.org as a fix for gethostbyname issues on linux machines
    try:
        address = socket.gethostbyname(socket.gethostname())
        # On my system, this always gives me 127.0.0.1. Hence...
    except:
        address = ''
    if not address or address.startswith('127.'):
        # ...the hard way.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('4.2.2.1', 0))
        address = s.getsockname()[0]
        s.close()
    return address
