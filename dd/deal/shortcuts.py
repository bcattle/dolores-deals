from django.shortcuts import get_object_or_404
from hyperlocal.models import City, Neighborhood
from hyperlocal.shortcuts import get_city_or_404, get_neighborhood_or_404
from deal.models import Deal

def get_deal_or_404(neighborhood, deal_slug):
	deals_enabled = Deal.objects.filter(neighborhood=neighborhood, public=True)
	deal = get_object_or_404(deals_enabled, slug=deal_slug)
	return deal