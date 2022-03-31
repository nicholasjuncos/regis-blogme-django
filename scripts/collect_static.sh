#!/usr/bin/env bash
source /home/ubuntu/env/bin/activate
cd /home/ubuntu/website
sudo mkdir /home/ubuntu/website/staticfiles
sudo chmod -R 777 /home/ubuntu/website/staticfiles
./manage.py collectstatic