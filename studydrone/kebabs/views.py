# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.views import login as accounts_login

from kebabs.models import Order

@login_required(login_url='/accounts/login')
def index(request):
	return render(request, 'kebabs/index.html', {"foo": "bar"})

@login_required(login_url='/accounts/login')
def view_menu(request):
	return render(request, 'kebabs/view-menu.html', {"foo": "bar"})
	
@login_required(login_url='/accounts/login')
def view_individual_order(request):
	return render(request, 'kebabs/view-individual-order.html', {"foo": "bar"})

@login_required(login_url='/accounts/login')
def my_orders(request):
	# Get the orders associated with the user
	orderlist = Order.objects.filter(Order_creator=request.session['_auth_user_id'])
	
	return render(request, 'kebabs/my-orders.html', {"orderlist": orderlist})
	

