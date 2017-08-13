#!/usr/bin/env python
# -*- coding:utf-8 -*-

import serial
import time
from observer import observer

RESPONSE_SIZE_MIN = 14

class watt_streamer(observer):
    def __init__(self, device_file, host, port, interval=1, baudrate=115200, threshold=10):
        super(watt_streamer, self).__init__("watt_checker", host, port, interval)
        self.serial = serial.Serial(device_file, baudrate=baudrate, timeout=0.1)
        self.threshold = threshold

    def _getvalue(self):
        # 適当な文字でよい
        self.serial.write("\n".encode("ascii"))
        while self.serial.in_waiting < RESPONSE_SIZE_MIN:
            time.sleep(0.01)
        val = float(self.serial.read(self.serial.in_waiting))
        if val < self.threshold:
            return 0
        return val

def main():
    w = watt_streamer("/dev/ttyACM0", "127.0.0.1", 6003)
    w.start()

if __name__=='__main__':
    main()