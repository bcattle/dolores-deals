from django.template import RequestContext
from django.shortcuts import render_to_response

def show_coupon(request, city_slug, neighborhood_slug, deal_slug, template_name='coupon.html'):
	c = { }
	return render_to_response(template_name, c, context_instance=RequestContext(request))
	
def redeem_coupon(request):
	c = { }
	return render_to_response('redeem.html', c, context_instance=RequestContext(request))
	