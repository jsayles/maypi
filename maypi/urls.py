import time
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
	url(r'^cache\.manifest$', lambda r: HttpResponse(get_manifest(), mimetype="text/plain")),

	url(r'^$', 'maypi.views.home', name='home'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^pincode/', 'maypi.views.pincode')
)

def get_manifest():
	return "CACHE MANIFEST\n#Time: %s\nCACHE:\nFALLBACK:\nNETWORK:\n*" % time.time()
