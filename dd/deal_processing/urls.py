from django.conf.urls.defaults import *

urlpatterns = patterns('deal_processing.views',
	# regex, view fxn, args, label for get_absolute_url()
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/buy/$', 
		'buy_deal', { 'template_name': 'deal_buy.html' }, 'buy_deal_page'),
	(r'order_info/(?P<city_slug>[-\w]+)/$', 'order_info', { 'template_name': 'order_info.html' }, 'order_info_page'),
)