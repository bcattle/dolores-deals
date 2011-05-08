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
from deal_processing.forms import DealChoiceForm, BuyDealForm, getStateIndex

#import pdb; pdb.set_trace()

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
		# What DealChoice did they buy?
		dealChoice_idx = int(request.POST['dealChoice'].split('_')[1])
		dealChoice = DealChoice.objects.get(deal=deal, index=dealChoice_idx)
		# Attempt to parse the number
		d = {'qty': request.POST[request.POST['dealChoice']]}
		dealChoiceForm = DealChoiceForm(data=d, maxPerPerson=dealChoice.maxPerPerson)

		# We're good if buyform is good and 
		# either (1) they're logged in or (2) they just made a new account
		if dealChoiceForm.is_valid():
			if buyForm.is_valid() and (request.user.is_authenticated() or newUserForm.is_valid()):
				# Create a new user if needed
				if request.user.is_authenticated():
					user = request.user
				else:
					user = createUser(newUserForm, city, neighborhood)
				# Stage the order
				currOrder = Order({
					'user': user,
					'dealChoice': dealChoice,
					'qty': dealChoiceForm.cleaned_data['qty'],
					'billingName': buyForm.cleaned_data['cardholderName'],
					'billingAddress': buyForm.cleaned_data['billingAddress'],
					#'billingAddress2': ,
					'billingCity': buyForm.cleaned_data['billingCity'],
					'billingState': buyForm.cleaned_data['billingState'],
					'billingZip': buyForm.cleaned_data['billingZip'],
				})
				# Stage the credit card info
				#cardNumber, cvvCode, expiration
				
				# We store the staged order in the session,
				# it isn't commit to db until the user confirms.
				# At that point Order.timePurchased is set.
				request.session['currOrder'] = currOrder
				# Send to confirm page
				return HttpResponseRedirect(deal.get_confirm_url())
		else:
			dealChoiceFormErrors = dealChoiceForm.errors['qty']
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
		buyForm = BuyDealForm(initial=initialBuyData, defaultState=city.state)
	# New forms or if we fell through validation
	dealChoices = DealChoice.objects.filter(deal=deal).order_by('index')
	c = {
		'city': city,
		'neighborhood': neighborhood,
		'currDeal': deal,
		'dealChoices': dealChoices,
		'dealChoiceFormErrors': dealChoiceFormErrors,
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
	# request.session['currOrder']
	
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
	