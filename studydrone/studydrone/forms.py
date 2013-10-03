from django import forms
from django.forms import CharField, Form, PasswordInput


class SignInForm(forms.Form):
		email = forms.EmailField(required=True)
		password = forms.CharField(Widget=forms.PasswordInput())
