from django.db import models

class UrlString(models.Model):
	str = models.CharField(max_length=150, unique=True)
	
	def __unicode__(self):
		return self.str
	
	class Meta:
		ordering = ['str']
		
class TinyUrlString(models.Model):
	str = models.CharField(max_length=10, unique=True)
	
	def __unicode__(self):
		return self.str
	
	class Meta:
		ordering = ['str']

class City(models.Model):
	name = models.CharField(max_length=50, unique=True)
	abbreviation = models.CharField(max_length=10, blank=True, unique=True)
	urlString = models.ForeignKey(UrlStrings, blank=True, null=True, on_delete=models.SET_NULL)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ['name']

class Neighborhood(models.Model):
	name = models.CharField(max_length=50)
	city = models.ForeignKey(City)
	urlString = models.ForeignKey(UrlStrings, blank=True, null=True, on_delete=models.SET_NULL)

	def __unicode__(self):
		return self.city.name + ', ' + self.name
	
	class Meta:
		unique_together = ('name', 'city')


class User(models.Model):
	firstName = models.CharField(max_length=50)
	middleName = models.CharField(max_length=50, blank=True)
	lastName = models.CharField(max_length=50)
	preferredString = models.CharField(max_length=50, blank=True)	# Allow them to choose fn only, firstlast, firstmiddlelast
	email = models.EmailField()
	password = models.CharField(max_length=50, blank=True)			# TODO: figure out how to do this
	
	twitter = models.CharField(max_length=50, blank=True)
	url = models.UrlField(blank=True)
	pic = models.ImageField(upload_to="profilepics", blank=True, null=True)
	
	created = models.DateTimeField(auto_now_add=True)
	lastLogin = models.DateTimeField(blank=True, null=True)
	enabled = models.BooleanField()
	
	defaultNeighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, on_delete=models.SET_NULL)
	defaultCity = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)

class Picture(models.Model):
	pic = models.ImageField(upload_to="uploadpics")
	created = models.DateTimeField(auto_now_add=True)
	createdBy = models.ForeignKey(User)
	related = models.ManyToManyField(Picture, blank=True, null=True)
	description = models.CharField(max_length=200, blank=True)


class Cause(models.Model):
	name = models.CharField(max_length=50, unique=True)
	pictures = ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	icons = models.ManyToManyField(Picture, blank=True, null=True)
	
class Nonprofit(models.Model):
	name = models.CharField(max_length=50, unique=True)
	causes = models.ManyToManyField(Cause, blank=True, null=True)
	pictures = models.ManyToManyField(Picture, blank=True, null=True)
	htmlLong = models.TextField(max_length=2000, blank=True)
	htmlShort = models.TextField(max_length=500, blank=True)
	contacts = models.ManyToManyField(User, blank=True, null=True)
	comment = models.TextField(max_length=2000, blank=True)
	
class Benficiary(models.Model):
	cause = models.ForeignKey(Cause, blank=True, null=True)
	nonprofit = models.ForeignKey(Nonprofit, blank=True, null=True)
	class Meta:
		unique_together = ('cause', 'nonprofit')

class Vendor(models.Model):
			
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
	
class DealChoice(models.Model):
	deal = models.ForeignKey(Deal)
	index = models.SmallPositiveIntegerField()
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
	
	class Meta:
		unique_together = ('deal', 'index')

class DealRun(models.Model):
	deal = models.ForeignKey(Deal)
	start = models.DateTimeField()
	end = models.DateTimeField()
		
class Purchase(models.Model):
	dealChoice = models.ForeignKey(DealChoice)
	qty = models.PositiveSmallIntegerField()
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	
PAYMENT_STATUS_CHOICES = (
	('PENDING', 'Payment pending'),
	('PROCESSING', 'Payment being processed'),
	('PAID', 'Payment complete'),
	('REFUNDED', 'Payment refunded'),
)	

class Donation(models.Model):
	purchase = models.ForeignKey(Purchase)					# The associated purchase transaction
	beneficiary = models.ForeignKey(Beneficiary)
	nonprofit = models.ForeignKey(Nonprofit, blank=True, null=True)		# Holds nonprofit if beneficiary is a cause
	nonprofitAssigned = models.BooleanField()				# Did the user select a nonprofit, or do we need to
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	
class Payment(models.Model):
	purchase = models.ForeignKey(Purchase)					# The associated purchase transaction
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
