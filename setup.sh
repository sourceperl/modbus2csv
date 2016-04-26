#!/bin/bash

# create a 32M RAM disk (file system in RAM: tmpfs) in /var/ramdisk/
sudo mkdir -p /var/ramdisk/
# add line for mount RAMDISK at system startup if not already exist
LINE='tmpfs           /var/ramdisk    tmpfs   defaults,size=32M 0       0'
FILE='/etc/fstab'
sudo grep -q "$LINE" "$FILE" || echo "$LINE" | sudo tee -a "$FILE"

# install python libs
sudo pip install -r requirements.txt

# copy program
sudo cp data_log.py /usr/local/bin/

# need reboot
echo 'Please reboot for changes take effect !'

