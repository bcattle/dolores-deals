from django import forms

class NewUserForm(forms.Form):
	firstName = forms.CharField(max_length = 30, label='First name')
	lastName = forms.CharField(max_length = 60, label='Last name')
	email = forms.EmailField(label='Email address')
	password = forms.CharField(max_length = 30, widget=forms.PasswordInput, label='Password')
	password2 = forms.CharField(max_length = 30, widget=forms.PasswordInput, label='Confirm password')