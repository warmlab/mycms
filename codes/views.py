# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse

from codes.models import *

PAGE_NUM = 5

def category(request, slug):
	categories = Category.objects.all()
	category = get_object_or_404(Category, slug=slug)
	codes = Code.objects.filter(category=category).order_by('-modified')
	heading = "Category: %s" % category.label

	paginator = Paginator(codes, PAGE_NUM)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	code_list=codes.object_list
	return render_to_response("codes/list.html", locals())

def list(request):
	categories = Category.objects.all()

	codes = Code.objects.all().order_by('-modified')
	paginator = Paginator(codes, PAGE_NUM)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	return render_to_response("codes/list.html", dict(categories=categories, codes=codes, user=request.user, code_list=codes.object_list))

def code(request, slug):
	categories = Category.objects.all()
	code = Code.objects.get(slug=slug)
	d = dict(categories=categories, code=code, user=request.user)
	d.update(csrf(request))
	return render_to_response("codes/code.html", d)

def search(request):
	categories = Category.objects.all()
	if 'q' in request.GET:
		term = request.GET['q']
		code_list = Code.objects.filter(Q(title__contains=term)
					| Q(body__contains=term))
		heading = 'Search results'
		return render_to_response("codes/list.html", locals())
