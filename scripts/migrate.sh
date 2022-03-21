#!/usr/bin/env bash
source /home/ubuntu/env/bin/activate
cd /home/ubuntu/website/backend
./manage.py migrate --no-input
cd /home/ubuntu/website