#!/usr/bin/env python
import os
import csv
from dateutil import parser

DATA_FILE = '/media/ramdisk/data.csv' 
BAK_FILE = '/media/ramdisk/hourly.csv'
ARCH_DIR = '/home/pi/'

# move file
os.rename(DATA_FILE, BAK_FILE)

# decode file
# parse CSV and build archive dict {filename: [l1, l2...]}
a_files = {}
with open(BAK_FILE, 'rb') as r_f:
    d_data = csv.reader(r_f)
    for d in d_data:
        dt = parser.parse(d[0])
        id_csv = '{:%Y%m%d}'.format(dt)
        a_files.setdefault(id_csv, []).append(d)

# store archive to disk
for id_file in a_files:
    # filename with path
    csv_file = ARCH_DIR+id_file+'.csv'
    # build daily CSV file 
    with open(csv_file, 'ab') as w_f:
        writer = csv.writer(w_f)
        writer.writerows(a_files[id_file])

# delete file
os.remove(BAK_FILE)
