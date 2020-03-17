#!/bin/bash

mkdir Gpac
cd Gpac

sudo apt-get install build-essential pkg-config g++ git scons cmake yasm -y
sudo apt-get install zlib1g-dev libfreetype6-dev libjpeg62-dev libpng-dev libmad0-dev libfaad-dev libogg-dev libvorbis-dev libtheora-dev liba52-0.7.4-dev libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libavdevice-dev libxv-dev x11proto-video-dev libgl1-mesa-dev x11proto-gl-dev libxvidcore-dev libssl-dev libjack-dev libasound2-dev libpulse-dev libsdl2-dev dvb-apps mesa-utils -y

git clone https://github.com/gpac/gpac gpac_public
git clone https://github.com/gpac/deps_unix
cd deps_unix/
git submodule update --init --recursive --force --checkout
./build_all.sh linux
cd ../gpac_public
./configure
make
sudo make install
