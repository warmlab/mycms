# Create your views here.
from django.shortcuts import render_to_response

def about(request):
	about = About.objects.get()
	return render_to_response("about/about.html", dict(about=about))
