from django.conf.urls.defaults import *

urlpatterns = patterns('hyperlocal.views',
	(r'^(?P<city_slug>[-\w]+)/(?P<neighborhood_slug>[-\w]+)/$', 
		'show_neighborhood', { 'template_name': 'neighborhood.html' }, 'neighborhood_index'),
	(r'^(?P<city_slug>[-\w]+)/$', 
		'show_city', { 'template_name': 'city.html' }, 'city_index'),

)