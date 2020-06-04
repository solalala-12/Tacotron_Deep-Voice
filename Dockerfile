# Using untu18:04  as base images
FROM ubuntu:18.04

WORKDIR /home/multi-speaker-tacotron

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y 
# RUN apt-get clean

# Install packages about python3
RUN apt-get install -y build-essential python3 python3-pip 
RUN apt-get upgrade python3 -y
RUN apt-get install git -y

# Install packages in Python
RUN pip3 install ffmpeg

# Install packages in Ubuntu
RUN apt-get install lsb-core -y
RUN apt-get install sudo -y 
RUN apt-get install ffmpeg -y

# 한글 설정
ENV LANG C.UTF-8 

RUN mkdir resources
# local / container
ADD resources/requirements.txt /home/multi-speaker-tacotron/resources
RUN pip3 install -r /home/multi-speaker-tacotron/resources/requirements.txt

