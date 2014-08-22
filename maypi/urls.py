import time
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
	url(r'^cache\.manifest$', lambda r: HttpResponse(get_manifest(), mimetype="text/plain")),

	url(r'^$', 'maypi.views.home', name='home'),
	url(r'^test_code/', 'maypi.views.test_code', name='test_code'),
	url(r'^pincode/', 'maypi.views.pincode', name='pincode'),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
)

def get_manifest():
	return "CACHE MANIFEST\n#Time: %s\nCACHE:\nFALLBACK:\nNETWORK:\n*" % time.time()
