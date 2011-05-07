from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	(r'^', include('dd.base_accounts.urls')),
	(r'^', include('dd.base_flatpages.urls')),
	(r'^', include('dd.deal.urls')),
	(r'^', include('dd.deal_processing.urls')),	
	(r'^', include('dd.deal_coupon.urls')),
	(r'^', include('dd.hyperlocal.urls')),
	(r'^', include('dd.nonprofit.urls')),
	
)
