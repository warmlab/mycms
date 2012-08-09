import datetime
from django.db import models
from django.db.models import permalink
from django.forms import ModelForm

from django.contrib import admin
from django.contrib.auth.models import User

from markdown import markdown

VIEWABLE_STATUS = [3, 4]
class ViewableManager(models.Manager):
	def get_query_set(self):
		default_queryset = super(ViewableManager, self).get_query_set()
		return default_queryset.filter(status__in=VIEWABLE_STATUS)
	search_field = ['name']

class Category(models.Model):
	label = models.CharField(max_length=63);
	slug = models.SlugField()
	desc = models.TextField(null=True)

	class Meta:
		verbose_name_plural = "categories"

	def __unicode__(self):
		return self.label

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('label',)}
	search_field = ['name']

class Lang(models.Model):
	name = models.CharField(max_length=7);
	desc = models.TextField(null=True)

	def __unicode__(self):
		return self.name

class LangAdmin(admin.ModelAdmin):
	search_field = ['name']

# Create your models here.
class Code(models.Model):
	STATUS_CHOICES = (
			(1, "Needs Edit"),
			(2, "Needs Approval"),
			(3, "Published"),
			(4, "Archived"),
		)

	title = models.CharField(max_length=127)
	slug = models.SlugField()
	nice = models.SmallIntegerField(default=5)
	status = models.IntegerField(choices=STATUS_CHOICES, default=1)
	owner = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	lang = models.ForeignKey(Lang)
	body = models.TextField()
	html_body = models.TextField(editable=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)

	def save(self):
		# The codehilite extension for the markdown library adds the pygments code highlighting support
		self.html_body = markdown(self.body, ['codehilite'])
		self.modified = datetime.datetime.now()
		super(Code, self).save()

	class Meta:
		ordering = ['modified']
		verbose_name_plural = 'codes'

	admin_objects = models.Manager()
	objects = ViewableManager()

	@permalink
	def get_absolute_url(self):
		return ("codes", (), {'slug': self.slug})

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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Lang, LangAdmin)
admin.site.register(Code, CodeAdmin)
admin.site.register(Comment, CommentAdmin)
