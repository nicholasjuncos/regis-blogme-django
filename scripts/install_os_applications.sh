##!/bin/bash
sudo apt update -y

sudo apt install postgresql -y
sudo apt install nginx -y
sudo apt install supervisor -y
sudo apt install python3-pip -y
sudo apt install virtualenv -y

sudo apt update -y
sudo apt upgrade -y

sudo apt autoremove -y
