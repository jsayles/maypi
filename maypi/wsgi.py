"""
WSGI config for maypi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import sys
sys.path.append('/home/maypi/webapp/maypi')
sys.path.append('/home/maypi/webapp/lib/python2.7/site-packages')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maypi.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
