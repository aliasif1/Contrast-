#!/bin/bash

git clone https://github.com/ultravideo/kvazaar.git
cd kvazaar
sudo apt-get update -y
sudo apt-get install automake -y
sudo apt-get install autoconf -y
sudo apt-get install libtool -y
sudo apt-get install m4 -y
sudo apt-get install build-essential -y
sudo apt-get install yasm -y

./autogen.sh
./configure
make
sudo make install

sudo ldconfig
echo "Successfully installed Kvazaar - run Kvazaar --version for verifying the installation"
