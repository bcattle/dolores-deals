from django.http import HttpRequest, HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

def deal(request, deal_id = 0, template_name='deal.html'):
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
