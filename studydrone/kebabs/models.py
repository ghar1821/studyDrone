from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.
 
class Order(models.Model):
    DELIVERY_POINTS = (
        ('Link', 'Link Building'),
        ('SIT', 'School of Information Technology'),
        ('Carslaw', 'Carlsaw Learning Lab'),
    )
    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('Mastercard', 'Mastercard'),
        ('Visa', 'Visa'),
	('Points','Points'),
	('Paypal','Paypal')
    )
    # Order table listing all orders
    Order_date = models.DateField(auto_now=False, auto_now_add=True)
    Delivery_time = models.TimeField(auto_now=False, auto_now_add=False)
    """ Order_creator need to be enabled once the account table is created """
    Order_creator = models.ForeignKey(User)
    # Maximum total cost be $9999
    Total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    Delivery_point = models.CharField(max_length=50, choices=DELIVERY_POINTS)
    Payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    Delivery_instruction = models.CharField(max_length=500,blank=True,default="")
    # Relationship
    def __unicode__(self):
        return self.Delivery_instruction

class Ingredient(models.Model):
    Name = models.CharField(max_length=50, unique=True)
    def __unicode__(self):
        return str(self.Name)




class Food_item(models.Model):
    # Food_item table listing the food item in menu
    Food_name = models.CharField(max_length=20, unique=True)
    Basic_ingredients = models.CharField(max_length=100)
    Dietary_information = models.CharField(max_length=200)
    Allergy_information = models.CharField(max_length=200)
    # Maximum price is $99
    Price = models.DecimalField(max_digits=4, decimal_places=2)
    Food_picture = models.ImageField(upload_to='food_pictures',blank=True)
    # Relationship
    orders = models.ManyToManyField(Order, through='Order_item')
    additional_ingredients = models.ManyToManyField(Ingredient, through='Food_Ingredient')
    def __unicode__(self):
	    return str(self.Food_name)

class Order_item(models.Model):
    food_item = models.ForeignKey(Food_item)
    order = models.ForeignKey(Order)
    Quantity = models.IntegerField()
    # Maximum cost is $999
    Cost = models.DecimalField(max_digits=5, decimal_places=2)

class Promotion(models.Model):
    # Promotion listing all food Promotion
    Promotion_title = models.CharField(max_length=50, unique=True)
    Promotion_picture = models.ImageField(upload_to='promotion_pictures',blank=True)
    # Maximum price is $999
    Price = models.DecimalField(max_digits=5, decimal_places=2)
    Start_date = models.DateField(auto_now=False, auto_now_add=False)
    End_date = models.DateField(auto_now=False, auto_now_add=False)
    # Many to many Relationship with food item

    #food_items = models.ManyToManyField(Food_item, through='Promotion_item')
    food_item = models.ForeignKey(Food_item)
    def __unicode__(self):
        return self.Promotion_title

class Promotion_item(models.Model):
    promotion = models.ForeignKey(Promotion)
    food_item = models.ForeignKey(Food_item)

class Food_Ingredient(models.Model):
    food_item = models.ForeignKey(Food_item)
    ingredient  = models.ForeignKey(Ingredient)

