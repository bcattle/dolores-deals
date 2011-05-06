from django.template import RequestContext
from django.shortcuts import render_to_response
from hyperlocal.shortcuts import get_city_or_404, get_neighborhood_or_404

def show_city(request, city_slug, template_name='city.html'):
	city = get_city_or_404(city_slug)
	c = {
		'city': city,
		'page_title': 'DoloresDeals.org - ' + city.name + ' deals that help your neighborhood',
	}
	if city.meta_keywords:
		c['meta_keywords'] = city.meta_keywords
	if city.meta_description:
		c['meta_description'] = city.meta_description
	return render_to_response(template_name, c, context_instance=RequestContext(request))

def show_neighborhood(request, city_slug, neighborhood_slug, template_name='neighborhood.html'):
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	c = {
		'city': city,
		'neighborhood': neighborhood,
		'page_title': 'DoloresDeals.org - deals that help ' + neighborhood.name
	}
	if neighborhood.meta_keywords:
		c['meta_keywords'] = neighborhood.meta_keywords
	if neighborhood.meta_description:
		c['meta_description'] = neighborhood.meta_description
	return render_to_response(template_name, c, context_instance=RequestContext(request))
