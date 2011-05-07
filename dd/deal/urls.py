from django.conf.urls.defaults import *

urlpatterns = patterns('deal.views',		
	# regex, view fxn, args, label for get_absolute_url()
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/$', 
		'show_deal', { 'template_name': 'deal.html' }, 'deal_page'),
	(r'^$', 'default_deal'),
)