from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mycms.views.home', name='home'),
    # url(r'^mycms/', include('mycms.foo.urls')),
	#url(r'^$', 'home.views.home', name='home'),
	url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
	url(r'^robots\.txt$', 'django.views.generic.simple.direct_to_template', {'template': 'robots.txt', 'mimetype': 'text/plain'}),
	url(r'^$','codes.views.list', name='codes_list'),

	url(r'^codes/', include('codes.urls')),
	url(r'^apps/', include('apps.urls')),
#url(r'^codes/$', 'codes.views.list', name='codes_list'),
#url(r'^codes/tag/(\d+)/$', 'codes.views.list', name='codes_taglist'),
#url(r'^codes/(\d+)/$', 'codes.views.code'),
#url(r'^codes/add_comment/(\d+)/$', 'codes.views.add_comment'),

	url(r'^about/$', 'about.views.about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
