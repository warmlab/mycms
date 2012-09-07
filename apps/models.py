from datetime import datetime
from django.db import models
from django.db.models import permalink
from django.contrib import admin

# Create your models here.

class Application(models.Model):
	name = models.CharField(max_length=64)
	slug = models.SlugField()
	version = models.CharField(max_length=16)
	author = models.CharField(max_length=128)
	icon = models.ImageField(upload_to='images/apps')
	desc = models.TextField()
	ios_url = models.URLField(null=True, blank=True)
	android_url = models.URLField(null=True, blank=True)
	windows_url = models.URLField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'apps'

	def save(self):
		self.modified = datetime.now()
		super(Application, self).save()

	def __unicode__(self):
		return self.name

class Image(models.Model):
	title = models.CharField(max_length=64)
	slug = models.SlugField()
	app = models.ForeignKey(Application)
	image = models.ImageField(upload_to="images/apps/img")
	caption = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		ordering = ['title']

	def __unicode__(self):
		return self.title

	@permalink
	def get_absolute_url(self):
		return ('app_image', None, {'slug': self.slug})

class ImageInline(admin.StackedInline):
	model = Image

class ApplicationAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	search_field = ['name']
	inlines = [ImageInline]

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Image)
