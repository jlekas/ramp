#!/usr/bin/python
import socket
import thread

me = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def init():
  host = get_address()
  print host
  port = 1085
  me.bind((host,port))
  me.listen(5)
  thread.start_new_thread(serve,(1,))

def myName():
  return get_address() 

def myPort():
  return "1085"

def serve(a):
  while a:
    client, address = me.accept()
    client.send('Hello')
    client.close()


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
