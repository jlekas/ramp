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
import datetime


def init(server, frame, messages): #called once at start, always uses port 1085
  if server != None:
    server.close()
    server = None
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) 
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  myIP = get_address()
  port = 1085
  server.bind((myIP,port))
  server.listen(5) #listens for up to 5 incoming connections at once
  thread.start_new_thread(findClients,(server, frame,messages)) 
  #find clients runs in new thread so main thread finishes first init in main

def myName():
  print get_address()
  return get_address() 

def myPort():
  return "1085"

def findClients(server, frame,messages):
  while 1:
    user, address = server.accept()
    #print "Connection from %s %s" % (user, address)
    thread.start_new_thread(recClient, (user, address, frame,messages))
    #if a connection is found, it will handle the receiving in a new thread
    #to allow for more connections to be found in parallel 
  server.close()

def recClient(name, address, frame,messages):
  tag = name.recv(1) #we use the first char of the string as an identifier
  if(tag == "j"): # / = file receive 
    fileReceive(name, address, "Downloads/%s.jpg" % str(datetime.datetime.now()))
    return
  if(tag == "4"): # / = file receive 
    fileReceive(name, address, "Downloads/%s.mp4" % str(datetime.datetime.now()))
    return
  if(tag == "3"): # / = file receive 
    fileReceive(name, address, "Downloads/%s.mp3" % str(datetime.datetime.now()))
    return
  if(tag == "p"): # / = file receive 
    fileReceive(name, address, "Downloads/%s.pdf" % str(datetime.datetime.now()))
    return
  if(tag=="v"): # v = video
    videoReceive(name, address)
    return
  if(tag=="f"): # f = file request
    fileRequest(name, address, frame)
    return
  while 1: 
    try:
      message = name.recv(1024) #magic number size of rec message
      if not message:
        break
      if address[0] not in messages: 
        #case where someone you are not connected to is messaging you
        print 'new messages from: %s' % address[0]
        messages[address[0]] = []
      messages[address[0]].append("Peer: %s\n" % message)
      frame.chatBox.config(state=NORMAL)
      print "messages", messages
      frame.chatBox.delete(1.0, END)
      for m in messages[frame.activeUser]:
        frame.chatBox.insert(END, m)
      frame.chatBox.config(state=DISABLED)
      m = ramp_db.chatMessage(address[0], "127.0.0.1", message)
      m.add_db()
    except Exception, e:
      print(e)
      break
  name.close()

def fileRequest(connect, address, frame): 
  #receives a lookup and sends back file to peer of result from query
  buffer = 1024
  port = 1085
  data = []
  while 1:
    x = connect.recv(buffer)
    if not x:
      break
    else:
      data.append(x)
  d = ''.join(data)
  d = d.split(":") 
  if (d[3] == "general"):
    q = cache.query(d[0], d[1], d[2])
  elif (d[3] == "specific"):
    q = cache.fileQuery(d[0], d[1], d[2]) #query database differently for g/s
  if (q.alreadySeen() == -1):
    send = q.findLocal()
    if (send == 0):
      frame.chatBox.config(state=NORMAL)
      frame.chatBox.insert(END,"Could not find File\n")
      frame.chatBox.config(state=DISABLED) 
  for f in send:
    #can send multiple files at once if multiple results
    thread.start_new_thread(outgoing.sendFile, (frame.activeUser, port, f))
    frame.chatBox.config(state=NORMAL)
    frame.chatBox.insert(END,"File Sent\n")
    frame.chatBox.config(state=DISABLED)  
  connect.close()


def videoReceive(connect, address):
  size = (640, 480) #default size
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("p2p video chat")
  buffer = 2048
  #buffer so data recv isn't too large
  while 1:
    vid = []
    #appended with incoming data
    while 1:
      data = connect.recv(buffer)
      if not data:
        break
      else:
        vid.append(data)
    d = ''.join(vid)
    img = pygame.image.fromstring(d, size, "RGB")
    #displays the video chat in pygame window
    screen.blit(img, (0,0))
    pygame.display.update()
      #updates pygame display

def fileReceive(connect, address, fileStr): 
  #receives and writes the file with name in fileStr
  buffer = 1024
  print fileStr
  newFile = open(fileStr, 'w')
  while 1:
    data = connect.recv(buffer)
    if not data:
      break
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
