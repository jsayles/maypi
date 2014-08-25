from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from maypi.models import DoorCode, CodeLog
from maypi import door
from time import sleep
import logging

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
		status = "FAIL"
		try:
			door_code = DoorCode.objects.filter(code=code_entered).first()
			if door_code:
				log.code = door_code
				log.user = door_code.user
				if door_code.start > now:
					status = "TOOEARLY"
				else:
					if door_code.end and door_code.end < now:
						status = "EXPIRED"
					else:
						delay_sec = int(settings.UNLOCK_DELAY)
						door.unlock(delay_sec)
						status = "UNLOCKED"
						log.success = True
			else:
				door.alarm(delay_sec=1)
				status = "ALARM"
		except:
			pass
		log.status = status
		log.save()
	return HttpResponse(status, content_type="text/plain")

