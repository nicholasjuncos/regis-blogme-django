#!/usr/bin/env bash
sudo mkdir /home/ubuntu/website/staticfiles
sudo chmod -R 777 /home/ubuntu/website/staticfiles
./manage.py collectstatic