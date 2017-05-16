#!/usr/bin/python
import socket

me = socket.socket()

def init():
  host = socket.gethostname()
  port = 1085
  me.bind((host,port))
  me.listen(5)
  print host

def myName():
  print socket.gethostname()
  return socket.gethostname()

def myPort():
  return "1085"

def serve():
  while 1:
    client, address = me.accept()
    client.send('Hello')
    client.close()
