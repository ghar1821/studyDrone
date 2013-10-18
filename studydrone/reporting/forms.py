from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Profile

import datetime

# Safe from injection, etc.
class ReportCreationForm(UserCreationForm):
	note = forms.CharField(max_length=50, required=True)
	description = forms.CharField(max_length=200, required=True)
	
	class Meta:
		model = User
		fields = ('username','email','password1', 'password2','first_name','last_name',)

	def save(self, commit=True):
		user = super(ReportCreationForm, self).save(commit=False)
		user.email = self.clean_email()
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		
		if commit:
			user.save()

		return user
