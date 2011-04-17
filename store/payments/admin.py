from django.contrib import admin
from payments.models import Purchase, PaymentToNonprofit, PaymentToUs, PaymentToVendor

admin.site.register(Purchase)
admin.site.register(PaymentToNonprofit)
admin.site.register(PaymentToUs)
admin.site.register(PaymentToVendor)