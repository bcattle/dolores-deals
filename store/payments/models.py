from django.db import models

from django.contrib.auth.models import User
#from deal_site.models import DealChoice, Benficiary, Nonprofit, Vendor

# Create your models here.
class Purchase(models.Model):
	user = models.ForeignKey(User)
	dealChoice = models.ForeignKey('deal_site.DealChoice')
	qty = models.PositiveSmallIntegerField()
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	timePurchased = models.DateTimeField()
	
	def __unicode__(self):
		return str(self.user) + ' : ' + str(self.timePurchased) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['timePurchased']
	
PAYMENT_STATUS_CHOICES = (
	('PENDING', 'Payment pending'),
	('PROCESSING', 'Payment being processed'),
	('PAID', 'Payment complete'),
	('REFUNDED', 'Payment refunded'),
)	

class PaymentToNonprofit(models.Model):
	purchase = models.ForeignKey(Purchase)					# The associated purchase transaction
	beneficiary = models.ForeignKey('deal_site.Beneficiary')
	nonprofit = models.ForeignKey('deal_site.Nonprofit', blank=True, null=True)		# Holds nonprofit if beneficiary is a cause
	nonprofitAssigned = models.BooleanField()				# Did the user select a nonprofit, or do we need to
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES)
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madePending = models.DateTimeField(blank=True, null=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.nonprofit) + ' : ' + str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['nonprofit', 'created']
	
class PaymentToUs(models.Model):
	purchase = models.ForeignKey(Purchase)					# The associated purchase transaction
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES)
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madePending = models.DateTimeField(blank=True, null=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['created']

class PaymentToVendor(models.Model):
	purchase = models.ForeignKey(Purchase)					# The associated purchase transaction
	vendor = models.ForeignKey('deal_site.Vendor', blank=True, null=True)		# Holds nonprofit if beneficiary is a cause
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES)
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madePending = models.DateTimeField(blank=True, null=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.vendor) + ' : ' + str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['vendor', 'created']