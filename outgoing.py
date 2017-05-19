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
  port = int(port)
  addr = (name,port)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)
  client.send("f")
  data = q.messageID + ":" + q.message + ":" + q.privPub + ":" + q.searchType
  client.send(data)
  client.close()

def sendFile(client,fileStr): #file is a string with a file extension
  data = open(fileStr).read()
  client.send("/")
  client.send(data)

def sendPing(name):
  addr = (name,1085)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)  
  client.send("~")
  client.close()

def sendVideo(name,port):
  port = int(port)
  addr = (name, port)
  
  pygame.init()
  pygame.camera.init()
  size = (320, 240)
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
