from django.conf.urls.defaults import *

urlpatterns = patterns('deal_coupon.views',
	# regex, view fxn, args, label for get_absolute_url()
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/coupon/$', 
		'show_coupon', { 'template_name': 'deal_buy.html' }, 'show_coupon_page'),
	(r'^redeem/$', 'redeem_coupon'),
)