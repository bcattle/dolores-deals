from django.conf.urls.defaults import *

urlpatterns = patterns('nonprofit.views',
	#(r'^causes/$', 'causes'),
	(r'^causes/(?P<cause_slug>[-\w]+)/$', 
		'show_cause', { 'template_name': 'cause.html' }, 'cause_index'),
	(r'^partners/(?P<nonprofit_slug>[-\w]+)/$', 
		'show_nonprofit', { 'template_name': 'nonprofit.html' }, 'nonprofit_index'),
)