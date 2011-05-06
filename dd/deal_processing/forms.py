from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField, USStateField
from django.contrib.localflavor.us.us_states import US_STATES
from deal_processing.fields import MonthYearField
from deal_processing.widgets import MonthYearWidget

# class DealChoiceForm(forms.Form):
	# activeDealChoice = 
# widget=forms.RadioSelect
	
class NewUserForm(forms.Form):
	firstName = forms.CharField(max_length = 30, label='First name')
	lastName = forms.CharField(max_length = 60, label='Last name')
	email = forms.EmailField(label='Email address')
	password = forms.CharField(max_length = 30, widget=forms.PasswordInput, label='Password')
	password2 = forms.CharField(max_length = 30, widget=forms.PasswordInput, label='Confirm password')
	
class BuyDealForm(forms.Form):
	cardholderName = forms.CharField(max_length = 90, label='Name on card')
	cardNumber = forms.CharField(max_length=24, label='Card number')
	cvvCode = forms.CharField(max_length=5, widget=forms.PasswordInput, label='Card verification code')
	expiration = MonthYearField(label='Expiration date', widget=MonthYearWidget)
	billingAddress = forms.CharField(max_length = 90, label='Billing address')
	billingZip = USZipCodeField(label='Zip code')
	agreeToTerms = forms.BooleanField(required=True, label='Check to indicate that you agree with the DoloresDeals.org Terms of Service')
	# TODO: save this info for later, reuse saved billing address
	
	def __init__(self, defaultCity='', defaultState='', *args, **kwargs):
		super(BuyDealForm, self).__init__(*args, **kwargs)
		self.fields['billingCity'] = forms.CharField(max_length = 30, label='City', initial=defaultCity)
		STATE_CHOICES = list(US_STATES)
		if defaultState:
			STATE_CHOICES.insert(0, (defaultState, getStateFromAbbreviation(defaultState)))
			STATE_CHOICES.insert(1, ('', '---------'))
		self.fields['billingState'] = USStateField(widget=forms.Select(choices=STATE_CHOICES), initial=0, label='State')
		
def getStateFromAbbreviation(abbrev):
	for state in US_STATES:
		if abbrev == state[0]:
			return state[1]
	return None