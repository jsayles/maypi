#!/usr/bin/env python
import time
import pigpio
import wiegand

DATA0_PIN = 14
DATA1_PIN = 15
LOGFILE = "/tmp/wiegand.log"

ESC=10
ENT=11

def log(msg):
	print(msg)
	with open(LOGFILE, "a") as f:
		f.write(time.ctime() + ": " + msg + "\n")

def callback(bits, value):
	log("key=%d" % value)

if __name__ == "__main__":
	log("Starting wiegand daemon...")
	pi = pigpio.pi()
	w = wiegand.decoder(pi, 14, 15, callback)

	try:
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		log("Stopping wiegand daemon...")
		w.cancel()
		pi.stop()

