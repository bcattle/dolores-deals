from django.contrib import admin
from nonprofit.models import Cause, Nonprofit

class CauseAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

class NonprofitAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Cause, CauseAdmin)
admin.site.register(Nonprofit, NonprofitAdmin)