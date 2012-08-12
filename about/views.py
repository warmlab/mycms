# Create your views here.
from django.shortcuts import render_to_response
from about.models import About

def about(request):
	abouts = About.objects.all()
	return render_to_response("about/about.html", dict(abouts=abouts))
