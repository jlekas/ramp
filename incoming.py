#!/usr/bin/python
from Tkinter import *
import socket
import thread
import ramp_db

import cache
from PIL import Image
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
      print "MESSAGE :  %s" % message
      frame.chatbox.insert(END, "Peer: %s" % message)

      messages[frame.activeUser].append("Peer: %s" % message)

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
  print("start of func")
  size = (480, 320)
  pygame.init()
  pygame.camera.init()
  print("stuff")
  screen = pygame.display.set_mode(size, 0)
  pygame.display.set_caption("p2p video chat")
  buffer = 1024000
  timer = 0
  prevImg = ""
  img = ""
  while 1:
    print("to loop")
    #check if pygame stuff shows quit
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        pygame.quit()
    print("before receive")
    data = connect.recv(buffer)
    print("after data,"+data)
    if not data:
      break
    try:
      img = pygame.image.fromString(useData, size, "RGB")
      prevImg = img
      img = Image.fromString("RGB", size, data)
      img = img.resize(size)
      img = pygame.image.frombuffer(img.tostring(),size,"RGB")
    except:
      img = prevImg
    screen.blit(img, (0,0))
    pygame.display.update()
    pygame.display.flip()
    


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
