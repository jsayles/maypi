#!/usr/bin/env python
import sys
import time
import pigpio
import wiegand
import requests
from datetime import datetime

DATA0_PIN = 14
DATA1_PIN = 15

ESC=10
ENT=11

TARGET="http://localhost/pincode/"

def log(message, newline=True):
	timestamp = datetime.now()
	sys.stdout.write("%s: %s" % (timestamp, message))
	if newline:
		sys.stdout.write("\n")

class Controller:
	index = 0
	keys = []

	def callback(self, bits, value):
		#sys.stdout.write("key pressed: %s\n" % value)
		if value == ESC:
			self.reset()
		elif value == ENT:
			self.submit()
			self.reset()
		else:
			self.save_key(value)

	def save_key(self, key):
		self.keys.append(key)
		self.index = self.index + 1

	def reset(self):
		self.index = 0
		self.keys = []

	def submit(self):
		code = ""
		for k in self.keys:
			code = code + str(k)
		log("code entered: %s" % code)
		payload = {"pin" : code}
		r = requests.post(TARGET, data=payload)
		log("Posting pin returned: %s" % r.text)

	def start(self, d0pin, d1pin):
		log("Starting wiegand daemon...", newline=False)
		self.pi = pigpio.pi()
		self.w = wiegand.decoder(self.pi, d0pin, d1pin, self.callback)
		log("done!")

	def stop(self):
		log("Stopping wiegand daemon...", newline=False)
		self.w.cancel()
		self.pi.stop()
		log("done!")

if __name__ == "__main__":
	# Start our controller
	controller = Controller()
	controller.start(DATA0_PIN, DATA1_PIN)

	try:
		while True:
			time.sleep(1)
			sys.stdout.flush()
	except (KeyboardInterrupt, SystemExit):
		controller.stop()
		sys.exit(0)
