from django.conf.urls import patterns, include, url

urlpatterns = patterns('codes.views',
	url(r'^$', 'list', name='codes_list'),
	url(r'^tag/(\d+)/$', 'list', name='codes_taglist'),
	url(r'^(\d+)/$', 'code'),
	url(r'^add_comment/(\d+)/$', 'add_comment'),
)
