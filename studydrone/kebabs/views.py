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

from accounts.models import User_Profile

from kebabs.forms import OrderForm

#comment is free

@login_required(login_url='/accounts/login')
def index(request):
	promotion_items =  Promotion.objects.filter(Start_date__lte=timezone.now(),End_date__gte=timezone.now())

	return render(request, 'kebabs/index.html', {"promotion_items":promotion_items})

@login_required(login_url='/accounts/login')
def order_not_processed(request):
	return render(request, 'kebabs/order-not-processed.html')

@login_required(login_url='/accounts/login')
def submit_order(request):
	#business logic which puts everything into the tables
	if request.POST and request.session["cart"]:
		orderform = OrderForm(request.POST)
		if orderform.is_valid():
			order = orderform.save(commit=False)
			order.Total_cost=request.POST["Total_cost"]
			cost_in_points = float(order.Total_cost)*100
			order.Order_creator=request.user
			#check payment method
			if order.Payment_method == "Points":
				#Check whether user has enough points
				profile = User_Profile.objects.get(User_associated=request.user)
				if profile.Points >= cost_in_points:
					profile.Points = int(profile.Points-cost_in_points)
					profile.save()
					order.save()
					#Need to implement second half - storing food item - order relationships
					cart = request.session["cart"]
					for item in cart:
						#Add line to table
						order_item = Order_item(food_item=item[0],order=order,Quantity=item[1],Cost=(item[0].Price*item[1]))
						order_item.save()
					#Reset cart
					request.session["cart"] = []
					return render(request,'kebabs/order-confirmation.html', {"foo": "bar"})
				#redirect to checkout with error
				else:
					form = OrderForm()
					errors = []
					totalcost = 0
					cart = request.session["cart"]
					for item in cart:
						totalcost += item[0].Price*item[1]
					errors.append("Not enough points to complete transaction. Please select another payment option.")
					return render(request,'kebabs/get-details.html',{"errors":errors,"form":form,"totalcost":totalcost})
			else:
				order.save()
				#Need to implement second half - storing food item - order relationships
				cart = request.session["cart"]
				for item in cart:
					#Add line to table
					order_item = Order_item(food_item=item[0],order=order,Quantity=item[1],Cost=(item[0].Price*item[1]))
					order_item.save()
				#Reset cart
				request.session["cart"] = []
				return redirect('/kebabs/order-confirmation', {"foo": "bar"})
		else:
			cart = request.session['cart']		
			totalcost = 0
			for item in cart:
				totalcost += item[0].Price*item[1]
			
			return render(request,'kebabs/get-details.html', {"form" : orderform,"totalcost":totalcost})
	return redirect('/kebabs/order-not-processed', {"foo": "bar"})

@login_required(login_url='/accounts/login')
def order_confirmation(request):
	#business logic which puts everything into the tables
	return render(request, 'kebabs/order-confirmation.html', {"foo": "bar"})


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

	post_food_id = request.POST.get('food-id')
	post_quantity = int(request.POST.get('food-quantity'))

	if not(post_food_id	and post_quantity):
		raise Http404
	#Temporarily store the food item
	food = Food_item.objects.get(id=post_food_id)
	#Check if there's a promotion within the date with the same food id
	try:
		is_promotion = Promotion.objects.filter(food_item=food.id).filter(Start_date__lte=datetime.date.today,End_date__gte=datetime.date.today)[0]
	except:
		is_promotion = None
	#If there is a promotion
	if is_promotion:
		food.Price = is_promotion.Price

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

@login_required(login_url='/accounts/login')
def view_individual_order(request,order_id):
	try:
		#find a way to specify the order id
		order=Order.objects.filter(Order_creator=request.user.id).get(pk=order_id)	
	except:
		raise Http404

	#Need to find a way to restrict view

	#Find the related food items	
	order_items = Order_item.objects.filter(order=order)
	return render(request, 'kebabs/view-individual-order.html', {"order" : order,"order_items" : order_items})

@login_required(login_url='/accounts/login')
def my_orders(request):
	# Get the orders associated with the user
	orderlist = Order.objects.filter(Order_creator=request.session['_auth_user_id']).order_by('-id')
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
	form = OrderForm()
	cart = request.session['cart']		
	totalcost = 0
	for item in cart:
		totalcost += item[0].Price*item[1]
	return render(request, 'kebabs/get-details.html', {"totalcost":totalcost,"form":form})
