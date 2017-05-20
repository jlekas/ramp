#!/usr/bin/python

import errno
import socket

import pygame
import sys
import pygame.camera
from pygame.locals import *
import cache
import time

def sendMessage(name,port,message): 
    #makes socket, sends "X" (tag for message), then sends message and closes
    port = int(port)
    addr = (name,port)
    buffer = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(addr)
    client.send("X") 
    client.send(message)
    client.close()


def sendFileRequest(name,port,q): #file is a string with a file extension
  #makes socket, sends "f" (tag for fRequest) then sends string to search and closes
  port = int(port)
  addr = (name,port)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)
  client.send("f")
  data = str(q.messageID) + ":" + q.message + ":" + q.privPub + ":" + q.searchType
  client.send(data)
  client.close()

def sendFile(name,port,fileStr): #file is a string with a file extension
  #makes socket, sends "/" (tag for sendfile) then sends file and closes
  port = int(port)
  addr = (name,port)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)
  if fileStr[-3:] == "jpg":
      client.send("j")
  if fileStr[-3:] == "mp4":
      client.send("4")
  if fileStr[-3:] == "mp3":
    client.send("3")
  if fileStr[-3:] == "pdf":
    client.send("p")
  data = open(fileStr).read()
  client.send(data)

def sendPing(name):
  #sends single char "~", acts as a ping to check if there is a connection
  addr = (name,1085)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)  
  client.send("~")
  client.close()

def sendVideo(name,port):
  #send "v" for video and then continues to stream webcam until stopped
  port = int(port)
  addr = (name, port)
  pygame.init()
  pygame.camera.init()
  size = (640, 480)
  camList = pygame.camera.list_cameras()
  screen = pygame.display.set_mode(size)
  if (not camList):
    print("no cams")
  cam = pygame.camera.Camera(camList[0], size)
  cam.start()
  
  while True:
    img = cam.get_image()
    data = pygame.image.tostring(img, "RGB")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(addr)
    client.send("v")
    client.send(data)
    client.close()
    time.sleep(0.05)
