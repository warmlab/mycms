from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mycms.views.home', name='home'),
    # url(r'^mycms/', include('mycms.foo.urls')),
	url(r'^$', 'home.views.home', name='home'),

	#url(r'^codes/$', include('codes.urls')),
	url(r'^codes/$', 'list', name='codes_list'),
	url(r'^codes/tag/(\d+)/$', 'list', name='codes_taglist'),
	url(r'^codes/(\d+)/$', 'code'),
	url(r'^codes/add_comment/(\d+)/$', 'add_comment'),

	url(r'^about/$', 'about.views.about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
