from django.db import models
from django.contrib.auth.models import User
#from deal.models import DealChoice

class Order(models.Model):
	user = models.ForeignKey(User)
	dealChoice = models.ForeignKey('deal.DealChoice')
	qty = models.PositiveSmallIntegerField()
	#amount = models.DecimalField(max_digits=9, decimal_places=2)
	timePurchased = models.DateTimeField()
	
	def __unicode__(self):
		return str(self.user) + ' : ' + str(self.timePurchased) + ' - $' + str(self.qty * dealChoice.price)
	class Meta:
		ordering = ['-timePurchased']
	
PAYMENT_STATUS_CHOICES = (
	('PENDING', 'Payment pending'),
	('PROCESSING', 'Payment being processed'),
	('PAID', 'Payment complete'),
	('REFUNDED', 'Payment refunded'),
)	

class PaymentToNonprofit(models.Model):
	order = models.ForeignKey(Order)					# The associated purchase transaction
	beneficiary = models.ForeignKey('deal.Beneficiary')
	nonprofit = models.ForeignKey('nonprofit.Nonprofit', blank=True, null=True)		# Holds nonprofit if beneficiary is a cause
	nonprofitAssigned = models.BooleanField(default=False)				# Did the user select a nonprofit, or do we need to
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.nonprofit) + ' : ' + str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['nonprofit', 'created']
		db_table = 'payments_payments_to_nonprofits'
		verbose_name_plural = 'Payments to Nonprofits'
	
class PaymentToUs(models.Model):
	order = models.ForeignKey(Order)					# The associated purchase transaction
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['created']
		db_table = 'payments_payments_to_us'
		verbose_name_plural = 'Payments to Us'

class PaymentToVendor(models.Model):
	order = models.ForeignKey(Order)					# The associated purchase transaction
	vendor = models.ForeignKey('deal.Vendor', blank=True, null=True)		# Holds nonprofit if beneficiary is a cause
	amount = models.DecimalField(max_digits=9, decimal_places=2)
	status = models.CharField(max_length=12, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
	lastStatusUpdated = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	madeProcessing = models.DateTimeField(blank=True, null=True)
	madePaid = models.DateTimeField(blank=True, null=True)
	madeRefunded = models.DateTimeField(blank=True, null=True)
	
	def __unicode__(self):
		return str(self.vendor) + ' : ' + str(self.created) + ' - ' + str(self.amount)
	class Meta:
		ordering = ['vendor', 'created']
		db_table = 'payments_payments_to_vendors'
		verbose_name_plural = 'Payments to Vendors'
