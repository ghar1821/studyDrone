# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import auth
# from accounts.forms import UserRegistrationForm
from django.core.context_processors import csrf

# Added 16/10/2013 12:53 PM
# from django.contrib.auth.forms import UserCreationForm
# from django.template import RequestContext
# from django.shortcuts import render_to_response,get_object_or_404
# from django.core import urlresolvers

# Added 17/10/2013 9:55 AM
from accounts.models import User_Profile
from django.contrib.auth.models import User
from accounts.forms import UserRegistrationForm, UserProfileRegistrationForm


#Should this go to settings.html, or will there be another accounts home page?
def index(request):
	return render(request, 'accounts/index.html', {"foo": "bar"})

def login(request):
	#Should we return a single login screen or an index, or something to register the user?
	return redirect('http://www.studydrone.com')

@login_required
def settings(request):
	return render(request, 'accounts/settings.html', {"foo": "bar"})

@login_required
def points_history(request):
	return render(request, 'accounts/points-history.html', {"foo": "bar"})

@login_required
def delete_account(request):
	return render(request, 'accounts/delete-account.html', {"foo": "bar"})

def register(request):
    if request.method == 'POST':
        userForm = UserRegistrationForm(request.POST,prefix="user_form" )
        profileForm = UserProfileRegistrationForm(request.POST, prefix="profile_form")
        if userForm.is_valid() and profile_form.is_valid():
            new_user = userForm.save()
            new_profile = profileForm.save(commit=False)
            new_profile.User_associated = new_user
            new_profile.save()
        return HttpResponseRedirect('/accounts/register-success')
    else:
        userForm = UserRegistrationForm(prefix="user_form")
        profileForm = UserProfileRegistrationForm(prefix="profile_form")
    return render_to_response('accounts/signup.html', {'user_form': userForm, 'profile_form': profileForm})


# def register(request):
#     if request.POST:
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/accounts/register-success')
#     else:
#         form = UserRegistrationForm()
#     args = {}
#     # prevent forgery
#     args.update(csrf(request))

#     # empty form
#     args['form'] = form
#     return render_to_response('accounts/signup.html', args)

def register_success(request):
    return render_to_response('accounts/signup_success.html')

