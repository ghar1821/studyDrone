# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
#for comment
from django.utils import timezone


from notes.models import Note, Membership, Group,Comment, NoteTag

def index(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/index.html', {"groups":groups})

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
		# if noteId:
		# 	# return redirect(view_notes,request=request)
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request, 'notes/view-notes.html',{"notes": notes})

def rate_notes(request):


	return redirect(request,'', {"foo":"bar"})

def new_comment(request):


	pass


# Due to inability to do redirecting properly will attempt to shove commenting and rating in one view
# Fix it one day
def view_individual_notes(request):
	#Processing new comment
	if request.method == 'POST':
		comment_note_id = request.POST.get('note-id') #shares id with page rendering
		comment_message = request.POST.get('comment_new_message')

		if comment_note_id and comment_message:
			comment_note=Note.objects.filter(uploader=request.user.id).get(pk=comment_note_id)
			if comment_note:
				new_comment = Comment(given_by=request.user,Note=comment_note,comment_content=comment_message,submission_time=timezone.now())
				new_comment.save()

	#Processing new rating

	#Rendering the page
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
	return Http404
def view_individual_group(request,group_id):
	try:
		group=Group.objects.filter(creator=request.user.id).get(pk=group_id)	
	except:
		raise Http404
	
	return render(request, 'notes/view-individual-group.html', {"group": group})
