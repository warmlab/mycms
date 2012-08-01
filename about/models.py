from django.db import models
from django.contrib import admin

# Create your models here.
class About(models.Model):
	desc = models.TextField()

	def __unicode__(self):
		return self.desc

class AboutAdmin(admin.ModelAdmin):
	search_field = ['desc']

admin.site.register(About, AboutAdmin)
