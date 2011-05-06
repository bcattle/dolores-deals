from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.forms import UserCreationForm

#def login(request):
#	c = { }
#	return render_to_response('login.html', c, context_instance=RequestContext(request))
def register(request, template_name='register.html'):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect('')
	else:
		form = UserCreationForm()
		c = { 
			'form': form, 
		}
	return render_to_response(template_name, c, context_instance=RequestContext(request))

def verify(request, template_name='verify.html'):
	c = { }
	return render_to_response(template_name, c, context_instance=RequestContext(request))

def profile(request, template_name='profile.html'):
	c = { }
	return render_to_response(template_name, c, context_instance=RequestContext(request))
	