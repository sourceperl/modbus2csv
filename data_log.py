#!/usr/bin/env python

import csv
import time
import schedule
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient

# set global
regs = [None] * 5
clone_regs = []
cycle_count = 0
good_count = 0
error_count = 0
regs_lock = Lock()

# modbus polling thread
def polling_thd():
    global regs, cycle_count, good_count, error_count
    c = ModbusClient(host='localhost', auto_open=True)
    # polling loop
    while True:
        # do modbus reading on socket
        reg_list = c.read_holding_registers(0, len(regs))
        # if read is ok, store result in regs (with thread lock synchronization)
        with regs_lock:
            cycle_count += 1
            if reg_list:
                regs = list(reg_list)
                good_count += 1
            else:
                regs = [None] * 5
                error_count += 1
        # 1.0s before next polling
        time.sleep(1.0)

# CSV job
def csv_job():
    # format data
    str_datetime = time.strftime('%Y-%m-%d %H:%M:%S %z')
    with regs_lock:
        a_stats = [cycle_count, good_count, error_count]
        a_data = list(regs)
    # add to CSV
    with open('/var/ramdisk/data.csv', 'a') as f:
        w = csv.writer(f)
        w.writerow([str_datetime] + a_stats + a_data)

# main task
if __name__ == '__main__':
    # start polling thread
    tp = Thread(target=polling_thd)
    # set daemon: polling thread will exit if main thread exit
    tp.daemon = True
    tp.start()
    # setup jobs
    schedule.every(2).seconds.do(csv_job)
    # main loop
    while True:
        schedule.run_pending()
        time.sleep(.1)
