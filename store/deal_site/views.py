from django.http import HttpRequest, HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from deal_site.models import City, Neighborhood, Deal

def show_city(request, city_slug, template_name='city.html'):
	cities_enabled = City.objects.filter(enabled=True)
	city = get_object_or_404(cities_enabled, slug=city_slug)
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
	cities_enabled = City.objects.filter(enabled=True)
	city = get_object_or_404(cities_enabled, slug=city_slug)
	neighborhoods_enabled = Neighborhood.objects.filter(city=city, enabled=True)
	neighborhood = get_object_or_404(neighborhoods_enabled, slug=neighborhood_slug)
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
	
def show_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal.html'):
	cities_enabled = City.objects.filter(enabled=True)
	city = get_object_or_404(cities_enabled, slug=city_slug)
	neighborhoods_enabled = Neighborhood.objects.filter(city=city, enabled=True)
	neighborhood = get_object_or_404(neighborhoods_enabled, slug=neighborhood_slug)
	deals_enabled = Deal.objects.filter(neighborhood=neighborhood, public=True)
	deal = get_object_or_404(deals_enabled, slug=deal_slug)
	defaultDealChoice = dealChoice.objects.filter(deal=deal, index=1)
	c = {
		'city': city,
		'neighborhood': neighborhood,
		'deal': deal,
		'defaultDealChoice': defaultDealChoice,
		'page_title': 'DoloresDeals.org - ' + neighborhood.name + ' : ' + deal.headline
	}
	if deal.meta_keywords:
		c['meta_keywords'] = deal.meta_keywords
	if deal.meta_description:
		c['meta_description'] = deal.meta_description
	return render_to_response(template_name, c, context_instance=RequestContext(request))
	
def show_nonprofit(request, nonprofit_slug, template_name='nonprofit.html'):
	pass

def show_cause(request, cause_slug, template_name='cause.html'):
	pass
	
def deal(request, deal_id = 0, template_name='deal_old.html'):
	if deal_id:
		# Get a specific deal by id
		return HttpResponse('Got deal ' + deal_id)
	else:
		chomp_url = 'http://www.chompon.com/i_deal?nver=1&pid=1661&fg=ffffff&wh=980&noshare=buzz&template=north&'
		mural_file = 'mural.jpg'
		if request.GET.get('d','') == 'fake':
			chomp_url += 'test=1&'
		elif request.GET.get('m','') == '2':
			mural_file = 'mural2.jpg'
	
		# Get today's deal
		c = {
			# get_object_or_404()
			'current_menu_choice': 'deal',
			'chomp_url': chomp_url,
			'mural_file' : mural_file,
		}
		return render_to_response(template_name, c, context_instance=RequestContext(request))

def login(request):
	c = { }
	return render_to_response('coupons.html', c, context_instance=RequestContext(request))
def verify(request):
	c = { }
	return render_to_response('chomp-verify.html', c, context_instance=RequestContext(request))
def coupons(request):
	c = { }
	return render_to_response('coupons.html', c, context_instance=RequestContext(request))
	
def causes(request):
	c = {
		'current_menu_choice': 'causes'
	}
	return render_to_response('causes.html', c, context_instance=RequestContext(request))
def impact(request):
	c = {
		'current_menu_choice': 'impact'
	}
	return render_to_response('impact.html', c, context_instance=RequestContext(request))
def community(request):
	c = {
		'current_menu_choice': 'community'
	}
	return render_to_response('community.html', c, context_instance=RequestContext(request))

def thanks(request):
	c = { }
	return render_to_response('thanks.html', c, context_instance=RequestContext(request))
def partners_vendors(request):
	c = { }
	return render_to_response('partners_vendors.html', c, context_instance=RequestContext(request))
def partners_nonprofits(request):
	c = { }
	return render_to_response('partners_nonprofits.html', c, context_instance=RequestContext(request))
def legal(request):
	c = { }
	return render_to_response('legal.html', c, context_instance=RequestContext(request))
def press(request):
	c = { }
	return render_to_response('press.html', c, context_instance=RequestContext(request))
def jobs(request):
	c = { }
	return render_to_response('jobs.html', c, context_instance=RequestContext(request))
