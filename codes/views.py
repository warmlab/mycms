# Create your views here.
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from codes.models import *

def list(request):
	codes = Code.objects.all().order_by('-created')
	paginator = Paginator(codes, 2)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: codes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		codes = paginator.page(paginator.num_pages)

	return render_to_response("codes/list.html", dict(user=request.user, code_list=codes.object_list))

def code(request, pk):
	code = Code.objects.get(pk=int(pk))
	comments = Comment.objects.filter(code=code)
	d = dict(code=code, comments=comments, form=CommentForm(), user=request.user)
	d.update(csrf(request))
	return render_to_response("codes/code.html", d)
