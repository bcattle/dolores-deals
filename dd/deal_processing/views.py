from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test

from base_accounts.util import user_enabled, createUser
from base_accounts.forms import NewUserForm
from hyperlocal.models import City, Neighborhood
from hyperlocal.shortcuts import get_city_or_404, get_neighborhood_or_404
from deal.models import Deal, DealChoice
from deal.shortcuts import get_deal_or_404
from deal_processing.models import Order
from deal_processing.forms import BuyDealForm, getStateIndex

def buy_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal_buy.html'):
	# Is it a valid deal url?
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	deal = get_deal_or_404(neighborhood, deal_slug)
	# Is it a POST request?
	if request.method == 'POST':
		# Create both forms, if the newuser form doesn't validate - doesn't matter
		newUserForm = NewUserForm(request.POST)
		buyForm = BuyDealForm(request.POST)
		# We're good if buyform is good and 
		# either (1) they're logged in or (2) they just made a new account
		if buyForm.is_valid() and (request.user.is_authenticated() or newUserForm.is_valid()):
			# fields are in form.cleaned_data
			#import pdb; pdb.set_trace()
			if not request.user.is_authenticated():
				createUser(newUserForm)
			# Store form data in session and send to confirm page
			request.session['buyForm'] = buyForm
			return HttpResponseRedirect(deal.get_confirm_url())
		# We failed to validate, fall through to render form with errors
	else:
		newUserForm = NewUserForm()
		if request.user.is_authenticated():
			defaultName = request.user.first_name + ' ' + request.user.last_name
		else:
			defaultName = ''
		initialBuyData = {
			'cardholderName': defaultName,
			'billingCity': city.name,
		}
		buyForm = BuyDealForm(initial=initialBuyData, defaultState='CA')
		#buyForm = BuyDealForm(initial=initialBuyData)
	# New forms or if we fell through validation
	dealChoices = DealChoice.objects.filter(deal=deal).order_by('index')
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

def confirm_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal_confirm.html'):
	# Is it a valid deal url?
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	deal = get_deal_or_404(neighborhood, deal_slug)
	# Is there a purchase queued in session?
	# Create Purchase object
	# Save this order info if not already in the database
	pass
	
def thanks_deal(request, city_slug, neighborhood_slug, deal_slug, template_name='deal_thanks.html'):
	# Is it a valid deal url?
	city = get_city_or_404(city_slug)
	neighborhood = get_neighborhood_or_404(city, neighborhood_slug)
	deal = get_deal_or_404(neighborhood, deal_slug)
	# Did the user actually purchase?
	pass
	
@user_passes_test(user_enabled, login_url='/login/')
def order_info(request, order_id, template_name='order_info.html'):
	# Test that order_id exists and belongs to logged-in user
	if not Order.objects.filter(id=order_id).user == request.user:
		raise Http404
	c = { }
	return render_to_response(template_name, c, context_instance=RequestContext(request))