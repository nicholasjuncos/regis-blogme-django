#!/usr/bin/env bash
source /home/ubuntu/env/bin/activate
cd /home/ubuntu/website
./manage.py migrate --no-input
