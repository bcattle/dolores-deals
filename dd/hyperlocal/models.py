from django.db import models

class City(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	abbreviation = models.CharField(max_length=10, blank=True, unique=True)
	#urlString = models.ForeignKey('dynamicurls.UrlString', blank=True, null=True, on_delete=models.SET_NULL)
	enabled  = models.BooleanField(default=False)
	meta_keywords = models.CharField('Meta Keywords', max_length=255, blank=True)
	meta_description = models.CharField('Meta Description', max_length=255, blank=True)
	
	class Meta:
		ordering = ['name']
		#db_table = 'hyperlocal_city'
		verbose_name_plural = 'Cities'
	def __unicode__(self):
		return self.name
	@models.permalink
	def get_absolute_url(self):
		# view, positional_args, named_args
		return('city_index', (), {'city_slug': self.slug})

class Neighborhood(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50)
	city = models.ForeignKey(City)
	#urlString = models.ForeignKey('dynamicurls.UrlString', blank=True, null=True, on_delete=models.SET_NULL)
	enabled  = models.BooleanField(default=False)
	meta_keywords = models.CharField('Meta Keywords', max_length=255, blank=True)
	meta_description = models.CharField('Meta Description', max_length=255, blank=True)

	class Meta:
		unique_together = (('name', 'city'), ('city', 'slug'))
		order_with_respect_to = 'city'
		ordering = ['city', 'name']
	def __unicode__(self):
		return self.city.name + ', ' + self.name
	@models.permalink
	def get_absolute_url(self):
		# view, positional_args, named_args
		return('neighborhood_index', (), {
			'neighborhood_slug': self.slug,
			'city_slug': self.city.slug
		})