#!/bin/bash

sudo apt-get update -y
sudo apt-get install automake -y
sudo apt-get install autoconf -y
sudo apt-get install libtool -y
sudo apt-get install m4 -y
sudo apt-get install yasm -y
sudo ldconfig
echo "Successfully installed Kvazaar - run Kvazaar --version for verifying the installation"
