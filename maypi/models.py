from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DoorCode(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	code = models.CharField(max_length=16, unique=True, db_index=True)
	user = models.ForeignKey(User, null=True, blank=True)
	start = models.DateTimeField(null=False, default=datetime.now)
	end = models.DateTimeField(null=True, blank=True)

class CodeLog(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	code_entered = models.CharField(max_length=100)
	code = models.ForeignKey(DoorCode, null=True, blank=True)
	user = models.ForeignKey(User, null=True, blank=True)
	success = models.BooleanField(default=False)
