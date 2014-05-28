#!/bin/bash

# Updates
apt-get -y update 
apt-get -y upgrade

# CTF-Platform Dependencies
apt-get -y install python3-pip
apt-get -y install nginx
apt-get -y install mongodb
apt-get -y install gunicorn
apt-get -y install git
apt-get install libzmq-dev
pip3 install Flask
pip3 install py3k-bcrypt
pip3 install pymongo
pip3 install pyzmq

# Configure Nginx
cp /vagrant/config/ctf.nginx /etc/nginx/sites-enabled/ctf
rm /etc/nginx/sites-enabled/default
service nginx restart
