#!/usr/bin/python
import socket
import thread

me = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def init():
  host = socket.gethostbyname(socket.gethostname())
  print host
  port = 1085
  me.bind((host,port))
  me.listen(5)
  thread.start_new_thread(serve,(1,))

def myName():
  return socket.gethostbyname(socket.gethostname())

def myPort():
  return "1085"

def serve(a):
  while a:
    client, address = me.accept()
    print client
    print address 
    client.send('Hello')
    client.close()
