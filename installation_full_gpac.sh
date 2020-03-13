#!/bin/bash

mkdir Gpac
cd Gpac
git clone https://github.com/gpac/gpac gpac_public
git clone https://github.com/gpac/deps_unix
cd deps_unix/
git submodule update --init --recursive --force --checkout
./build_all.sh linux
cd ../gpac_public
./configure
make
sudo make install
