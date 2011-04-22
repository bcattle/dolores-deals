from store import settings

def default(request):
	# Format: id, label, url
	defaultMenu = [
		{'id': 'deal', 'label': 'Today\'s deal', 'url': '/'},
		{'id': 'causes', 'label': 'Causes', 'url': '/causes/'},
		{'id': 'impact', 'label': 'Impact', 'url': '/impact/'},
		{'id': 'community', 'label': 'Community', 'url': '/community/'},
		{'id': 'blog', 'label': 'Blog', 'url': 'http://blog.doloresdeals.org/'},
	]
	
	return {
		'site_name': settings.SITE_NAME,
		'meta_keywords': settings.META_KEYWORDS,
		'meta_description': settings.META_DESCRIPTION,
		'menu_choices': defaultMenu,
		'mailing_list_text': 'Sign up for our mailing list',
	}