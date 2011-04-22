from django.db import models

# Create your models here.

class UrlString(models.Model):
	str = models.SlugField(max_length=50, unique=True)
	
	def __unicode__(self):
		return self.str
	class Meta:
		ordering = ['str']
		
class TinyUrlString(models.Model):
	str = models.SlugField(max_length=10, unique=True)
	
	def __unicode__(self):
		return self.str
	class Meta:
		ordering = ['str']
