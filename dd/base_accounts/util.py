def user_enabled(user):
	return user.is_authenticated() and user.is_active