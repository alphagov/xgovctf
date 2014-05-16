#!/bin/bash

#updates and package installation

echo root:root|chpasswd

sudo apt-get -y update 
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
sudo apt-get -y install nginx
sudo apt-get -y install mongodb
sudo apt-get -y install gunicorn
sudo apt-get -y install git
sudo apt-get install libzmq-dev

#extra packages
sudo pip3 install Flask
sudo pip3 install py3k-bcrypt
sudo pip3 install pymongo
sudo pip3 install pyzmq

#configure nginx

