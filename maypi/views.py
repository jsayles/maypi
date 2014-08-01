from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from time import sleep
from os import system

def home(request):
   if request.method == 'POST':
      action = request.POST.get("action")
      if action == 'Ding':
         ding()
      if action == 'Unlock':
         unlock()

   return render(request, "home.html", {})

def ding() :
   system("/usr/local/bin/gpio -p write 201 1")
   sleep(0.15)
   system("/usr/local/bin/gpio -p write 201 0")

def unlock():
   system("/usr/local/bin/gpio -p write 200 1")
   sleep(5)
   system("/usr/local/bin/gpio -p write 200 0")

