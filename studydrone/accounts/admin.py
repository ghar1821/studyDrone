from django.contrib import admin

from accounts.models import User_Profile

class User_ProfileAdmin(admin.ModelAdmin):
	list_display = ('User_associated','Unikey_validated','Unikey','Degree','Profile_picture','Points','Year_first_enrolled')
	
	
admin.site.register(User_Profile,User_ProfileAdmin)
