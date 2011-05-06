from django.template import RequestContext
from django.shortcuts import render_to_response

def login(request):
	c = { }
	return render_to_response('login.html', c, context_instance=RequestContext(request))
def verify(request):
	c = { }
	return render_to_response('verify.html', c, context_instance=RequestContext(request))
