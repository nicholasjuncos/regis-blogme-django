##!/bin/bash
#sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable -y

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update -y
sudo apt-get install python3.9 -y

sudo apt install postgresql -y
sudo apt install nginx -y
sudo apt install supervisor -y
sudo apt install python3-pip -y
sudo apt install python3.9-distutils -y
sudo apt install virtualenv -y

sudo curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install nodejs -y


#sudo apt install gcc -y
#sudo apt install libffi-dev -y
#sudo apt install curl -y
#sudo apt install git -y
#sudo apt install build-essential -y
#sudo apt install python3-dev -y
#sudo apt install python3-setuptools -y
#sudo apt install python3-wheel -y
#sudo apt install python3-cffi -y
#sudo apt install libcairo2 -y
#sudo apt install libpango-1.0.0 -y
#sudo apt install libpangocairo-1.0-0 -y
#sudo apt install libgdk-pixbuf2.0-0 -y
#sudo apt install libffi-dev -y
#sudo apt install shared-mime-info -y
#sudo apt install libxslt1-dev -y
#sudo apt install gdal-bin -y
#sudo apt install libsasl2-dev -y
#sudo apt install python-dev -y
#sudo apt install libldap2-dev -y
#sudo apt install libssl-dev -y
#sudo apt install openssl -y
#sudo apt install libxml2 -y
## sudo apt install slapd -y
#sudo apt install ldap-utils -y
#sudo apt install libjpeg-turbo8-dev -y
#sudo apt install libgeos-dev -y
#sudo apt install libcurl3 -y
#sudo apt install cython -y
#sudo apt install graphviz -y

sudo apt update -y
sudo apt upgrade -y

sudo apt autoremove -y
