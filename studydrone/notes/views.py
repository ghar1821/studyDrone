# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

#from django.http import HttpResponse

#from polls.models import Choice, Poll

#def index(request):
#	return HttpResponse("Hello notes")

def index(request):
	return render(request,'notes/index.html', {"foo":"bar"})

def messages(request):
	return render(request,'notes/messages.html', {"foo":"bar"})

def view_groups(request):
	return render(request,'notes/view-groups.html', {"foo":"bar"})

def create_groups(request):
	return render(request,'notes/create-groups.html', {"foo":"bar"})

def upload_notes(request):
	return render(request,'notes/upload_notes.html', {"foo":"bar"})

def view_notes(request):
	return render(request, 'notes/view-notes.html',{"foo": "bar"})


def view_individual_notes(request):
	return render(request, 'notes/view-individual-notes.html', {"foo": "bar"})

