from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User_Profile

import datetime

# Added 20/10/2013 7:50 PM
from django.core.files.images import get_image_dimensions

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
		exclude = ('User_associated', 'Unikey_validated', 'Points','Unikey','Profile_picture',)

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		year = datetime.datetime.now().year
		year_choices = ( (x, str(x)) for x in range(1990,year+1) )
		self.fields['Year_first_enrolled'] = forms.ChoiceField(choices=year_choices)

	# def clean_profile_picture(self):
	# 	prof_pic = self.cleaned_data['Profile_picture']

	# 	if not prof_pic:
	# 		raise forms.ValidationError("No image!")
	# 	else:
	# 		width, height = get_image_dimensions(prof_pic)

	# 		# validate dimensions
	# 		max_width = max_height = 300

	# 		if width > max_width or height > max_height:
	# 			raise forms.ValidationError('Please use an image that is %i x %i pixels.' % (max_width, max_height))

	# 		# validate image type
	# 		main, sub = prof_pic.content_type.split('/')
	# 		if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
	# 			raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')

	# 		# validate image size
	# 		if len(prof_pic) > (70 * 1024):
	# 			raise forms.ValidationError('Profile picture file size may not exceed 70k')

		
	# 	return prof_pic

	# def save(self, commit=True):
	# 	profile = super(ProfileForm, self).save(commit=False)
	# 	profile.Profile_picture = self.clean_profile_picture()
	# 	profile.Degree = self.cleaned_data['Degree']
	# 	profile.Year_first_enrolled = self.cleaned_data['Year_first_enrolled']
		
	# 	if commit:
	# 		profile.save()

	# 	return profile

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name',)

class ProfilePictureForm(forms.ModelForm):
	class Meta:
		model = User_Profile
		fields = ('Profile_picture',)

	def clean_profile_picture(self):
		prof_pic = self.cleaned_data['Profile_picture']

		if not prof_pic:
			raise forms.ValidationError("No image!")
		else:
			width, height = get_image_dimensions(prof_pic)

			# validate dimensions
			max_width = max_height = 300

			if width > max_width or height > max_height:
				raise forms.ValidationError('Please use an image that is %i x %i pixels.' % (max_width, max_height))

			# validate image type
			main, sub = prof_pic.content_type.split('/')
			if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
				raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')

			# validate image size
			if len(prof_pic) > (70 * 1024):
				raise forms.ValidationError('Profile picture file size may not exceed 70k')

		
		return prof_pic

	def save(self, commit=True):
		profile_pic = super(ProfilePictureForm, self).save(commit=False)
		profile_pic.Profile_picture = self.clean_profile_picture()
		
		
		if commit:
			profile_pic.save()

		return profile_pic