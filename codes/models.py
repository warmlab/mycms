from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class Tag(models.Model):
	name = models.CharField(max_length=63);
	desc = models.TextField()

	def __unicode__(self):
		return self.name

class TagAdmin(admin.ModelAdmin):
	search_field = ['name']

class Lang(models.Model):
	name = models.CharField(max_length=7);
	desc = models.TextField()

	def __unicode__(self):
		return self.name

class LangAdmin(admin.ModelAdmin):
	search_field = ['name']

# Create your models here.
class Code(models.Model):
	title = models.CharField(max_length=127)
	body = models.TextField()
	nice = models.SmallIntegerField(default=5)
	created = models.DateTimeField(auto_now_add=True)
	tag = models.ForeignKey(Tag)
	lang = models.ForeignKey(Lang)

	def __unicode__(self):
		return self.title

class CodeAdmin(admin.ModelAdmin):
	search_field = ['title']

class Comment(models.Model):
	title = models.CharField(max_length=63);
	author = models.CharField(max_length=63)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	code = models.ForeignKey(Code)

	def __unicode__(self):
		return unicode("%s: %s" % (self.code, self.body[:63]))

class CommentAdmin(admin.ModelAdmin):
	display_fields = ["title", "code", "author", "created"]

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ["code"]

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

admin.site.register(Tag, TagAdmin)
admin.site.register(Lang, LangAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Comment, CommentAdmin)
