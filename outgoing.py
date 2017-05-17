#!/usr/bin/python

import errno
import socket

def sendMessage(name,port,message):
    port = int(port)
    addr = (name,port)
    buffer = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(addr)
    client.send(message)
    client.close()

def sendFile(name,port,file) #file is a string with a file extension
  port = int(port)
  addr = (name,port)
  buffer = 1024
  data = open(file).read()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)
  client.send(data)
  client.close()
