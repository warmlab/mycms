# Create your views here.
from django.http import HttpResponse

import json

from foods.models import *

def get_update_data(version):
	v = None
	try:
		v = Version.objects.get(current = True)
	except:
		pass

	if not v or v.version <= version:
		return ""

	foods = Food.objects.filter(version__gt = version)
	relations = Relation.objects.filter(version__gt = version)
	alias = []
	for f in foods:
		a = Alias.objects.filter(food = f)
		alias.extend([o for o in a])

	dic = {"foods": [f for f in foods], "relations": [r for r in relations],
			"alias": alias}
	
	return json.dumps(dic, default=lambda o:o.__dict__.pop('_state') and o.__dict__ or o.__dict__)

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

	food = request.GET.get('food')
	try: food = int(food)
	except: return HttpResponse(status = 406) # Not Acceptable

	food = Food.objects.get(pk=food)
	if not food:
		return HttpResponse(status = 404)

	try:
		alias = Alias.objects.filter(food=food)

		if alias:
			dic = {'alias': [a for a in alias]}
			return HttpResponse(json.dumps(dic, default=lambda o:o.__dict__.pop('_state') and o.__dict__ or o.__dict__), mimetype='application/json')
	except:
		pass

	return HttpResponse(status = 404)
