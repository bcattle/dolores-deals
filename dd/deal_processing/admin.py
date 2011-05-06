from django.contrib import admin
from deal_processing.models import Purchase, PaymentToNonprofit, PaymentToUs, PaymentToVendor

class PurchaseAdmin(admin.ModelAdmin):
	list_display = ('timePurchased', 'user', 'dealChoice', 'qty')
	
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PaymentToNonprofit)
admin.site.register(PaymentToUs)
admin.site.register(PaymentToVendor)