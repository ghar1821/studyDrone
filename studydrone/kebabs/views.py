# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.views import login as accounts_login

#from django.http import HttpResponse

@login_required(login_url='/accounts/login')
def index(request):
	return render(request, 'kebabs/index.html', {"foo": "bar"})

def view_menu(request):
	return render(request, 'kebabs/view-menu.html', {"foo": "bar"})
	
def view_individual_order(request):
	return render(request, 'kebabs/view-individual-order.html', {"foo": "bar"})
	
def my_orders(request):
	return render(request, 'kebabs/my-orders.html', {"foo": "bar"})
	

