from django.contrib.auth.models import User
from base_accounts.models import UserProfile
from base_accounts.forms import NewUserForm

def user_enabled(user):
	return user.is_authenticated() and user.is_active
	
def createUser(newUserForm, defaultCity, defaultNeighborhood):
	""" 
	Creates a new user account. Takes a NewUserForm as input.
	"""
	newUser = User(	username = newUserForm.cleaned_data['email'],
					first_name = newUserForm.cleaned_data['firstName'], 
					last_name = newUserForm.cleaned_data['lastName'], 
					email = newUserForm.cleaned_data['email'], 
					is_active = True)
	newUser.set_password(newUserForm.cleaned_data['password'])
	newUserProfile = UserProfile(	user = newUser,
									defaultNeighborhood = defaultNeighborhood,
									defaultCity = defaultCity)
	
	newUser.save()
	newUserProfile.save()
	return newUser
	