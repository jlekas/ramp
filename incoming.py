#!/usr/bin/python
from Tkinter import *
import socket
import thread
import ramp_db

import cache
import pygame
import sys
import pygame.camera
from pygame.locals import *
import outgoing


#added messages to functions
def init(server, frame, messages):
  if server != None:
    server.close()
    server = None
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) 
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  myIP = get_address()
  port = 1085
  server.bind((myIP,port))
  server.listen(5)
  thread.start_new_thread(findClients,(1,server, frame,messages))

def myName():
  print get_address()
  return get_address() 

def myPort():
  return "1085"

def findClients(a, server, frame,messages):
  while a:
    user, address = server.accept()
    #print "Connection from %s %s" % (user, address)
    thread.start_new_thread(recClient, (user, address, frame,messages))
  server.close()

def recClient(name, address, frame,messages):
  try: 
    tag = name.recv(1)
    if(tag == "/"):
      fileReceive(name, address, "pupper.jpg")
      print "receiving FILE"
      return
    if(tag=="v"):
      print"getting video 1"
      videoReceive(name, address)
      print"getting video"
      return
    if(tag=="f"):
      print("looking for file")
      fileRequest(name, address)
      return
  except:
    print "couldnt receive first bit"
  while 1:
    try:
      message = name.recv(1024) #magic number size of rec message
      if not message:
        break
      # print "MESSAGE :  %s" % message
      # print 'name = %s active user = %s' % (address[0], frame.activeUser)


      if address[0] not in messages:
        print 'new messages from: %s' % address[0]
        messages[address[0]] = []

      messages[address[0]].append("Peer: %s\n" % message)

      frame.chatBox.config(state=NORMAL)


      print messages





      frame.chatBox.delete(1.0, END)

      for m in messages[frame.activeUser]:
        frame.chatBox.insert(END, m)

      # frame.chatBox.insert(END, "Peer: %s\n" % message)
      frame.chatBox.config(state=DISABLED)
      m = ramp_db.chatMessage(address[0], "127.0.0.1", message)
      #print(ramp_db.getChats(address[0], "127.0.0.1"))
      m.add_db()
    except Exception, e:
      print(e)
      break
  name.close()


def fileRequest(connect, address, fileStr):
  buffer = 1024
  while 1:
    data = connect.recv(buffer)
    if not data:
      break
  if ":" not in data:
    connect.close()
    print("sorry error in file request")
  d = data.split(":")
  if (d[3] == "general"):
    q = cache.query(d[0], d[1], d[2])
  elif (d[3] == "specific"):
    q = cache.fileQuery(d[0], d[1], d[2])
  if (q.alreadySeen != -1):
    send = q.findLocal
    if (send == 0):
      print("no files")
  for f in send:
    outgoing.sendFile(connect, f)
  connect.close()


def videoReceive(connect, address):
  print("start of videoReceive")
  size = (640, 480)
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("p2p video chat")
  buffer = 2048
  while 1:
    #check if pygame stuff shows quit
    vid = []
    while 1:
      data = connect.recv(buffer)
      if not data:
        break
      else:
        vid.append(data)
    d = ''.join(vid)
    img = pygame.image.fromstring(d, size, "RGB")
    screen.blit(img, (0,0))
    pygame.display.update()

def fileReceive(connect, address, fileStr):
  buffer = 1024
  newFile = open(fileStr, 'w')
  while 1:
    data = connect.recv(buffer)
    if not data:
      break
    #print(data)
    newFile.write(data)
  newFile.close()
  connect.close()

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
