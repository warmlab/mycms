from django.conf.urls import patterns, url

urlpatterns = patterns('foods.views',
	url(r'^update$', 'update_all', name="update_all"),
	url(r'^get_food$', 'get_food', name="get_food"),
	url(r'^get_relation$', 'get_relation', name="get_relation"),
	url(r'^get_alias$', 'get_alias', name="get_alias"),
	url(r'^get_version$', 'get_version', name="get_version"),
)
