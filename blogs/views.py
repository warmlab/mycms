# Create your views here.
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

from blogs.models import *

def main(request):
	posts = Post.objects.all().order_by('-created')
	paginator = Paginator(posts, 2)

	try: page = int(request.GET.get("page", "1"))
	except ValueError: page = 1

	try: posts = paginator.page(page)
	except (InvalidPage, EmptyPage):
		posts = paginator.page(paginator.num_pages)

	return render_to_response("blogs/list.html", dict(posts=posts, user=request.user))

def post(request, pk):
	post = Post.objects.get(pk=int(pk))
	comments = Comment.objects.filter(post=post)
	d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
	d.update(csrf(request))
	return render_to_response("blogs/post.html", d)
