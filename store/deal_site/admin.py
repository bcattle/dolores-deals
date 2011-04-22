from django.contrib import admin
from deal_site.models import City, Neighborhood, Picture, Cause, Nonprofit, Beneficiary, Vendor, Deal, DealChoice, DealRun
from deal_site.forms import BeneficiaryAdminForm

class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'abbreviation', 'slug', 'enabled')
	prepopulated_fields = {'slug': ('name',)}

class NeighborhoodAdmin(admin.ModelAdmin):
	list_display = ('city', 'name', 'slug', 'enabled')
	search_fields = ('city', 'name')
	list_filter = ('city', 'enabled')
	prepopulated_fields = {'slug': ('name',)}

class PictureAdmin(admin.ModelAdmin):
	list_display = ('pic', 'id', 'created', 'createdBy', 'description')
	search_fields = ('createdBy', 'description')

class DealAdmin(admin.ModelAdmin):
	#form = DealAdminForm
	list_display = ('neighborhood', 'created', 'headline', 'createdBy', 'approvedBy', 'status')
	search_fields = ('headline', 'createdBy', 'approvedBy')
	list_filter = ('status','neighborhood')
	prepopulated_fields = {'slug': ('headline',)}
	
class CauseAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

class NonprofitAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

class BeneficiaryAdmin(admin.ModelAdmin):
	#form = BeneficiaryAdminForm
	pass
	
admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Cause, CauseAdmin)
admin.site.register(Nonprofit, NonprofitAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(Vendor)
admin.site.register(Deal, DealAdmin)
admin.site.register(DealChoice)
admin.site.register(DealRun)