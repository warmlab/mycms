from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mycms.views.home', name='home'),
    # url(r'^mycms/', include('mycms.foo.urls')),
	url(r'^$', 'home.views.home'),
	url(r'^codes/$', 'codes.views.list'),
	url(r'^codes/tag/(\d+)/$', 'codes.views.list'),
	url(r'^codes/(\d+)/$', 'codes.views.code'),
	url(r'^codes/add_comment/(\d+)/$', 'codes.views.add_comment'),

	url(r'^about/$', 'about.views.about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
