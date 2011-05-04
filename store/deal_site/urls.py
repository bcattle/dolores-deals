from django.conf.urls.defaults import *

urlpatterns = patterns('deal_site.views',
	(r'^$', 'deal'),
	(r'^deal/$', 'deal'),
	(r'^deal/(?P<deal_id>\d+)/$', 'deal'),
	(r'^coupons/$', 'coupons'),
	(r'^verify/$', 'verify'),
	(r'^impact/$', 'impact'),
	(r'^community/$', 'community'),
	# (r'^blog/$', 'blog'),
	(r'^login/$', 'login'),
	(r'^thanks/$', 'thanks'),
	(r'^partners/vendors/$', 'partners_vendors'),
	(r'^partners/nonprofits/$', 'partners_nonprofits'),
	(r'^legal/$', 'legal'),
	(r'^press/$', 'press'),
	(r'^jobs/$', 'jobs'),

	(r'^causes/$', 'causes'),
	(r'^causes/(?P<cause_slug>[-\w]+)/$', 
		'show_cause', { 'template_name': 'cause.html' }, 'cause_index'),
	(r'^partners/(?P<nonprofit_slug>[-\w]+)/$', 
		'show_nonprofit', { 'template_name': 'nonprofit.html' }, 'nonprofit_index'),
		
	# regex, view fxn, args, label for get_absolute_url()
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/(?P<deal_slug>[-\w]+)/$', 
		'show_deal', { 'template_name': 'deal.html' }, 'deal_page'),
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/$', 
		'show_neighborhood', { 'template_name': 'city.html' }, 'neighborhood_index'),
	(r'^(?P<city_slug>[-\w]+)/$', 
		'show_city', { 'template_name': 'city.html' }, 'city_index'),
)