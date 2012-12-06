from django.db import models

from django.contrib import admin

# Create your models here.
class Food(models.Model):
	name = models.CharField(max_length=64)
	photo = models.ImageField(upload_to='images/foods')
	pinyin = models.CharField(max_length=64)
	english_name = models.CharField(max_length=64)

	disposition = models.SmallIntegerField()
	flavour = models.SmallIntegerField()
	meridian = models.SmallIntegerField()

	efficacy = models.TextField()
	shiliao = models.TextField()
	nature = models.TextField()
	shiyi = models.TextField()
	shiji = models.TextField()

	version = models.IntegerField()

	def __unicode__(self):
		return self.name

class FoodAdmin(admin.ModelAdmin):
	search_field = ['name']

class Alias(models.Model):
	food_id = models.ForeignKey(Food)
	name = models.CharField(max_length=64)
	version = models.IntegerField()

	def __unicode__(self):
		return self.name

class AliasAdmin(admin.ModelAdmin):
	search_field = ['name']

class Relation(models.Model):
	food_id1 = models.ForeignKey(Food, related_name="+")
	food_id2 = models.ForeignKey(Food, related_name="+")
	food_id3 = models.ForeignKey(Food, null=True, blank=True, related_name="+")
	food_id4 = models.ForeignKey(Food, null=True, blank=True, related_name="+")
	relation = models.BooleanField()
	nature = models.TextField()
	version = models.IntegerField()

	def __unicode__(self):
		return self.nature

class RelationAdmin(admin.ModelAdmin):
	search_field = ['nature']

class Version(models.Model):
	version = models.IntegerField()
	desc = models.TextField(null=True, blank=True)

admin.site.register(Food, FoodAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Relation, RelationAdmin)
