from datetime import datetime
from django.db import models
from django.contrib import admin

# Create your models here.

class Application(models.Model):
	name = models.CharField(max_length=63)
	slug = models.SlugField()
	version = models.CharField(max_length=16)
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

class ApplicationAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	search_field = ['name']

admin.site.register(Application, ApplicationAdmin)
