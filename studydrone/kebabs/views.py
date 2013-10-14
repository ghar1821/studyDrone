# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from accounts.views import login as accounts_login

from kebabs.models import Order, Food_item, Order_item

@login_required(login_url='/accounts/login')
def index(request):
	return render(request, 'kebabs/index.html', {"foo": "bar"})

@login_required(login_url='/accounts/login')
def view_menu(request):
	food_items = Food_item.objects.all()	
	return render(request, 'kebabs/view-menu.html', {"food_items": food_items})
	
@login_required(login_url='/accounts/login')
def view_individual_order(request):

	order=Order.objects.get(id=1)	
	
	order_items= Order_item.objects.all()
	#=Order_item.objects.filter(ADDSOMETHING)
	
	return render(request, 'kebabs/view-individual-order.html', {"order" : order,"order_items" : order_items})

@login_required(login_url='/accounts/login')
def my_orders(request):
	"""		
	#I think you may need to add some sort of session context
	#This would allow you to have some shopping cart functionality
	#Retrieve the order
	tmp = request.session['cart']
	beefkebab = Food_item.objects.get(id=1)
	first = [beefkebab,1]	
	tmp.append(first)
	request.session['cart'] = tmp
	"""	
	# Get the orders associated with the user
	orderlist = Order.objects.filter(Order_creator=request.session['_auth_user_id'])
			
	return render(request, 'kebabs/my-orders.html', {"orderlist": orderlist})
	

