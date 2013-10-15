# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login')
def index(request):
	return render(request, 'reporting/index.html', {"foo": "bar"})
