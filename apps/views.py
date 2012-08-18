# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.context_processors import csrf

from apps.models import Application

PAGE_NUM = 5

def list(request):
	apps = Application.objects.all().order_by('-modified')

	paginator = Paginator(apps, PAGE_NUM)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: apps = paginator.page(page)
	except (InvalidPage, EmptyPage):
		apps = paginator.page(paginator.num_pages)

	return render_to_response("apps/list.html", dict(apps=apps, user=request.user, app_list=apps.object_list))

def app(request, slug):
	app = get_object_or_404(Application, slug=slug)
	d = dict(app=app, user=request.user)
	d.update(csrf(request))
	return render_to_response("apps/app.html", d)
