# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

# Needed for templates
from django.template.loader import get_template
from django.template import Context, RequestContext

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from accounts.models import User_Profile

def updateSessionPoints(request):
	request_user_profile = User_Profile.objects.get(User_associated=request.user)
	request.session['points'] = request_user_profile.Points



def index(request):

	if request.user.is_authenticated():
		return redirect('/accounts/')
	
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
										##points
					#check users last login and assign points
					difference = timezone.now() - user.last_login
					if difference.days > 0:
						request_user_profile = User_Profile.objects.get(User_associated=user)
						request_user_points = request_user_profile.Points
						request_user_profile.Points = request_user_points+150
						request_user_profile.save()

					auth_login(request,user)
					#Create a session variable for the shopping cart
					request.session['cart'] = []
					try: 
						points = User_Profile.objects.get(User_associated=user.id).Points
					except:
						raise Http404
					request.session['points'] = points
					profile_picture = User_Profile.objects.get(User_associated=user.id).Profile_picture
					request.session['profile_picture'] = profile_picture



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
	#Logout function clears the session data
	auth_logout(request)	
	return redirect(index)

def help(request):
	return render(request,'help.html', {"foo":"bar"})

def knowledge_base(request):
	return render(request,'knowledge-base.html', {"foo":"bar"})

def search_knowledge_base(request):
	return render(request,'search-knowledge-base.html', {"foo":"bar"})

def contact_us(request):
	return render(request,'contact-us.html', {"foo":"bar"})

#    context_object_name = 'latest_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]

