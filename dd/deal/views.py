from django.template import RequestContext
from django.shortcuts import render_to_response

from hyperlocal.models import City, Neighborhood
from hyperlocal.shortcuts import get_city_or_404, get_neighborhood_or_404
from deal.models import Deal, DealChoice
from deal.shortcuts import get_deal_or_404
	
def show_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal.html'):
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	deal = get_deal_or_404(neighborhood, deal_slug)
	defaultDealChoice = DealChoice.objects.filter(deal=deal).order_by('index')[0]
	c = {
		'city': city,
		'neighborhood': neighborhood,
		'currDeal': deal,
		'defaultDealChoice': defaultDealChoice,
		'nonprofit': deal.getDefaultNonprofit(),
		'current_menu_choice': 'deal',
		'page_title': 'DoloresDeals.org - ' + neighborhood.name + ' : ' + deal.headline
	}
	if deal.meta_keywords:
		c['meta_keywords'] = deal.meta_keywords
	if deal.meta_description:
		c['meta_description'] = deal.meta_description
	return render_to_response(template_name, c, context_instance=RequestContext(request))
	
