from django.db import models
from django.contrib.auth.models import User
from payments.models import Purchase

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
		db_table = 'deal_site_cities'
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

class Picture(models.Model):
	pic = models.ImageField(upload_to='uploadpics')
	created = models.DateTimeField(auto_now_add=True)
	createdBy = models.ForeignKey(User)
	related = models.ManyToManyField('self', blank=True, null=True)
	description = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return str(self.id) + ' : ' + str(self.created)
	class Meta:
		ordering = ['created']

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
	neighborhood = models.ManyToManyField(Neighborhood)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	sidebarLogo = models.ForeignKey(Picture, related_name='nonprofit_sidebarLogo', blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	url = models.URLField(verify_exists=False, blank=True)		# TODO: turn on verify_exists for rigorous editorial process
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
	
class Beneficiary(models.Model):
	cause = models.ForeignKey(Cause, blank=True, null=True)
	nonprofit = models.ForeignKey(Nonprofit, blank=True, null=True)
	def __unicode__(self):
		if self.cause:
			return str(self.cause)
		elif self.nonprofit:
			return str(self.nonprofit)
		else:
			return 'Empty'
	class Meta:
		unique_together = ('cause', 'nonprofit')
		db_table = 'deal_site_beneficiaries'
		verbose_name_plural = 'Beneficiaries'

class Vendor(models.Model):
	name = models.CharField(max_length=50, unique=True)
	neighborhood = models.ForeignKey(Neighborhood)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	url = models.URLField(verify_exists=False, blank=True)		# TODO: turn on verify_exists for rigorous editorial process
	contacts = models.ManyToManyField(User, blank=True, null=True)
	comment = models.TextField(max_length=2000, blank=True)
	
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']
		order_with_respect_to = 'neighborhood'
	
DEAL_STATUS_CHOICES = (
	('EDT', 'Being edited'),
	('REV', 'Awaiting review'),
	('REL', 'Released to run'),
	('RUN', 'Running'),
	('DON', 'Done'),
)

VENDOR_EMAIL_NOTIFICATION_CHOICES = (
	('PS', 'Per sale'),
	('D', 'Daily'),
	('PD', 'Per deal')
)

class Deal(models.Model):
	neighborhood = models.ForeignKey(Neighborhood)			# Deal has a home neighborhood, relavence to other neighborhoods
															# is inferred from neighborhood adjacency graph
	headline = models.TextField(max_length=200)
	subheadline = models.TextField(max_length=200)
	slug = models.SlugField(max_length=50)
	htmlLong = models.TextField(max_length=4000)
	picture = models.ForeignKey(Picture, blank=True, null=True)
	startDate = models.DateTimeField(blank=True, null=True)
	endDate = models.DateTimeField(blank=True, null=True)		# These override the values in a particular DealChoice
	vendor = models.ForeignKey(Vendor)
	vendorEmailNotificationFrequency = models.CharField(max_length=3, choices=VENDOR_EMAIL_NOTIFICATION_CHOICES, blank=True)
	defaultBeneficiary = models.ForeignKey(Beneficiary)
	beneficiaryCanChange = models.BooleanField(default=True)
	#urlString = models.ForeignKey('dynamicurls.UrlString', blank=True, null=True)
	#tinyUrlString = models.ForeignKey('dynamicurls.TinyUrlString', blank=True, null=True)
	#related = models.ManyToManyField('self', blank=True, null=True)		# This replaces the 'DealChoice' class
																		# after the customer buys, they are presented 
																		# the opportunity to choose between the "related" deals
	status = models.CharField(max_length=3, choices=DEAL_STATUS_CHOICES, default='EDT')
	public = models.BooleanField(default=False)				# Is the deal publically-visible? Allows completed 
															# deals to persist for some amount of time
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	createdBy = models.ForeignKey(User, related_name='deal_createdBy')
	approvedBy = models.ForeignKey(User, related_name='deal_approvedBy', blank=True, null=True)
	meta_keywords = models.CharField('Meta Keywords', max_length=255, blank=True)
	meta_description = models.CharField('Meta Description', max_length=255, blank=True)

	def getTimeRemainingString(self):
		
	def getNumPurchased(self):
		return Purchase.objects.filter(dealChoice__deal=deal).count()
	class Meta:
		ordering = ['startDate', 'vendor']
		order_with_respect_to = 'neighborhood'
		unique_together = ('neighborhood', 'slug')
	def __unicode__(self):
		return self.vendor.name + ' : ' + self.headline
	@models.permalink
	def get_absolute_url(self):
		# view, positional_args, named_args
		return('deal_page', (), {
			'deal_slug': self.slug, 
			'neighborhood_slug': self.neighborhood.slug,
			'city_slug': self.neighborhood.city.slug
		})
	
class DealChoice(models.Model):
	deal = models.ForeignKey(Deal)
	index = models.PositiveSmallIntegerField()
	descriptionHtml = models.TextField(max_length=500, blank=True)
	picture = models.ForeignKey(Picture, blank=True, null=True)
	#startDate = models.DateTimeField(blank=True, null=True)
	#endDate = models.DateTimeField(blank=True, null=True)
	
	price = models.DecimalField(max_digits=9, decimal_places=2)
	regPrice = models.DecimalField(max_digits=9, decimal_places=2)
	# One or the other, keeps nice round numbers
	dollarsToCharity = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	percentToCharity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	
	minQty = models.PositiveIntegerField(blank=True, null=True)			# Or the deal won't happen (TODO)
	maxQty = models.PositiveIntegerField(blank=True, null=True)
	
	def getDonationString(self):
		if self.dollarsToCharity:
			return '$' + str(self.dollarsToCharity) + '</span> from'
		else:
			return str(self.percentToCharity) + '%</span> of'
	def discountDollars(self):
		return '%.2f' % (self.regPrice - self.price)
	def discountPercent(self):
		return '%d' % ((self.price / self.regPrice) * 100)
	def __unicode__(self):
		return str(self.deal.vendor) + ': (opt ' + str(self.index) + ') - ' + self.title
	class Meta:
		unique_together = ('deal', 'index')
		ordering = ['deal', 'index']
		order_with_respect_to = 'deal'

class DealRun(models.Model):
	deal = models.ForeignKey(Deal)
	start = models.DateTimeField()
	end = models.DateTimeField()
	
	def __unicode__(self):
		return str(self.deal) + ': run from ' + str(self.start) + ' to ' + str(self.end)
	class Meta:
		ordering = ['-start', 'deal']
		
# Inflexible? or implement this as a kind of cache
# that avoids the neighborhood-adjacency logic?
# class ActiveDeal(models.Model):
	# """ 
	# Lists the active deal in every neighborhood,
	# null if no deal is active. 
	# """
	# neighborhood = models.ForeignKey(Neighborhood)
	# deal = models.ForeignKey(Deal, blank=True, null=True)
	
	# def __unicode__(self):
		# return str(self.neighborhood) + ', active: ' + str(self.deal)
	# class Meta:
		# ordering = ['neighborhood']
