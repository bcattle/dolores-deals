from django.shortcuts import get_object_or_404
from hyperlocal.models import City, Neighborhood

def get_city_or_404(city_slug):
	cities_enabled = City.objects.filter(enabled=True)
	city = get_object_or_404(cities_enabled, slug=city_slug)
	return city
def get_neighborhood_or_404(city, neighborhood_slug):
	neighborhoods_enabled = Neighborhood.objects.filter(city=city, enabled=True)
	neighborhood = get_object_or_404(neighborhoods_enabled, slug=neighborhood_slug)
	return neighborhood
