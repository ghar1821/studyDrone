from django.contrib import admin
from kebabs.models import Order,Food_item, Order_item, Promotion, Promotion_item ,Ingredient ,Food_Ingredient

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','Order_date','Delivery_time','Order_creator','Total_cost','Delivery_point','Delivery_instruction')

class Order_itemAdmin(admin.ModelAdmin):
	list_display = ('food_item','order','Quantity','Cost')

class Food_itemAdmin(admin.ModelAdmin):
	list_display = ('id','Food_name','Basic_ingredients','Dietary_information','Allergy_information','Price')

class PromotionAdmin(admin.ModelAdmin):
	list_display = ('id','Promotion_title','Price','Start_date','End_date')

class Promotion_itemAdmin(admin.ModelAdmin):
	list_display = ('promotion','food_item')

class IngredientAdmin(admin.ModelAdmin):
	list_display = ('id','Name')

class Food_IngredientAdmin(admin.ModelAdmin):
	list_display = ('ingredient','food_item')


admin.site.register(Order,OrderAdmin)
admin.site.register(Order_item,Order_itemAdmin)
admin.site.register(Food_item,Food_itemAdmin)
admin.site.register(Promotion,PromotionAdmin)
admin.site.register(Promotion_item,Promotion_itemAdmin)
admin.site.register(Ingredient,IngredientAdmin)
admin.site.register(Food_Ingredient,Food_IngredientAdmin)
