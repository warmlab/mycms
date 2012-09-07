from django.db import models
from django.contrib import admin

# Create your models here.
class About(models.Model):
	title = models.CharField(max_length=64)
	photo = models.ImageField(upload_to='images/about', null=True, blank=True)
	desc = models.TextField()

	def __unicode__(self):
		return self.desc

class AboutAdmin(admin.ModelAdmin):
	search_field = ['desc']

admin.site.register(About, AboutAdmin)
