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

class Controller:
	def callback(self, bits, value):
		if value == ESC:
			log("<ESC>")
		elif value == ENT:
			log("<ENT>")
		else:
			log("key=%d" % value)

	def start(self, d0pin, d1pin):
		log("Starting wiegand daemon...")
		self.pi = pigpio.pi()
		self.w = wiegand.decoder(self.pi, d0pin, d1pin, self.callback)

	def stop(self):
		log("Stopping wiegand daemon...")
		self.w.cancel()
		self.pi.stop()

if __name__ == "__main__":
	# Start our controller
	controller = Controller()
	controller.start(DATA0_PIN, DATA1_PIN)

	try:
		while True:
			time.sleep(1)
	except (KeyboardInterrupt, SystemExit):
		controller.stop()
		sys.exit(0)


