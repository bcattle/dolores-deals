from django import forms
from deal.models import Beneficiary

# This doesn't work, because you can't refer to other fields 
# when doing per-field validation. There is probably another place for this.
# Model save() hook?
class BeneficiaryAdminForm(forms.ModelForm):
	class Meta:
		model = Beneficiary
	
	def clean_cause(self):
		self.clean_beneficiary()
		
	def clean_nonprofit(self):
		self.clean_beneficiary()
			
	def clean_beneficiary(self):
		# Make sure only one or the other exists
		print self.cleaned_data
		if self.cleaned_data.get('nonprofit', '') and self.cleaned_data.get('cause', ''):
			raise forms.ValidationError('Beneficiary must contain only a cause or a nonprofit, not both!')
		elif (not self.cleaned_data.get('nonprofit', '')) and (not self.cleaned_data.get('cause', '')):
			raise forms.ValidationError('Beneficiary must contain either a cause or a nonprofit')
		else:
			if self.cleaned_data.get('nonprofit', ''):
				return self.cleaned_data['nonprofit']
			else:
				return self.cleaned_data['cause']