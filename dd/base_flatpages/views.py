# Create your views here.
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
