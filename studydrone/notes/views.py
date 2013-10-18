# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView


from notes.models import Note, Membership, Group

#from django.http import HttpResponse

#from polls.models import Choice, Poll

#def index(request):
#	return HttpResponse("Hello notes")

def index(request):
	return render(request,'notes/index.html', {"foo":"bar"})

def messages(request):
	return render(request,'notes/messages.html', {"foo":"bar"})

def view_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/view-groups.html', {"groups":groups})

def create_groups(request):
	return render(request,'notes/create-groups.html', {"foo":"bar"})

def upload_notes(request):
	return render(request,'notes/upload-notes.html', {"foo":"bar"})

def view_notes(request):
	try:
		notes=Note.objects.filter(uploader=request.user.id)	
	except:
		raise Http404
	return render(request, 'notes/view-notes.html',{"notes": notes})


def view_individual_notes(request,note_id):
	"""
	try:
		note=Note.objects.filter(uploader=request.user.id).get(pk=note_id)	
	except:
		raise Http404
	"""

	note =1
	return render(request, 'notes/view-individual-notes.html', {"note": note})

