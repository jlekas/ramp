#!/usr/bin/python

import errno
import socket

import pygame
import sys
import pygame.camera
from pygame.locals import *
from PIL import *
import cache

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
  pygame.init()
  pygame.camera.init()
  size = (640, 480)
  screen = pygame.display.set_mode(size)
  camList = pygame.camera.list_cameras()
  if (not camList):
    print("no cams")
  cam = pygame.camera.Camera(camList[0], size, "RGB")
  cam.start()
  port = int(port)
  addr = (name, port)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.connect(addr)
  while True:
    img = cam.get_image()
    data = cam.get_raw()
    client.send("v")
    client.send(data)
    pygame.display.update()
  client.close()
