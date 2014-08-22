from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from maypi.models import *
from time import sleep
from os import system
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
	if request.method == 'POST':
		action = request.POST.get("action")
		if action == 'Alert':
			ding()
		if action == 'Unlock':
			unlock()

	return render(request, "home.html", {})

@login_required
def test_code(request):
	return render(request, "test_code.html", {})

@csrf_exempt
def pincode(request):
	if request.method == 'POST':
		# pin = json.loads(request.body)["pin"]
		code_entered = request.POST.get("pin")
		logger.debug("code_entered: %s" % code_entered)
		log = CodeLog(code_entered=code_entered, success=False)
		now = timezone.localtime(timezone.now())
		try:
			door_code = DoorCode.objects.get(code=code_entered)
			if door_code:
				log.code = door_code
				log.user = door_code.user
				if door_code.start < now:
					if not door_code.end or dore_code.end > now:
						delay_sec = int(settings.UNLOCK_DELAY)
						unlock(delay_sec)
						log.success = True
		except:
			pass
		log.save()
	return HttpResponse()

def ding() :
	system("/usr/local/bin/gpio -p write 201 1")
	sleep(0.15)
	system("/usr/local/bin/gpio -p write 201 0")

def unlock(delay_sec):
	system("/usr/local/bin/gpio -p write 202 1")
	system("/usr/local/bin/gpio -p write 200 1")
	sleep(delay_sec)
	system("/usr/local/bin/gpio -p write 202 0")
	system("/usr/local/bin/gpio -p write 200 0")
