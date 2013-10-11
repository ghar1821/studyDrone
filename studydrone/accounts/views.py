# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render_to_response, redirect

from django.contrib.auth.decorators import login_required

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
def delete_account(request):
	return render(request, 'accounts/delete-account.html', {"foo": "bar"})
