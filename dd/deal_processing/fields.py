from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us import us_states
		
class MonthYearField(forms.MultiValueField):
	def __init__(self, *args, **kwargs):
		forms.MultiValueField.__init__(self, *args, **kwargs)
		self.fields = (forms.CharField(), forms.CharField(),)
	
	# Compress takes multiple values and combines them into one 
	def compress(self, data_list):
		if data_list:
			return datetime.date(year=int(data_list[1]), month=int(data_list[0]), day=1)
		else:
			return None
			#return datetime.date.today()
			