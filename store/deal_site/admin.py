from django.contrib import admin
from deal_site.models import City, Neighborhood, Picture, Cause, Nonprofit, Beneficiary, Vendor, Deal, DealChoice, DealRun

class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'abbreviation', 'urlString', 'enabled')

class NeighborhoodAdmin(admin.ModelAdmin):
	list_display = ('city', 'name', 'urlString', 'enabled')
	search_fields = ('city', 'name')
	list_filter = ('city', 'enabled')

class PictureAdmin(admin.ModelAdmin):
	list_display = ('pic', 'id', 'created', 'createdBy', 'description')
	search_fields = ('createdBy', 'description')

class DealAdmin(admin.ModelAdmin):
	list_display = ('neighborhood', 'created', 'headline', 'createdBy', 'approvedBy', 'status')
	search_fields = ('headline', 'createdBy', 'approvedBy')
	list_filter = ('status','neighborhood')
	
admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Cause)
admin.site.register(Nonprofit)
admin.site.register(Beneficiary)
admin.site.register(Vendor)
admin.site.register(Deal, DealAdmin)
admin.site.register(DealChoice)
admin.site.register(DealRun)