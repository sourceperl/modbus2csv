#!/bin/bash

# create a 32M RAM disk (file system in RAM: tmpfs) in /media/ramdisk/
sudo mkdir -p /media/ramdisk/
# add line for mount RAMDISK at system startup if not already exist
LINE='tmpfs           /media/ramdisk  tmpfs   defaults,size=32M 0       0'
FILE='/etc/fstab'
sudo grep -q "$LINE" "$FILE" || echo "$LINE" | sudo tee -a "$FILE"

# create dir for CSV archives
sudo mkdir -p /home/pi/csv_arch/

# install python libs
sudo pip install -r requirements.txt
# copy program
sudo cp data_log.py /usr/local/bin/

# need reboot
echo 'Please reboot for changes take effect !'

