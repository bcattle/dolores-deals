from django.contrib import admin
from base_util.models import Picture

class PictureAdmin(admin.ModelAdmin):
	list_display = ('pic', 'id', 'created', 'createdBy', 'description')
	search_fields = ('createdBy', 'description')
	
admin.site.register(Picture, PictureAdmin)