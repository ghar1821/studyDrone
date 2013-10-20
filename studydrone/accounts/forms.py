from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Profile

import datetime

# Safe from injection, etc.
class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required = True)
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	
	class Meta:
		model = User
		fields = ('username','email','password1', 'password2','first_name','last_name',)

	def clean_email(self):
	    data = self.cleaned_data['email']
	    if User.objects.filter(email=data).exists():
	        raise forms.ValidationError("This email already used")
	    return data
	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.clean_email()
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		
		if commit:
			user.save()

		return user

class UserProfileRegistrationForm(forms.ModelForm):
	class Meta:
		model = User_Profile
		exclude = ('User_associated', 'Unikey_validated', 'Profile_picture', 'Points',)

	def __init__(self, *args, **kwargs):
		super(UserProfileRegistrationForm, self).__init__(*args, **kwargs)
		year = datetime.datetime.now().year
		year_choices = ( (x, str(x)) for x in range(1990,year+1) )
		self.fields['Year_first_enrolled'] = forms.ChoiceField(choices=year_choices)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = User_Profile
		exclude = ('User_associated', 'Unikey_validated', 'Profile_picture', 'Points','Unikey',)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')	