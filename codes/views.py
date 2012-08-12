# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse

from codes.models import *

import logging
logger = logging.getLogger('mycms.debug')

def category(request, slug):
	categories = Category.objects.all()
	category = get_object_or_404(Category, slug=slug)
	codes = Code.objects.filter(category=category).order_by('-modified')
	heading = "Category: %s" % category.label

	paginator = Paginator(codes, 2)

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
	paginator = Paginator(codes, 2)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	return render_to_response("codes/list.html", dict(categories=categories, codes=codes, user=request.user, code_list=codes.object_list))

def code(request, slug):
	categories = Category.objects.all()
	code = Code.objects.get(slug=slug)
	comments = Comment.objects.filter(code=code)
	d = dict(categories=categories, code=code, comments=comments, form=CommentForm(), user=request.user)
	d.update(csrf(request))
	return render_to_response("codes/code.html", d)

def search(request):
	if 'q' in request.GET:
		term = request.GET['q']
		code_list = Code.objects.filter(Q(title__contains=term)
					| Q(body__contains=term))
		heading = 'Search results'
		return render_to_response("codes/list.html", locals())

def comment(request, slug):
	"""Add a new comment by ajax."""
	""" format: application/xml, application/javascript """
	mimetype = "application/json"
	if request.is_ajax(): 
		p = request.POST
		logger.error(p)
		if p.has_key("body") and p["body"]:
			title = "Unknown"
			author = "Anonymous"
			email = "anonymous@warmlab.com"
			if p['title']: title = p['title']
			if p["author"]: author = p["author"]
			if p['email']: email = p['email']

			#comment = Comment(code=Code.objects.get(slug=slug))
			#cf = CommentForm(p, instance=comment)
			#cf.fields["author"].required = False

			#comment = cf.save(commit=False)
			"""
			comment = Comment()
			comment.title = title
			comment.author = author
			comment.email = email
			comment.body = p['body']
			comment.code = Code.objects.get(slug=slug)
			"""
			comment = Comment(title = title,
			author = author,
			email = email,
			body = p['body'],
			code = Code.objects.get(slug=slug))
			comment.save()
			data = serializers.serialize('json', [comment])
			return HttpResponse(data, content_type=mimetype)
		else:
			return HttpResponse(status=400)
	else:
		return HttpResponse(status=400)

def add_comment(request, pk):
	"""Add a new comment."""
	p = request.POST

	if p.has_key("body") and p["body"]:
		title = "Unknown"
		author = "Anonymous"
		email = "anonymous@warmlab.com"
		if p['title']: title = p['title']
		if p["author"]: author = p["author"]
		if p['email']: email = p['email']

		comment = Comment(code=Code.objects.get(pk=pk))
		cf = CommentForm(p, instance=comment)
		cf.fields["author"].required = False

		comment = cf.save(commit=False)
		comment.title = title
		comment.author = author
		comment.email = email
		comment.save()
	return HttpResponseRedirect(reverse("codes.views.code", args=[pk]))
