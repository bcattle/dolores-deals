from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField, USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import US_STATES
from deal_processing.fields import MonthYearField
from deal_processing.widgets import MonthYearWidget
	
class BuyDealForm(forms.Form):
	cardholderName = forms.CharField(max_length = 90, label='Name on card')
	cardNumber = forms.CharField(max_length=24, label='Card number', initial='')
	cvvCode = forms.CharField(max_length=5, widget=forms.PasswordInput, label='Card verification code')
	expiration = MonthYearField(label='Expiration date', widget=MonthYearWidget)
	billingAddress = forms.CharField(max_length = 90, label='Billing address')
	billingCity = forms.CharField(max_length = 30, label='City')
	#billingState = USStateField(widget=USStateSelect, label='State')
	billingState = forms.CharField()
	billingZip = USZipCodeField(label='Zip code')
	agreeToTerms = forms.BooleanField(required=True, label='Check to indicate that you agree with the DoloresDeals.org Terms of Service')
	# TODO: save this info for later, reuse saved billing address
	def __init__(self, *args, **kwargs):
		defaultState = kwargs.pop('defaultState','')
		super(BuyDealForm, self).__init__(*args, **kwargs)
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
	
def getStateIndex(abbrev):
	for index,state in enumerate(US_STATES):
		if abbrev == state[0]:
			return index
	return None