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
import logging
import door

logger = logging.getLogger(__name__)

@login_required
def home(request):
	if request.method == 'POST':
		action = request.POST.get("action")
		if action == 'Bell':
			door.bell()
		if action == 'Unlock':
			door.unlock()

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
		message = "FAIL"
		try:
			door_code = DoorCode.objects.get(code=code_entered)
			if door_code:
				log.code = door_code
				log.user = door_code.user
				if door_code.start < now:
					if not door_code.end or dore_code.end > now:
						delay_sec = int(settings.UNLOCK_DELAY)
						door.unlock(delay_sec)
						message = "UNLOCKED"
						log.success = True
			else:
				door.alarm(delay_sec=1)
				message = "ALARM"
		except:
			pass
		log.save()
	return HttpResponse("Unlocked", content_type="text/plain", status=200)

