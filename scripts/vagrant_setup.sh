#!/bin/bash

#updates and package installation

echo root:root|chpasswd

sudo apt-get -y update 
sudo apt-get -y upgrade
sudo apt-get -y install python3-pip
#sudo apt-get -y install unzip
sudo apt-get -y install nginx
#sudo apt-get -y install memcached
#sudo apt-get -y install libmemcached-dev
sudo apt-get -y install mongodb
#sudo apt-get -y install python-setuptools python-dev build-essential
sudo apt-get -y install gunicorn
sudo apt-get -y install git
sudo apt-get install libzmq-dev
#sudo apt-get -y install exiv2
#sudo apt-get -y install python-imaging
#sudo easy_install pip
#sudo pip install --upgrade virtualenv
#sudo pip install Flask
#sudo pip install watchdog -U
#sudo pip install argcomplete

#extra packages
#sudo pip install flask-pymongo
#sudo pip install py-bcrypt
#sudo pip install pylibmc
sudo pip3 install Flask
sudo pip3 install py3k-bcrypt
sudo pip3 install pymongo
sudo pip3 install pyzmq

#configure nginx

