#!/usr/bin/env python
# encoding: utf-8
"""
wiegand_daemon.py

Created by Jacob Sayles on 2014-08-03.
"""
import daemon
import time

DATA0_PIN = 14
DATA1_PIN = 15
LOGFILE = "/tmp/wiegand.log"

def log(msg):
	with open(LOGFILE, "a") as f:
		f.write(time.ctime() + ": " + msg + "\n")

def catch_keycodes():
	def callback(bits, value):
		log("key=" + value)

	log("Starting wiegand daemon...")
	pi = pigpio.pi()
	w = wiegand.decoder(pi, DATA0_PIN, DATA1_PIN, callback)
	while True:
		time.sleep(5)

	log("Stopping wiegand daemon...")
	w.cancel()
	pi.stop()

def run():
	with daemon.DaemonContext():
		catch_keycodes()

if __name__ == "__main__":
	run()
