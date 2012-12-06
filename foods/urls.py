from django.conf.urls import patterns, url

urlpatterns = patterns('foods.views',
	url(r'^update$', 'update', name="update"),
)
