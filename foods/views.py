# Create your views here.
from django.http import HttpResponse

import json

def update(request):
	if request.method != 'GET':
		return HttpResponse(status = 405) # Method Not Allowed
	version = request.GET.get('version')

	try: version = int(version)
	except: return HttpResponse(status = 406) # Not Acceptable

	value = get_update_data(version)
	return HttpResponse(value, mimetype='application/json')


def get_update_data(version):
	return '{"a":5}'
