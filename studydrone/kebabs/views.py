# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

from accounts.views import login as accounts_login

from kebabs.models import Order, Food_item, Order_item ,Promotion

#comment is free

@login_required(login_url='/accounts/login')
def index(request):
	promotion_items =  Promotion.objects.filter(Start_date__lte=timezone.now(),End_date__gte=timezone.now())

	return render(request, 'kebabs/index.html', {"promotion_items":promotion_items})

@login_required(login_url='/accounts/login')
def submit_order(request):
	#business logic which puts everything into the tables
	
	return redirect('/kebabs/view-confirmation', {"foo": "bar"})

@login_required(login_url='/accounts/login')
def view_confirmation(request):
	#business logic which puts everything into the tables
	
	return render(request, 'kebabs/view-confirmation.html', {"foo": "bar"})


@login_required(login_url='/accounts/login')
def view_menu(request):
	current_promotion_items =  Promotion.objects.filter(Start_date__lte=timezone.now(),End_date__gte=timezone.now())
	food_items_notpromotion = Food_item.objects.exclude(promotion__isnull=False,promotion__Start_date__lte=timezone.now(),promotion__End_date__gte=datetime.date.today) 
	return render(request, 'kebabs/view-menu.html', {"food_items": food_items_notpromotion,"promotion_items":current_promotion_items})
	
@login_required(login_url='/accounts/login')
def add_menu_item(request):
	#Retrieve the order
	tmp = request.session['cart']



	#Post items returned
	post_menuPage =  int(request.POST.get('menu-origin'))
	post_price = request.POST.get('note-id')
	post_food_id = request.POST.get('food-id')
	post_quantity = int(request.POST.get('food-quantity'))


	#Temporarily store the food item
	food = Food_item.objects.get(id=post_food_id)
	#Check if there's a promotion within the date with the same food id
	is_promotion = Promotion.objects.filter(food_item=food.id).filter(Start_date__lte=datetime.date.today,End_date__gte=datetime.date.today)
	
	#If there is a promotion
	if is_promotion:
		food.Price = post_price

	#Attach the food, quantity pair
	food_quantity_pair = [food,post_quantity]

	#Apped the pair to the cart
	tmp.append(food_quantity_pair)
	
	#Store the cart variable
	request.session['cart'] = tmp
	
	#Redirect back to the menu
	if post_menuPage == 1:
		return redirect('http://www.studydrone.com/kebabs/view-menu')
	elif post_menuPage == 0:
		return redirect('/kebabs/')
"""
@login_required(login_url='/accounts/login')
def add_promotion_item(request):
	
	#I think you may need to add some sort of session context
	#This would allow you to have some shopping cart functionality
	#Retrieve the order
	tmp = request.session['cart']
	beefkebab = Food_item.objects.get(id=1)
	first = [beefkebab,1]	
	tmp.append(first)
	request.session['cart'] = tmp
	return redirect('http://www.studydrone.com/kebabs/view-menu')
"""

@login_required(login_url='/accounts/login')
def view_individual_order(request,order_id):
	try:
		#find a way to specify the order id
		order=Order.objects.filter(Order_creator=request.user.id).get(pk=order_id)	
	except:
		raise Http404

	#Need to find a way to restrict view

	#Find the related food items	
	food_items = Order_item.objects.filter(order=order)

	#This is temporary
	order_items = food_items
	return render(request, 'kebabs/view-individual-order.html', {"order" : order,"order_items" : order_items})

@login_required(login_url='/accounts/login')
def my_orders(request):
	# Get the orders associated with the user
	orderlist = Order.objects.filter(Order_creator=request.session['_auth_user_id'])
	cart = request.session['cart']		
	
	totalcost = 0
	for item in cart:
		totalcost += item[0].Price*item[1]
	
	return render(request, 'kebabs/my-orders.html', {"orderlist": orderlist, "totalcost":totalcost})
	

@login_required(login_url='/accounts/login')
def view_cart(request):
	cart = request.session['cart']		
	totalcost = 0
	for item in cart:
		totalcost += item[0].Price*item[1]
	return render(request, 'kebabs/view-cart.html', {"totalcost":totalcost})

@login_required(login_url='/accounts/login')
def empty_cart(request):
	request.session['cart'] = []
	return redirect('http://www.studydrone.com/kebabs/my-orders')

@login_required(login_url='/accounts/login')
def get_details(request):
	cart = request.session['cart']		
	totalcost = 0
	for item in cart:
		totalcost += item[0].Price*item[1]
	return render(request, 'kebabs/get-details.html', {"totalcost":totalcost})
