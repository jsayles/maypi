from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'maypi.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/docs/', include('django.contrib.admindocs.urls')),
)
