from django import forms
import datetime

class MonthYearWidget(forms.MultiWidget):
	"""
	A widget that splits a date into Month/Year with selects.
	"""
	def __init__(self, attrs=None):
		months = (
			('01', 'Jan'),
			('02', 'Feb'),
			('03', 'Mar'),
			('04', 'Apr'),
			('05', 'May'),
			('06', 'Jun'),
			('07', 'Jul'),
			('08', 'Aug'),
			('09', 'Sep'),
			('10', 'Oct'),
			('11', 'Nov'),
			('12', 'Dec'),
		)
		year = int(datetime.date.today().year)
		year_digits = range(year, year+10)
		years = [(year, year) for year in year_digits]
		
		widgets = (forms.Select(attrs=attrs, choices=months), forms.Select(attrs=attrs, choices=years))
		super(MonthYearWidget, self).__init__(widgets, attrs)

	def decompress(self, value):
		if value:
			return [value.month, value.year]
		return [None, None]

	def render(self, name, value, attrs=None):
		try:
			value = datetime.date(month=int(value[0]), year=int(value[1]), day=1)
		except:
			value = ''
		return super(MonthYearWidget, self).render(name, value, attrs)
