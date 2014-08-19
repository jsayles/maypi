from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from time import sleep
from os import system
import json

@login_required
def home(request):
   if request.method == 'POST':
      action = request.POST.get("action")
      if action == 'Alert':
         ding()
      if action == 'Unlock':
         unlock()

   return render(request, "home.html", {})


@csrf_exempt
def pincode(request):
    if request.method == 'POST':
        # pin = json.loads(request.body)["pin"]
        pin = request.POST.get("pin")
        if pin == "1234":
            unlock()
    return HttpResponse()

def ding() :
   system("/usr/local/bin/gpio -p write 201 1")
   sleep(0.15)
   system("/usr/local/bin/gpio -p write 201 0")

def unlock():
   system("/usr/local/bin/gpio -p write 202 1")
   system("/usr/local/bin/gpio -p write 203 1")
   system("/usr/local/bin/gpio -p write 200 1")
   sleep(5)
   system("/usr/local/bin/gpio -p write 203 0")
   system("/usr/local/bin/gpio -p write 202 0")
   system("/usr/local/bin/gpio -p write 200 0")
