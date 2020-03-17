FROM ubuntu:latest
MAINTAINER Asif

#Update the apt package manager
RUN apt update

#Install ffmpeg
RUN apt install -y ffmpeg

#update the apt-get package manager
RUN apt-get update -y

#Install kvazaar
RUN apt-get install git -y
RUN apt-get install automake -y
RUN apt-get install autoconf -y
RUN apt-get install libtool -y
RUN apt-get install m4 -y
RUN apt-get install build-essential -y
RUN apt-get install yasm -y
RUN git clone https://github.com/ultravideo/kvazaar.git
WORKDIR /kvazaar

RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install
RUN ldconfig

#Install FULL_GPAC

WORKDIR  /
RUN mkdir Gpac
WORKDIR /Gpac
RUN apt-get install build-essential pkg-config g++ git scons cmake yasm -y
RUN apt-get install zlib1g-dev libfreetype6-dev libjpeg62-dev libpng-dev libmad0-dev libfaad-dev libogg-dev libvorbis-dev libtheora-dev liba52-0.7.4-dev libavcodec-dev libavformat-dev libavutil-dev libswscale-dev libavdevice-dev libxv-dev x11proto-video-dev libgl1-mesa-dev x11proto-gl-dev libxvidcore-dev libssl-dev libjack-dev libasound2-dev libpulse-dev libsdl2-dev dvb-apps mesa-utils -y
RUN git clone https://github.com/gpac/gpac gpac_public
RUN git clone https://github.com/gpac/deps_unix
WORKDIR /Gpac/deps_unix/
RUN git submodule update --init --recursive --force --checkout
RUN ./build_all.sh linux
WORKDIR /Gpac/gpac_public
RUN ./configure
RUN make
RUN make install


#Make the mounting folder
RUN mkdir -p /VideoProcessing

#Change directory to mounted folder
WORKDIR /VideoProcessing
