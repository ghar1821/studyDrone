# Create your views here.
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
#for comment
from django.utils import timezone

from django.contrib.auth.models import User

from notes.models import Note, Membership, Group,Comment, NoteTag, SentMessage, Message, MaliciousReport


from notes.forms import UploadNotesForm, UploadNotesTagsForm
from django.forms.formsets import formset_factory


@login_required(login_url='/accounts/login')
def index(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/index.html', {"groups":groups})

@login_required(login_url='/accounts/login')
def my_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	try:
		messages=SentMessage.objects.filter(receiver=request.user.id).order_by('-id')	
	except:
		raise Http404
	return render(request,'notes/my-groups.html', {"messages":messages, "groups":groups})

@login_required(login_url='/accounts/login')

def search_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	try:
		users=User.objects.all()	
	except:
		raise Http404
	return render(request,'notes/search-groups.html', {"groups":groups, "users":users})

@login_required(login_url='/accounts/login')
def search_groups_results(request):
	post_search_name = request.POST["search_name"]
	post_search_description = request.POST["search_description"]
	post_member_ids= request.POST.get("member_ids",False)
	
	try:
		results_groups = Group.objects.all()
	except:
		raise Http404

	if post_member_ids:
		results_groups = results_groups.filter(members__in=post_member_ids)
	if post_search_name:
		results_groups = results_groups.filter(name__icontains=post_search_name)
	if post_search_description:
		results_groups = results_groups.filter(description__icontains=post_search_description)

	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/search-groups-results.html', {"groups":groups,"results_groups":results_groups})

@login_required(login_url='/accounts/login')
def messages(request):
	try:
		messages=SentMessage.objects.filter(receiver=request.user.id).order_by('-id')	
	except:
		raise Http404

	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	return render(request,'notes/messages.html', {"messages":messages,"groups":groups})

@login_required(login_url='/accounts/login')
def send_message(request):
	if request.POST:
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

	return render(request,'notes/message-send-error.html')

@login_required(login_url='/accounts/login')
def delete_all_messages(request):
	#For all messages associated to the user id - delete them
	messages = SentMessage.objects.filter(receiver=request.user.id)	
	#Delete associated Sent Messages and Message
	#Deleting the message in Message deletes the SentMessage entry
	for i in messages:
		Message.objects.get(id=i.message.id).delete()
	return redirect('/notes/messages')

@login_required(login_url='/accounts/login')
def delete_message(request):
	#Delete associated Sent Message and Message
	message_id = request.POST["message_id"]
	Message.objects.get(id=message_id).delete()
	return redirect('/notes/messages')

@login_required(login_url='/accounts/login')
def create_group(request):
	return render(request,'notes/create-group.html', {"foo":"bar"})

@login_required(login_url='/accounts/login')
def delete_note(request):

	if request.method == 'POST':
		note_id = request.POST.get('note-id')		
		note = Note.objects.get(pk=note_id).delete()
		return redirect('/notes/my-notes')
	return redirect('/notes/my-notes')

@login_required(login_url='/accounts/login')
def leave_group(request):
	if request.POST:
		group_id = request.POST["group_id"]
		Membership.objects.filter(group=group_id).filter(member=request.user).delete()		
		return redirect('/notes/my-groups')

@login_required(login_url='/accounts/login')
def my_notes(request):
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request,'notes/my-notes.html',{"notes": notes})

@login_required(login_url='/accounts/login')
def browse_notes(request):
	notes = Note.objects.filter(permission_public=True)
	return render(request,'notes/browse-notes.html', {"notes":notes})

@login_required(login_url='/accounts/login')
def search_notes(request):
	return render(request,'notes/search-notes.html', {"foo":"bar"})

@login_required(login_url='/accounts/login')
def search_notes_results(request):
	return render(request,'notes/search-notes-results.html', {"foo":"bar"})

@login_required(login_url='/accounts/login')
def view_user(request,user_id):

	return render(request,'notes/view-user.html',{"user":user})

@login_required(login_url='/accounts/login')
def upload_notes(request):

	if request.method == 'POST':
		form = UploadNotesForm(request.POST, request.FILES)

		if form.is_valid():
			note = form.save(commit=False)
			note.uploader = request.user
			note.save()
			form.update_tags()
			return HttpResponseRedirect('/notes/my-notes')

	else:
		form = UploadNotesForm()
	return render(request,'notes/upload-notes.html', {"form":form})
	
@login_required(login_url='/accounts/login')
def view_notes(request):
		# if noteId:
		# 	# return redirect(view_notes,request=request)
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request, 'notes/view-notes.html',{"notes": notes})

@login_required(login_url='/accounts/login')
def rate_notes(request):
	return redirect(request,'', {"foo":"bar"})

# Due to inability to do redirecting properly will attempt to shove commenting and rating in one view
# Fix it one day
@login_required(login_url='/accounts/login')
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

		note = None
		try:
			note=Note.objects.filter(uploader=request.user.id).get(pk=noteId)	
		except:
			note=Note.objects.filter(permission_public=True).get(pk=noteId)

		if not note:
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

@login_required(login_url='/accounts/login')
def view_individual_group(request,group_id):
	try:
		group=Group.objects.filter(creator=request.user.id).get(pk=group_id)	
	except:
		raise Http404
	
	return render(request, 'notes/view-individual-group.html', {"group": group})

@login_required(login_url='/accounts/login')
def create_report(request):
	if request.POST:
		post_note = request.POST["note_id"]
		post_note = Note.objects.get(id=request.POST["note_id"])		
		post_report_content = request.POST["report_content"]
		
		malreport = MaliciousReport(reported_by=request.user,note=post_note,report_content=post_report_content)
		malreport.save()
		return redirect('/notes/report-submitted')
	"""
		malreport = ReportCreationForm(request.POST)
		if malreport.is_valid():
			malreport.save()
			return redirect('/notes/report-submitted')
	return redirect('/notes/')
	"""

@login_required(login_url='/accounts/login')
def report_submitted(request):
	return render(request, 'notes/report-submitted.html')
