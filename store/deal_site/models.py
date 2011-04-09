from django.db import models

from django.contrib.auth.models import User
from dynamicurls.models import UrlString, TinyUrlString

class City(models.Model):
	name = models.CharField(max_length=50, unique=True)
	abbreviation = models.CharField(max_length=10, blank=True, unique=True)
	urlString = models.ForeignKey(UrlString, blank=True, null=True, on_delete=models.SET_NULL)
	enabled  = models.BooleanField()
	
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']

class Neighborhood(models.Model):
	name = models.CharField(max_length=50)
	city = models.ForeignKey(City)
	urlString = models.ForeignKey(UrlString, blank=True, null=True, on_delete=models.SET_NULL)
	enabled  = models.BooleanField()

	def __unicode__(self):
		return self.city.name + ', ' + self.name
	class Meta:
		unique_together = ('name', 'city')

class Picture(models.Model):
	pic = models.ImageField(upload_to="uploadpics")
	created = models.DateTimeField(auto_now_add=True)
	createdBy = models.ForeignKey(User)
	related = models.ManyToManyField(Picture, blank=True, null=True)
	description = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.id + ' : ' + str(self.created)
	class Meta:
		ordering = ['created']

class Cause(models.Model):
	name = models.CharField(max_length=50, unique=True)
	pictures = ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	icons = models.ManyToManyField(Picture, blank=True, null=True)
	
	def __unicode__(self):
		return name
	class Meta:
		ordering = ['name']
	
class Nonprofit(models.Model):
	name = models.CharField(max_length=50, unique=True)
	causes = models.ManyToManyField(Cause, blank=True, null=True)
	neighborhood = models.ManyToManyField(Neighborhood)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	contacts = models.ManyToManyField(User, blank=True, null=True)
	comment = models.TextField(max_length=2000, blank=True)
	
	def __unicode__(self):
		return name
	class Meta:
		ordering = ['name']
	
class Benficiary(models.Model):
	cause = models.ForeignKey(Cause, blank=True, null=True)
	nonprofit = models.ForeignKey(Nonprofit, blank=True, null=True)
	def __unicode__(self):
		if cause:
			return cause
		if nonprofit:
			return nonprofit
		else:
			return 'Empty'
	class Meta:
		unique_together = ('cause', 'nonprofit')

class Vendor(models.Model):
	name = models.CharField(max_length=50, unique=True)
	neighborhood = models.ForeignKey(Neighborhood)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	contacts = models.ManyToManyField(User, blank=True, null=True)
	comment = models.TextField(max_length=2000, blank=True)
	
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']
	
DEAL_STATUS_CHOICES = (
	('EDT', 'Being edited'),
	('REV', 'Awaiting review'),
	('REL', 'Released to run'),
	('RUN', 'Running'),
	('DON', 'Done'),
)

class Deal(models.Model):
	headline = models.TextField(max_length=200)
	htmlLong = models.TextField(max_length=4000)
	picture = models.ForeignKey(Picture, blank=True, null=True)
	startDate = models.DateTimeField(blank=True, null=True)
	endDate = models.DateTimeField(blank=True, null=True)		# These override the values in a particular DealChoice
	vendor = models.ManyToManyField(Vendor)
	defaultBeneficiary = models.ForeignKey(Beneficiary)
	beneficiaryCanChange = models.BooleanField()
	urlString = models.ForeignKey(UrlString)
	tinyUrlString = models.ForeignKey(TinyUrlString, blank=True, null=True)
	status = models.CharField(max_length=3, choices=DEAL_STATUS_CHOICES)
	created = models.DateTimeField(auto_now_add=True)
	createdBy = models.ForeignKey(User)
	approvedBy = models.ForeignKey(User, blank=True, null=True)
	
	def __unicode__(self):
		return self.vendor.name + ' : ' + self.headline
	class Meta:
		ordering = ['vendor', 'startDate']
	
	
class DealChoice(models.Model):
	deal = models.ForeignKey(Deal)
	index = models.SmallPositiveIntegerField()
	headline = models.TextField(max_length=200)
	htmlLong = models.TextField(max_length=4000)
	picture = models.ForeignKey(Picture, blank=True, null=True)
	startDate = models.DateTimeField(blank=True, null=True)
	endDate = models.DateTimeField(blank=True, null=True)		# These override the values in a particular DealChoice
	
	price = models.DecimalField(max_digits=6, decimal_places=2)
	regPrice = models.DecimalField(max_digits=6, decimal_places=2)
	amtToCharity = models.DecimalField(max_digits=6, decimal_places=2)
	percentToCharity = models.DecimalField(max_digits=5, decimal_places=2)
	
	minQty = models.PositiveIntegerField()
	maxQty = models.PositiveIntegerField()
	
	def __unicode__(self):
		return str(self.deal) + ':(' + self.index + ') - ' + self.headline
	class Meta:
		unique_together = ('deal', 'index')
		ordering = ['deal', 'index']

class DealRun(models.Model):
	deal = models.ForeignKey(Deal)
	start = models.DateTimeField()
	end = models.DateTimeField()
	
	def __unicode__(self):
		return str(self.deal) + ': run from ' + str(self.start) + ' to ' + str(self.end)
	class Meta:
		ordering = ['deal', 'start']
		
