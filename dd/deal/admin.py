from django.contrib import admin
from deal.models import Beneficiary, Vendor, Deal, DealChoice, DealRun
from deal.forms import BeneficiaryAdminForm

class DealAdmin(admin.ModelAdmin):
	#form = DealAdminForm
	list_display = ('neighborhood', 'created', 'headline', 'createdBy', 'approvedBy', 'status')
	search_fields = ('headline', 'createdBy', 'approvedBy')
	list_filter = ('status','neighborhood')
	prepopulated_fields = {'slug': ('headline',)}

class DealChoiceAdmin(admin.ModelAdmin):
	list_display = ('deal', 'index', 'descriptionHtml', 'price', 'enabled', 'minQty', 'maxQty', 'maxPerPerson')
	list_filter = ('deal',)
	
class BeneficiaryAdmin(admin.ModelAdmin):
	#form = BeneficiaryAdminForm
	pass
	
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(Vendor)
admin.site.register(Deal, DealAdmin)
admin.site.register(DealChoice, DealChoiceAdmin)
admin.site.register(DealRun)