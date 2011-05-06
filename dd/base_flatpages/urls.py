from django.conf.urls.defaults import *

urlpatterns = patterns('base_flatpages.views',
	(r'^impact/$', 'impact'),
	(r'^community/$', 'community'),
	# (r'^blog/$', 'blog'),
	(r'^thanks/$', 'thanks'),
	(r'^partners/vendors/$', 'partners_vendors'),
	(r'^partners/nonprofits/$', 'partners_nonprofits'),
	(r'^legal/$', 'legal'),
	(r'^press/$', 'press'),
	(r'^jobs/$', 'jobs'),
)