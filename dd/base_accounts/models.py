from django.db import models
from django.contrib.auth.models import User
from hyperlocal.models import Neighborhood, City
from deal_processing.models import BillingDetailBase

# auth.models.User contains
# username, first_name, last_name, email, is_active, last_login, date_joined

GENDER_CHOICES = (
	('M', 'male'),
	('F', 'female'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	middle_name = models.CharField(max_length=50, blank=True)
	preferredString = models.CharField(max_length=50, blank=True)	# Allow them to choose fn only, firstlast, firstmiddlelast
	sex = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True)
	
	twitter = models.CharField(max_length=50, blank=True)
	url = models.URLField(verify_exists=False, blank=True)
	pic = models.ImageField(upload_to="profilepics", blank=True, null=True)
	
	defaultNeighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, on_delete=models.SET_NULL)
	defaultCity = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
	zipCode = models.CharField(max_length=11, blank=True)
	
	def __unicode__(self):
		return self.user.first_name + ' ' + self.user.last_name
	class Meta:
		ordering = ['user']

class UserBillingDetail(BillingDetailBase):
	user =  models.ForeignKey(User)