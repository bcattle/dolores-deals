from django.conf.urls.defaults import *
from store_chompon import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('deal_site.views',
    # Example:
    # (r'^dolores/', include('dolores.foo.urls')),
    # (r'^dolores/', include('dolores.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	(r'^$', 'deal'),

	(r'^deal/$', 'deal'),
	(r'^deal/(?P<deal_id>\d+)/$', 'deal'),
	(r'^coupons/$', 'coupons'),
	(r'^verify/$', 'verify'),
	(r'^causes/$', 'causes'),
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
	
)

# In the template, {{ staticroot }} is prepended to every static url
# settings.STATIC_PATH			- 'media/'
# settings.STATIC_URL			- {{ staticroot }} 
# settings.STATIC_ROOT			- root on the filesystem

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^' + settings.STATIC_PATH + r'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )