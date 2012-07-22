from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

class PostAdmin(admin.ModelAdmin):
	search_field = ['title']

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=60)
	body = models.TextField()
	post = models.ForeignKey(Post)

	def __unicode__(self):
		return unicode("%s: %s" % (self.post, self.body[:60]))

class CommentAdmin(admin.ModelAdmin):
	display_fields = ["post", "author", "created"]

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ["post"]

def add_comment(request, pk):
	"""Add a new comment."""
	p = request.POST

	if p.has_key("body") and p["body"]:
		author = "Anonymous"
		if p["author"]: author = p["author"]

		comment = Comment(post=Post.objects.get(pk=pk))
		cf = CommentForm(p, instance=comment)
		cf.fields["author"].required = False

		comment = cf.save(commit=False)
		comment.author = author
		comment.save()
	return HttpResponseRedirect(reverse("blogs.views.post", args=[pk]))

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
