from django.contrib import admin
from payments.models import Purchase, PaymentToNonprofit, PaymentToUs, PaymentToVendor

class PurchaseAdmin(admin.ModelAdmin):
	list_display = ('timePurchased', 'user', 'dealChoice', 'qty', 'amount')
	
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PaymentToNonprofit)
admin.site.register(PaymentToUs)
admin.site.register(PaymentToVendor)

	