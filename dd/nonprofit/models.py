from django.db import models
from django.contrib.auth.models import User
from base_util.models import Picture
from hyperlocal.models import Neighborhood

class Cause(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50)
	pictures = models.ManyToManyField(Picture, related_name='cause_pictures', blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	icons = models.ManyToManyField(Picture, related_name='cause_icons', blank=True, null=True)
	
	class Meta:
		ordering = ['name']	
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		# view, positional_args, named_args
		return('cause', (), {'cause_slug': self.slug})
		# For now we don't give each city a cause page
		
class Nonprofit(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50)
	causes = models.ManyToManyField(Cause, blank=True, null=True)
	neighborhoods = models.ManyToManyField(Neighborhood)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	sidebarLogo = models.ForeignKey(Picture, related_name='nonprofit_sidebarLogo', blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	url = models.URLField(verify_exists=False, blank=True)		# TODO: turn on verify_exists for rigorous editorial process
	enabled  = models.BooleanField(default=False)
	contacts = models.ManyToManyField(User, blank=True, null=True)
	comment = models.TextField(max_length=2000, blank=True)
	
	class Meta:
		ordering = ['name']
		#order_with_respect_to = 'neighborhood'
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		# view, positional_args, named_args
		return('nonprofit', (), {
			'nonprofit_slug': self.slug,
			'neighborhood_slug': self.neighborhood.slug,
			'city_slug': self.neighborhood.city.slug
		})