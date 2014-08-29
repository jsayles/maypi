from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django import forms

from maypi.models import DoorCode, CodeLog
from maypi.forms import UserForm, DoorCodeForm
from maypi import door

from time import sleep
import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
	logs = CodeLog.objects.all().order_by('-created')[:25]
	return render(request, "home.html", {'logs':logs})

@user_passes_test(lambda u: u.is_staff)
def users(request):
	codes = DoorCode.objects.all().order_by("user")
	
	user_form = UserForm()
	code_form = DoorCodeForm()
	
	if request.method == 'POST':
		action = request.POST.get('action')
		if action == "add_user":
			form = UserForm(request.POST)
			try:
				if form.is_valid():
					form.save()
			except forms.ValidationError, e:
				messages.add_message(request, messages.ERROR, e.message)
		elif action == "add_code":
			form = DoorCodeForm(request.POST)
			try:
				if form.is_valid():
					form.save()
			except forms.ValidationError, e:
				messages.error(request, e.message)
		elif aciton == "expire":
			code_id = request.POST.get('code')
			door_code = DoorCode.objects.filter(id=code_id).first()
			if door_code:
				door_code.end = timezone.localtime(timezone.now())
				door_code.save()

	return render(request, "users.html", {"codes":codes, "user_form":user_form, "code_form":code_form})

@login_required
def test_code(request):
	return render(request, "test_code.html", {})

@login_required
def mobile(request):
	if request.method == 'POST':
		action = request.POST.get("action")
		action = action.lower()
		logger.debug("Action=%s" % action)
		if action == 'bell':
			door.bell()
		elif action == 'alarm':
			door.alarm()
		elif action == 'unlock':
			door.unlock()
	return render(request, "mobile.html", {})

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

