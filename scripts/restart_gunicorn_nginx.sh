#!/bin/bash
sudo supervisorctl restart website
sudo supervisorctl restart frontend
sudo service nginx restart