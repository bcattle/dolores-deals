from django.conf.urls.defaults import *

urlpatterns = patterns('base_accounts.views',
	(r'^login/$', 'login'),
	(r'^verify/$', 'verify'),
)