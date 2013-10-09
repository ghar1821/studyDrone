# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

# Needed for templates
from django.template.loader import get_template
from django.template import Context, RequestContext

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

#def index(request):
#		return render(request, 'index.html')
def index(request):

	if request.user.is_authenticated():
		return redirect(settings)
	
	errors = []

	if request.method == 'POST':
	
		username = request.POST.get('username')
		if not username:
			errors.append('Enter a username')
		
		password = request.POST.get('password')
		if not password:
			errors.append('Enter a password')
		
		if username and password:
				# Get the right redirect variable
				user = authenticate(username=username, password=password)
				if user is not None and user.is_active:
					auth_login(request,user)
					#if for the redirect
					#Use a redirect for the below
					if request.POST.get('redirect') == 'kebabs':
						return redirect('/kebabs/')
					else:
						return redirect('/notes/')
				
				errors = []
				errors.append('Enter a correct username or password for a user')
				#return render_to_response('index.html', RequestContext(request))
	return render(request, 'index.html', {'errors' : errors})


@login_required
def needs_redirect(request):
	if request.user.is_authenticated():
		return render(request, 'needs_redirect.html')
	else:
		return redirect(index)

def dash(request):
	return render(request, 'dash.html', {"foo": "bar"})

def signup(request):
	return render(request, 'signup.html', {"foo": "bar"})

def logout(request):
	auth_logout(request)	
	return redirect(index)

@login_required
def settings(request):
	return render(request, 'settings.html', {"foo": "bar"})

@login_required
def delete_account(request):
	return render(request, 'delete-account.html', {"foo": "bar"})


"""
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Get the right redirect variable
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth_login(request,user)
			#if for the redirect
			#Use a redirect for the below
				return render(request,'needs_redirect.html')
			return render(request,'invalid_user.html')

	else:
		render(request,'index.html')

		# form = LoginForm();
		#return render(request,'signup.html')
"""


#    context_object_name = 'latest_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]

