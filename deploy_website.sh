#! /bin/bash

echo "Cloning repo..."
git clone git@github.com:krulys/IbreW.git

echo "Copying files to /var/www/html..."
sudo cp IbreW/source/server/website/ /var/www/html

echo"Removing folder..."
sudo rm -r IbreW
