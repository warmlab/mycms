from django.conf.urls import patterns, url

urlpatterns = patterns('apps.views',
	url(r'^$', 'list', name="app_list"),
	url(r'^(?P<slug>[-\w]+)/$', 'app', name="app_content"),
)
