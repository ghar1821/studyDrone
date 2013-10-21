# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView
#for comment
from django.utils import timezone

from django.contrib.auth.models import User

from notes.models import Note, Membership, Group,Comment, NoteTag, SentMessage, Message

def index(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/index.html', {"groups":groups})

def my_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/my-groups.html', {"groups":groups})
def messages(request):
	try:
		messages=SentMessage.objects.filter(receiver=request.user.id)	
	except:
		raise Http404

	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/messages.html', {"messages":messages,"groups":groups})

def send_message(request):
	#validate input user
	post_recipient = request.POST["recipient"]
	if (User.objects.filter(username=post_recipient).exists()):
		#Extract information
		recipient = User.objects.get(username=post_recipient)
		post_title = request.POST["title"]
		post_message = request.POST["message"]
		
		#Insert message into Message and SentMessage table
		temp_message = Message(title=post_title,body=post_message,sender=request.user)
		temp_message.save()
		
		temp_sentmessage = SentMessage(message=temp_message,receiver=recipient)
		temp_sentmessage.save()
		return redirect('/notes/messages')
	else:
		return render(request,'notes/message-send-error.html')

def delete_all_messages(request):
	#For all messages associated to the user id - delete them
	messages = SentMessage.objects.filter(receiver=request.user.id)	
	#Delete associated Sent Messages and Message
	#Deleting the message in Message deletes the SentMessage entry
	for i in messages:
		Message.objects.get(id=i.message.id).delete()
	return redirect('/notes/messages')

def delete_message(request):
	#Delete associated Sent Message and Message
	message_id = request.POST["message_id"]
	Message.objects.get(id=message_id).delete()
	return redirect('/notes/messages')

def create_group(request):
	return render(request,'notes/create-group.html', {"foo":"bar"})

def delete_note(request):

	if request.method == 'POST':
		note_id = request.POST.get('note-id')		
		note = Note.objects.get(pk=note_id).delete()
		return redirect('/notes/my-notes')
	return redirect('/notes/my-notes')

def my_notes(request):
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request,'notes/my-notes.html',{"notes": notes})

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
