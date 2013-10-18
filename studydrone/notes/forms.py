from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from notes.models import Note

# Safe from injection, etc.
class UserRegistrationForm(UserCreationForm):
	title = forms.CharField(max_length=100, required=True)
	description = forms.CharField(max_length=200, required=True)
	format = forms.CharField(max_length=10, required=True)
	note_file = forms.FileField(upload_to = '/var/www/studydrone/studydrone/media/notes_files')
	
	
	
	class Meta:
		model = User
		fields = ('username','email','password1', 'password2','first_name','last_name','unikey','degree','Year_first_enrolled')

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.unikey = self.cleaned_data['unikey']
		user.degree = self.cleaned_data['degree']
		user.Year_first_enrolled = self.cleaned_data['Year_first_enrolled']
		if commit:
			user.save()

		return user

