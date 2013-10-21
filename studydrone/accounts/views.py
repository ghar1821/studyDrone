# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import auth
from accounts.forms import UserRegistrationForm
from accounts.forms import UserProfileRegistrationForm
from django.core.context_processors import csrf

# Added 16/10/2013 12:53 PM
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.core import urlresolvers

# Added 20/10/2013 1:55 PM
from accounts.forms import ProfileForm
from accounts.forms import UserForm
from django.contrib.auth.models import User
from accounts.models import User_Profile
from django.contrib.auth.views import password_change
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from PIL import Image as PImage
from os.path import join as pjoin

# Added 20/10/2013 10:27 PM
from accounts.forms import ProfilePictureForm


#Should this go to settings.html, or will there be another accounts home page?
@login_required(login_url='/accounts/login')
def index(request):
	return render(request, 'accounts/index.html', {"foo": "bar"})

def login(request):
	#Should we return a single login screen or an index, or something to register the user?
	return redirect('http://www.studydrone.com')

# @login_required
# def settings(request):
# 	return render(request, 'accounts/settings.html', {"foo": "bar"})

@login_required
def points_history(request):
	return render(request, 'accounts/points-history.html', {"foo": "bar"})

@login_required
def delete_account(request):
	return render(request, 'accounts/delete-account.html', {"foo": "bar"})

def register(request):
    if request.POST:
        userForm = UserRegistrationForm(request.POST, prefix="user_form")
        profileForm = UserProfileRegistrationForm(request.POST, prefix="profile_form")

        if userForm.is_valid() and profileForm.is_valid():
            new_user = userForm.save()
            new_profile = profileForm.save(commit=False)
            new_profile.User_associated = new_user
            new_profile.Unikey_validated = True
            new_profile.save()
            return HttpResponseRedirect('/accounts/register-success')
    else:
        userForm = UserRegistrationForm(prefix="user_form")
        profileForm = UserProfileRegistrationForm(prefix="profile_form")
   
    return render_to_response('accounts/signup.html', {"user_form": userForm, "profile_form": profileForm}, context_instance=RequestContext(request))

def register_success(request):
    return render_to_response('accounts/signup_success.html')

@sensitive_post_parameters()
@csrf_protect
@login_required
def edit_user(request, user_id):
    profile = User_Profile.objects.get(User_associated=user_id)
    user = User.objects.get(id=user_id)
    # img = None

    if request.method == "POST":  
        profileForm = ProfileForm(request.POST, instance=profile, prefix="profile_form")
        userForm = UserForm(request.POST, instance=user, prefix="user_form")
        # passwordForm = PasswordChangeForm(data=request.POST, user=request.user, prefix="password_form")
        if profileForm.is_valid() and userForm.is_valid():
            profileForm.save()
            userForm.save()
            # passwordForm.save()

    else:
        profileForm = ProfileForm(prefix="profile_form", instance=profile,
                initial={"Degree": profile.Degree,
                    "Year_first_enrolled": profile.Year_first_enrolled,})
        userForm = UserForm(prefix="user_form", instance=user,
            initial={'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name})
       
    return render_to_response("accounts/settings.html", 
        {"profile_form": profileForm, "user_form": userForm}, context_instance=RequestContext(request))

@sensitive_post_parameters()
@csrf_protect
@login_required
def edit_user_password(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        passwordForm = PasswordChangeForm(data=request.POST, user=request.user)
        if passwordForm.is_valid():
            passwordForm.save()
            return HttpResponseRedirect('/accounts/')

    else:
        passwordForm = PasswordChangeForm(user=request.user,prefix="password_form")

    return render_to_response("accounts/settings_password.html", {"form": passwordForm}, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def edit_user_picture(request, user_id):
    profile = User_Profile.objects.get(User_associated=user_id)
    img = None

    if request.method == "POST":
        if profile.Profile_picture:
                import os
                from django.conf import settings
                os.remove(os.path.join( settings.MEDIA_ROOT, str(profile.Profile_picture) ) )
        profilePictureForm = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if profilePictureForm.is_valid():
            profilePictureForm.save()
    else:
        profilePictureForm = ProfilePictureForm(instance=profile)

    if profile.Profile_picture:
        img = "/media/" + profile.Profile_picture.name
    return render_to_response("accounts/settings_profile_picture.html", {"form":profilePictureForm, "img":img}, context_instance=RequestContext(request))
