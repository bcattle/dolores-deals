from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.contrib.localflavor.us.us_states import US_STATES		# ('AL', 'Alabama')

from base_accounts.util import user_enabled
from hyperlocal.models import City, Neighborhood
from hyperlocal.shortcuts import get_city_or_404, get_neighborhood_or_404
from deal.models import Deal, DealChoice
from deal.shortcuts import get_deal_or_404
from deal_processing.models import Order
from deal_processing.forms import NewUserForm, BuyDealForm

def buy_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal_buy.html'):
	# Is it a valid deal url?
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	deal = get_deal_or_404(neighborhood, deal_slug)
	dealChoices = DealChoice.objects.filter(deal=deal).order_by('index')
	newUserForm = NewUserForm()
	buyForm = BuyDealForm(defaultState=city.state, defaultCity=city.name)
	c = {
		'city': city,
		'neighborhood': neighborhood,
		'currDeal': deal,
		'dealChoices': dealChoices,
		'nonprofit': deal.getDefaultNonprofit(),
		'newUserForm': newUserForm,
		'buyForm': buyForm,
		'current_menu_choice': 'deal',
		'page_title': 'DoloresDeals.org - ' + neighborhood.name + ' : ' + deal.headline
	}
	if deal.meta_keywords:
		c['meta_keywords'] = deal.meta_keywords
	if deal.meta_description:
		c['meta_description'] = deal.meta_description
	return render_to_response(template_name, c, context_instance=RequestContext(request))

@user_passes_test(user_enabled, login_url='/login/')
def order_info(request, order_id, template_name='order_info.html'):
	# Test that order_id exists and belongs to logged-in user
	if not Order.objects.filter(id=order_id).user == request.user:
		raise Http404
	c = { }
	return render_to_response(template_name, c, context_instance=RequestContext(request))