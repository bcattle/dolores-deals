from django.http import HttpRequest, HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from store_chompon import settings

# Format: id, label, url
defaultMenu = [
		{'id': 'deal', 'label': 'Today\'s deal', 'url': '/'},
		{'id': 'b2b', 'label': 'Save Bay to Breakers!', 'url': '/bay-to-breakers/'},
		{'id': 'story', 'label': 'Our Story', 'url': '/our-story/'},
		{'id': 'impact', 'label': 'Impact', 'url': '/impact/'},
		#{'id': 'community', 'label': 'Community', 'url': '/community/'},
		{'id': 'blog', 'label': 'Blog', 'url': 'http://blog.doloresdeals.org/'},
	]

defaultContext = Context({
			'staticroot': settings.STATIC_URL,
			'menu_choices': defaultMenu,
			'current_menu_choice': '',
			'mailing_list_text': 'Sign up for our mailing list',
		})

def deal(request, deal_id = 0):
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
		c = Context(defaultContext)
		c.update({
			'current_menu_choice': 'deal',
			'chomp_url': chomp_url,
			'mural_file' : mural_file,
		})
		return render_to_response('deal.html', c)

def login(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('coupons.html', c)
def verify(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('chomp-verify.html', c)
def coupons(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('coupons.html', c)
	
def causes(request):
	c = Context(defaultContext)
	# assert False
	c.update({
		'current_menu_choice': 'causes'
	})
	return render_to_response('causes.html', c)
def story(request):
	c = Context(defaultContext)
	c.update({
		'current_menu_choice': 'story'
	})
	return render_to_response('story.html', c)
def b2b(request):
	c = Context(defaultContext)
	c.update({
		'current_menu_choice': 'b2b'
	})
	return render_to_response('b2b.html', c)
def impact(request):
	c = Context(defaultContext)
	c.update({
		'current_menu_choice': 'impact'
	})
	return render_to_response('impact.html', c)
def community(request):
	c = Context(defaultContext)
	c.update({
		'current_menu_choice': 'community'
	})
	return render_to_response('community.html', c)

def thanks(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('thanks.html', c)
def partners_vendors(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('partners_vendors.html', c)
def partners_nonprofits(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('partners_nonprofits.html', c)
def legal(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('legal.html', c)
def press(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('press.html', c)
def jobs(request):
	c = Context(defaultContext)
	c.update({
	})
	return render_to_response('jobs.html', c)
