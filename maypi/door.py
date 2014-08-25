def bell() :
	system("/usr/local/bin/gpio -p write 201 1")
	sleep(0.15)
	system("/usr/local/bin/gpio -p write 201 0")

def unlock(delay_sec):
	system("/usr/local/bin/gpio -p write 202 1")
	system("/usr/local/bin/gpio -p write 200 1")
	sleep(delay_sec)
	system("/usr/local/bin/gpio -p write 202 0")
	system("/usr/local/bin/gpio -p write 200 0")

def alarm(delay_sec):
	system("/usr/local/bin/gpio -p write 203 1")
	sleep(delay_sec)
	system("/usr/local/bin/gpio -p write 203 0")
