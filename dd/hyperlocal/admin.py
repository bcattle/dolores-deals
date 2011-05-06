from django.contrib import admin
from hyperlocal.models import City, Neighborhood

class CityAdmin(admin.ModelAdmin):
	list_display = ('name', 'abbreviation', 'slug', 'enabled')
	prepopulated_fields = {'slug': ('name',)}

class NeighborhoodAdmin(admin.ModelAdmin):
	list_display = ('city', 'name', 'slug', 'enabled')
	search_fields = ('city', 'name')
	list_filter = ('city', 'enabled')
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(City, CityAdmin)
admin.site.register(Neighborhood, NeighborhoodAdmin)