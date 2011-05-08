from django.conf.urls.defaults import *

urlpatterns = patterns('deal_processing.views',
	# regex, view fxn, args, label for get_absolute_url()
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/buy/$', 
		'buy_deal', { 'template_name': 'deal_buy.html', 'SSL': True }, 'buy_deal_page'),
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/confirm/$', 
		'confirm_deal', { 'template_name': 'deal_confirm.html', 'SSL': True }, 'confirm_deal_page'),
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/thanks/$', 
		'thanks_deal', { 'template_name': 'deal_thanks.html' }, 'thanks_deal_page'),
)