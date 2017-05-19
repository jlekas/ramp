#!/bin/bash

#this is if the computer is ubuntu check python and packages installed
if [ "$(uname)" == "Linux" ]; then
  #script to install python2.7.13 which is python version of program
  sudo apt-get install build-essential checkinstall
  sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
  version=2.7.13
  cd ~/Downloads
  wget https://www.python.org/ftp/python/$version/Python-$version.tgz
  tar -xvf Python-$version.tgz
  cd Python-$version
  sudo ./configure
  sudo make altinstall
  # at this point python 2.7.13 is installed and can be used
  sudo apt-get install python-tk
  #install or make sure sqlite3 is installed
  sudo apt-get install sqlite3
  sudo pip install pygame
elif [ "$(uname)" == "Darwin" ]; then
  #if the computer is a mac check that python 2.7.13 and various
  #packages are installed in order to run application
  echo "hello"
