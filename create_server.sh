#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip nginx mongodb gunicorn tmux socat
sudo ln -s /home/ubuntu/xgovctf/config/ctf.nginx /etc/nginx/sites-enabled/
sudo ln -s /home/ubuntu/xgovctf/config/htpasswd /etc/nginx/
sudo mkdir -p /srv/http/ctf
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx reload

cd xgovctf/
pip3 install -r api/requirements.txt
pip3 install -r flaskweb/requirements.txt
cd api/
python3 api_manager.py -v problems load ../example_problems/ graders/ ../problem_static/
python3 api_manager.py autogen build 100

sudo ln -s /home/ubuntu/xgovctf/problem_static/ /srv/http/ctf/problem-static

tmux new-session -s picoapi -d "cd /home/ubuntu/xgovctf/api && python3 run.py -d"
tmux new-session -s flaskweb -d "cd /home/ubuntu/xgovctf/flaskweb && python3 run.py -d"

cd ../example_problems/buffer_overflow/
make
make host
