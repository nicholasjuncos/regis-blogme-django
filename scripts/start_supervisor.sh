#!/usr/bin/env bash
sudo supervisord
sudo supervisorctl reload
sudo supervisorctl restart website
sudo supervisorctl restart frontend