# Create your views here.
from django.http import HttpResponse

import json

from foods.models import *

def get_update_data(version):
	v = Version.objects.get(current = True)

	if v.version <= version:
		return ""
		
	foods = Food.objects.filter(version__gt = version)
	relations = Relation.objects.filter(version__gt = version)
	alias = Alias.objects.filter(version__gt = version)

	dic = {"foods": [f for f in foods], "relations": [r for r in relations],
			"alias": [a for a in alias]}
	
	return json.dumps(dic, default=lambda o:o.__dict__)

def update_all(request):
	if request.method != 'GET':
		return HttpResponse(status = 405) # Method Not Allowed

	version = request.GET.get('version')
	try: version = int(version)
	except: return HttpResponse(status = 406) # Not Acceptable

	value = get_update_data(version)
	return HttpResponse(value, mimetype='application/json')

def get_food(request):
	if request.method != 'GET':
		return HttpResponse(status = 405) # Method Not Allowed

	version = request.GET.get('version')
	try: version = int(version)
	except: return HttpResponse(status = 406) # Not Acceptable

	pk = request.GET.get('food')
	try: pk = int(pk)
	except: return HttpResponse(status = 406) # Not Acceptable

	try:
		food = Food.objects.get(pk=pk)

		if food and food.version > version:
			return HttpResponse(food.to_json(), mimetype='application/json')
	except:
		pass

	return HttpResponse(status = 404)

def get_relation(request):
	if request.method != 'GET':
		return HttpResponse(status = 405) # Method Not Allowed

	version = request.GET.get('version')
	try: version = int(version)
	except: return HttpResponse(status = 406) # Not Acceptable

	pk = request.GET.get('relation')
	try: pk = int(pk)
	except: return HttpResponse(status = 406) # Not Acceptable

	try:
		relation = Relation.objects.get(pk=pk)

		if relation.version > version:
			return HttpResponse(relation.to_json(), mimetype='application/json')
	except:
		pass

	return HttpResponse(status = 404)

def get_alias(request):
	if request.method != 'GET':
		return HttpResponse(status = 405) # Method Not Allowed

	version = request.GET.get('version')
	try: version = int(version)
	except: return HttpResponse(status = 406) # Not Acceptable

	pk = request.GET.get('alias')
	try: pk = int(pk)
	except: return HttpResponse(status = 406) # Not Acceptable

	try:
		alias = Alias.objects.get(pk=pk)

		if alias.version > version:
			return HttpResponse(alias.to_json(), mimetype='application/json')
	except:
		pass

	return HttpResponse(status = 404)
