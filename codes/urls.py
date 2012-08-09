from django.conf.urls import patterns, include, url
from codes.models import Code

info_dict = { 'queryset': Code.objects.all(), 'template_object_name': 'code', 'template_name': 'codes/list.html' }

urlpatterns = patterns('django.views.generic.list_detail',
	url(r'^(?P<slug>[-\w]+)/$', 'object_detail', info_dict, name='code_content'),
	url(r'^$', 'object_list', info_dict, name='code_list'),
)

urlpatterns = patterns('codes.views',
	url(r'^$', 'list', name="code_list"),
	url(r'^category/(?P<slug>[-\w]+)/$', 'category', name='codes_category'),
	url(r'^search/$', 'search', name='codes_search'),
	url(r'^comment/(?P<slug>[-\w]+)/$', 'comment', name="code_comment"),
	url(r'^(?P<slug>[-\w]+)/$', 'code', name="code_content"),
)
