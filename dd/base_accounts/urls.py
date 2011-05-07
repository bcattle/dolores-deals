from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.auth.views',
	(r'^login/$', 'login', { 'template_name': 'login.html' }, 'login_page'),
	(r'^logout/$', 'logout', { 'next_page': '/' }, 'logout_page'),
)

urlpatterns += patterns('base_accounts.views',
	(r'^register/$', 'register'),
	(r'^verify/$', 'verify'),
	(r'^profile/$', 'profile'),
)