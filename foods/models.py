from django.db import models

from django.contrib import admin

import json

# Create your models here.
class Food(models.Model):
	name = models.CharField(max_length=64)
	pinyin = models.CharField(max_length=64, null=True, blank=True)
	english_name = models.CharField(max_length=64, null=True, blank=True)

	disposition = models.SmallIntegerField()
	flavour = models.SmallIntegerField()
	meridian = models.SmallIntegerField()

	efficacy = models.TextField()
	shiliao = models.TextField()
	nature = models.TextField()
	shiyi = models.TextField(null=True, blank=True)
	shiji = models.TextField(null=True, blank=True)

	version = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name

	def to_json(self):
		self.__dict__.pop('_state')
		return json.dumps(self, default=lambda o:o.__dict__)

class FoodAdmin(admin.ModelAdmin):
	search_field = ['name']

class Alias(models.Model):
	food = models.ForeignKey(Food)
	name = models.CharField(max_length=64)

	def __unicode__(self):
		return self.name

	def to_json(self):
		self.__dict__.pop('_state')
		return json.dumps(self, default=lambda o:o.__dict__)

class AliasAdmin(admin.ModelAdmin):
	search_field = ['name']

class Relation(models.Model):
	food1 = models.ForeignKey(Food, related_name="+")
	food2 = models.ForeignKey(Food, related_name="+")
	food3 = models.ForeignKey(Food, null=True, blank=True, related_name="+")
	food4 = models.ForeignKey(Food, null=True, blank=True, related_name="+")
	relation = models.BooleanField()
	nature = models.TextField()
	version = models.IntegerField(default=1)

	def __unicode__(self):
		return self.nature

	def to_json(self):
		self.__dict__.pop('_state')
		return json.dumps(self, default=lambda o:o.__dict__)

class RelationAdmin(admin.ModelAdmin):
	search_field = ['nature']

class Version(models.Model):
	version = models.IntegerField(default=1)
	current = models.BooleanField()
	encrypt = models.IntegerField()
	desc = models.TextField(null=True, blank=True)

admin.site.register(Food, FoodAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Relation, RelationAdmin)
