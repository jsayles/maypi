#!/usr/bin/env python
import time
import pigpio
import wiegand
import sys
import requests

DATA0_PIN = 14
DATA1_PIN = 15

ESC=10
ENT=11

TARGET="http://localhost/pincode/"

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
		sys.stdout.write("code entered: %s\n" % code)
		payload = {"pin" : code}
		r = requests.post(TARGET, data=payload)
		sys.stdout.write("Posting pin returned: %s" % r.text)

	def start(self, d0pin, d1pin):
		sys.stdout.write("Starting wiegand daemon...")
		self.pi = pigpio.pi()
		self.w = wiegand.decoder(self.pi, d0pin, d1pin, self.callback)
		sys.stdout.write("done!\n")

	def stop(self):
		sys.stdout.write("Stopping wiegand daemon...")
		self.w.cancel()
		self.pi.stop()
		sys.stdout.write("done!\n")

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
