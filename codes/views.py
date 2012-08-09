# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect

from codes.models import *

import logging
logger = logging.getLogger('mycms.debug')

def category(request, slug):
	category = get_object_or_404(Category, slug=slug)
	code_list = Code.objects.filter(category=category)
	heading = "Category: %s" % category.label
	return render_to_response("codes/list.html", locals())

def taglist(request, pk):
	categories = Category.objects.all()
	category = Category.objects.get(pk=int(pk))
	codes = Code.objects.filter(category=category).order_by('-created')
	paginator = Paginator(codes, 2)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	return render_to_response("codes/list.html", dict(categories=categories, codes=codes, user=request.user, code_list=codes.object_list))

def list(request):
	pk = None
	categories = Category.objects.all()

	if pk is None:
		codes = Code.objects.all().order_by('-created')
	else:
		category = Category.objects.get(pk=int(pk))
		codes = Code.objects.filter(category=category).order_by('-created')
	paginator = Paginator(codes, 2)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	return render_to_response("codes/list.html", dict(categories=categories, codes=codes, user=request.user, code_list=codes.object_list))

def code(request, slug):
	logger.error(slug)
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

def comment(request, pk):
	"""Add a new comment by ajax."""
	""" format: application/xml, application/javascript """
	mimetype = "application/javascript";
	if request.is_ajax(): 
		p = request.POST
		logger.error(p)
		"""
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
		"""
		data = serilizers.serialize(mimetype, comment)
		return HttpResonse(data, mimetype)
	else:
		return HttpResonse(status=400)

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
