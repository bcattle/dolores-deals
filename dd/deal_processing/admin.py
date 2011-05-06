from django.contrib import admin
from deal_processing.models import Order, PaymentToNonprofit, PaymentToUs, PaymentToVendor

class OrderAdmin(admin.ModelAdmin):
	list_display = ('timePurchased', 'user', 'dealChoice', 'qty')
	
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentToNonprofit)
admin.site.register(PaymentToUs)
admin.site.register(PaymentToVendor)