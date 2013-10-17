from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Profile

# Safe from injection, etc.
class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required = True)
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	
	class Meta:
		model = User
		fields = ('username','email','password1', 'password2','first_name','last_name',)

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		
		if commit:
			user.save()

		return user

class UserProfileRegistrationForm(forms.ModelForm):
	class Meta:
		model = User_Profile
		exclude = ('User_associated', 'Unikey_validated', 'Profile_picture', 'Points',)

# class UserProfileRegistrationForm(forms.Form):
# 	unikey = forms.CharField(max_length=8, required=True)
# 	degree = forms.CharField(max_length=100)
# 	Year_first_enrolled = forms.ChoiceField(choices=[(x,x) for x in range(2000, 2013)])

# 	class Meta:
# 		model = User_Profile
# 		fields = ('unikey','degree','Year_first_enrolled',)

# 	def save(self, commit=True):
# 		user = super(UserProfileRegistrationForm, self).save(commit=False)
# 		user.unikey = self.cleaned_data['unikey']
# 		user.degree = self.cleaned_data['degree']
# 		user.Year_first_enrolled = self.cleaned_data['Year_first_enrolled']

# 		if commit:
# 			user.save()

# 		return user