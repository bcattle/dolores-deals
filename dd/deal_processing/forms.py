from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField, USStateField, USStateSelect
from django.contrib.localflavor.us.us_states import US_STATES
from deal_processing.fields import MonthYearField
from deal_processing.widgets import MonthYearWidget

# PROBLEM: If using a single select, how do we deal with different available quantities per choice?

# class DealChoiceForm(forms.Form):
	# def __init__(self, *args, **kwargs):
		# defaultState = kwargs.pop('defaultState','')
		# super(BuyDealForm, self).__init__(*args, **kwargs)
		
	# dealChoice = forms.ModelChoiceField(queryset= , empty_label=None)
	# qty = forms.IntegerField(max_value=99, label='', 
							# error_messages={'required': 'Please enter a quantity to buy',
											# 'invalid': 'Please enter a valid quantity',
											# 'max_value': 'Sorry, you can only purchase up to xx per person'})

# TODO: Verify actual maximum-length credit card numbers
class BuyDealForm(forms.Form):
	cardholderName = forms.CharField(max_length = 90, label='Name on card',
									error_messages={'required': 'Please enter a name for the cardholder'})
	cardNumber = forms.IntegerField(max_value=1000000000000000000000000, label='Card number', initial='',
									error_messages={'required': 'Please enter a valid card number',
													'invalid': 'Please enter a valid card number with only the digits 0-9'})
	cvvCode = forms.IntegerField(max_value=100000, widget=forms.PasswordInput, label='Card verification code',
									error_messages={'required': 'Please enter a verification code',
													'invalid': 'Please enter a valid verification code with only the digits 0-9'})
	expiration = MonthYearField(label='Expiration date', widget=MonthYearWidget)
	billingAddress = forms.CharField(max_length = 90, label='Billing address',
									error_messages={'required': 'Please enter a billing address'})
	billingCity = forms.CharField(max_length = 30, label='City',
									error_messages={'required': 'Please enter a city'})
	billingState = forms.CharField()
	billingZip = USZipCodeField(label='Zip code',
								error_messages={'required': 'Please enter a zip code'})
	#agreeToTerms = forms.BooleanField(required=True, label='Check to indicate that you agree with the DoloresDeals.org Terms of Service', error_messages={'required': 'You must agree to the Terms of Service to place this order'})
	# TODO: save this info for later, reuse saved billing address
	def __init__(self, *args, **kwargs):
		defaultState = kwargs.pop('defaultState','')
		super(BuyDealForm, self).__init__(*args, **kwargs)
		STATE_CHOICES = list(US_STATES)
		if defaultState:
			STATE_CHOICES.insert(0, (defaultState, getStateFromAbbreviation(defaultState)))
			STATE_CHOICES.insert(1, ('', '---------'))
		self.fields['billingState'] = USStateField(widget=forms.Select(choices=STATE_CHOICES), initial=0, label='State', error_messages={'required': 'Please choose a valid state'})
		
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