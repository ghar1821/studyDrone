# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView


from notes.models import Note, Membership, Group,Comment, NoteTag

def index(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/index.html', {"groups":groups})

def my_groups(request):
	return render(request,'notes/my-groups.html', {"foo":"bar"})
def messages(request):
	return render(request,'notes/messages.html', {"foo":"bar"})
def create_group(request):
	return render(request,'notes/create-group.html', {"foo":"bar"})

def view_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/view-groups.html', {"groups":groups})


def my_notes(request):
	return render(request,'notes/my-notes.html', {"foo":"bar"})
def browse_notes(request):
	return render(request,'notes/browse-notes.html', {"foo":"bar"})
def search_notes(request):
	return render(request,'notes/search-notes.html', {"foo":"bar"})
def search_notes_results(request):
	return render(request,'notes/search-notes-results.html', {"foo":"bar"})
def upload_notes(request):
	return render(request,'notes/upload-notes.html', {"foo":"bar"})
	
def view_notes(request):


		# if noteId:
		# 	# return redirect(view_notes,request=request)

	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request, 'notes/view-notes.html',{"notes": notes})

def rate_notes(request):
	return redirect(request,'', {"foo":"bar"})


def view_individual_notes(request):
	if request.method == 'POST':
		noteId = request.POST.get('note-id')
			


		try:
			note=Note.objects.filter(uploader=request.user.id).get(pk=noteId)	
		except:
			raise Http404
		
		try:
			comments=Comment.objects.filter(Note=noteId)	
		except:
			raise Http404

		try:
			tags=NoteTag.objects.filter(note=noteId)	
		except:
			raise Http404

		#Tags we can access through notes
		return render(request, 'notes/view-individual-notes.html', {"note": note, "comments":comments, "tags":tags})

def view_individual_group(request,group_id):
	try:
		group=Group.objects.filter(creator=request.user.id).get(pk=group_id)	
	except:
		raise Http404
	
	return render(request, 'notes/view-individual-group.html', {"group": group})
