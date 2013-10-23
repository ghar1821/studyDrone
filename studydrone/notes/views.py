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

from notes.models import Note, Membership, Group,Comment, NoteTag, SentMessage, Message, MaliciousReport ,Rating, Course
from accounts.models import User_Profile

from notes.forms import UploadNotesForm, UploadNotesTagsForm, EditNotesForm
from django.forms.formsets import formset_factory

from accounts.models import User_Profile

from django.template import RequestContext
from django.db.models import Q

import StringIO
import csv

#not a django view
def updateSessionPoints(request):
	request_user_profile = User_Profile.objects.get(User_associated=request.user)
	request.session['points'] = request_user_profile.Points


@login_required(login_url='/accounts/login')
def index(request):
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	try:
		messages=SentMessage.objects.filter(receiver=request.user.id).order_by('-id')	
	except:
		raise Http404
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('-id')	
	except:
		raise Http404
	return render(request,'notes/dashboard.html', {"groups":groups,"messages":messages, "notes":notes})

@login_required(login_url='/accounts/login')
def my_groups(request):
	try:
		groups=Group.objects.filter(members=request.user.id).order_by('-id')	
	except:
		raise Http404
	try:
		messages=SentMessage.objects.filter(receiver=request.user.id).order_by('-id')	
	except:
		raise Http404
	return render(request,'notes/my-groups.html', {"messages":messages, "groups":groups})


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

def search_groups_results(request):
	post_search_name = request.POST["search_name"]
	post_search_description = request.POST["search_description"]
	post_member_ids= request.POST.getlist("member_ids",False)
	
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
	errors = []
	try:
		users=User.objects.all()	
	except:
		raise Http404
	if request.POST:
		#something
		post_group_name = request.POST["group_name"]
		post_group_description = request.POST["group_description"]
		post_member_ids= request.POST.getlist("member_ids",False)
		if Group.objects.filter(name=post_group_name).exists():
			errors.append("Group already exists!")
			return render(request,'notes/create-group.html', {"users":users,"errors":errors})

		group = Group(name=post_group_name,description=post_group_description,creator=request.user)
		group.save()
		if post_member_ids:
			members = []
			for member_id in post_member_ids:
				member_inst = User.objects.get(pk=member_id)
				members.append(Membership(group=group,member=member_inst))
			for member in members:
				member.save()
		
		if not Membership.objects.filter(group=group,member=request.user).exists():
			membership = Membership(group=group,member=request.user)
			membership.save()
		return redirect('/notes/my-groups')
	return render(request,'notes/create-group.html', {"users":users})

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
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	try:
		notes=Note.objects.filter(uploader=request.user.id).order_by('id')
	except:
		raise Http404
	return render(request,'notes/my-notes.html',{"notes": notes,"groups":groups})

@login_required(login_url='/accounts/login')
def browse_notes(request):
	notes = Note.objects.filter(permission_public=True)
	return render(request,'notes/browse-notes.html', {"notes":notes})


def search_notes(request):
	return render(request,'notes/search-notes.html', {"foo":"bar"})

@login_required(login_url='/accounts/login')
def search_notes_results(request):
	return render(request,'notes/search-notes-results.html', {"foo":"bar"})
	
def edit_notes(request):
	return render(request,'notes/edit-notes.html', {"foo":"bar"})

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
		form.fields['extends'].queryset = Note.objects.filter(uploader=request.user)
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
# Download counter also here because why not
# Fix it one day
@login_required(login_url='/accounts/login')
def view_individual_notes(request):
	error = None

	#download note form
	# GOD THIS view looks so ugly someone find out a way how to redirect properly plz
	if request.method == 'POST':
		#post items
		download_note_id = request.POST.get('note-id')
		download_bool = request.POST.get('download-bool')
		#defined stuff
		note = Note.objects.get(pk=download_note_id)
		downloading_user_profile = User_Profile.objects.get(User_associated=request.user)

		if note and (download_bool == "True"):
			#check if downloading user has enough points
			if downloading_user_profile.Points >= note.download_cost:
				#subtract points from user

				downloading_user_points = downloading_user_profile.Points
				downloading_user_profile.Points = downloading_user_points - note.download_cost
				downloading_user_profile.save()
				#give points to uploading user
				uploading_user_profile = User_Profile.objects.get(User_associated=note.uploader)
				uploading_user_points = uploading_user_profile.Points
				uploading_user_points += 20 #downloading_points arbitarily set
				uploading_user_profile.Points = uploading_user_points
				uploading_user_profile.save()
				#updating download count
				download_count =note.download_count
				download_count += 1
				note.download_count = download_count 
				note.save()
				updateSessionPoints(request)
				return redirect(note.note_file.url)
			else:
				error = []
				error.append('Not enough points')

	#Processing new comment assumes that the user has permission
	if request.method == 'POST':
		comment_note_id = request.POST.get('note-id') #shares id with page rendering
		comment_message = request.POST.get('comment_new_message')

		if comment_note_id and comment_message:
			comment_note = Note.objects.get(pk=comment_note_id) # get note
			if comment_note:
				new_comment = Comment(given_by=request.user,Note=comment_note,comment_content=comment_message,submission_time=timezone.now())
				new_comment.save()
				#give points if the commenter is not uploader
				if request.user != comment_note.uploader:
					#give points to uploader
					uploading_user_profile = User_Profile.objects.get(User_associated=comment_note.uploader)
					uploading_user_points = uploading_user_profile.Points
					uploading_user_points += 2 #downloading_points arbitarily set
					uploading_user_profile.Points = uploading_user_points
					uploading_user_profile.save()
					#gve points to commenting user
					commenting_user = User_Profile.objects.get(User_associated=request.user)
					commenting_user_points = commenting_user.Points
					commenting_user.Points = commenting_user_points + 5
					commenting_user.save()
					updateSessionPoints(request)



	#Processing new rating assumes that user has permission to the note
	if request.method == 'POST':
		rating_note_id = request.POST.get('note-id')
		rating_note = request.POST.get('rating-value')

		if rating_note_id and rating_note:
			note = Note.objects.get(pk=rating_note_id)
			rating_for_note = None

			#check whther there was a previous rating
			try:
				rating_for_note = Rating.objects.get(Note=note)
			except:
				rating_for_note = Rating(given_by=request.user,Note=note,rate = 1,submission_time=timezone.now())
				#since new ratings give points .check if the rater is not the uploader
				if note.uploader != request.user:
					#give points to uploading user
					uploading_user_profile = User_Profile.objects.get(User_associated=note.uploader)
					uploading_user_points = uploading_user_profile.Points
					uploading_user_points += 5 #downloading_points arbitarily set
					uploading_user_profile.Points = uploading_user_points
					uploading_user_profile.save()
					#give points to rating user
					rating_user = User_Profile.objects.get(User_associated=request.user)
					rating_user_points = rating_user.Points
					rating_user.Points = rating_user_points + 5
					rating_user.save()
					updateSessionPoints(request)
			rating_for_note.rate = rating_note
			rating_for_note.save()

		


	#Rendering the page
	if request.method == 'POST':
		noteId = request.POST.get('note-id')

		note = None
		extendable = 'No'
		try:
			note=Note.objects.filter(uploader=request.user.id).get(pk=noteId)	
		except:
			try:
				note=Note.objects.filter(permission_public=True).get(pk=noteId)
			except:
				#user can belong to multiple groups
				#checks if the note belongs to one of the groups
				note=Note.objects.get(pk=noteId)
				members = note.permission_group.members
				if members:
					is_member = None
					try:
						is_member = members.objects.get(member=request.user)
					except:
						is_member = None
					if is_member:
						note=Note.objects.get(pk=noteId)
					else:
						note= None
				else:
					note = None

		if not note:
			raise Http404

		#comments
		try:
			comments=Comment.objects.filter(Note=noteId)	
		except:
			raise Http404
		#ratings
		ratings = Rating.objects.filter(Note=noteId)
		average_Rating = 0
		if ratings:
			for rating in ratings:
				average_Rating += int(rating.rate)

			average_Rating = average_Rating/len(ratings)

		#calculating points earned from note
		points_earned = 0
		#factor in download count
		points_earned = points_earned + note.download_count * 50
		#factor in comment count
		points_earned_comments = comments.exclude(given_by=note.uploader) 
		points_earned = points_earned + len(points_earned_comments)*2
		#factor in rating count
		points_earned_ratings = ratings.exclude(given_by=note.uploader)
		points_earned = points_earned + len(points_earned_ratings) * 5

		try:
			tags=NoteTag.objects.filter(note=noteId)	
		except:
			raise Http404

		#Tags we can access through notes
		
		username = request.user.id
		uploader = User.objects.get(username=note.uploader).id
		if username == uploader:
			# Note is extendable
			extendable = 'Yes'
		return render(request, 'notes/view-individual-notes.html', 
			{"note": note, "comments":comments, "tags":tags, "extendable": extendable,
			"username":username, "uploader":uploader,"rating":average_Rating,"error":error,"points_earned":points_earned})
	return Http404

def view_individual_user(request,user_id):
	try:
		user=User.objects.get(pk=user_id)
	except:
		raise Http404
	try:
		groups=Group.objects.filter(members=user.id)
	except:
		raise Http404
	try:
		if int(user_id) != request.user.id:
			notes=Note.objects.filter(uploader=user).exclude(permission_public=False).order_by('-id')
		else:
			notes=Note.objects.filter(uploader=user).order_by('-id')
	except:
		raise Http404
	try:
		profile=User_Profile.objects.get(User_associated=user)
	except:
		raise Http404
	
	return render(request, 'notes/view-individual-user.html', {"groups": groups, "notes":notes,"user":user,"profile":profile})
	
def view_individual_group(request,group_id):
	try:
		group=Group.objects.filter(members=request.user.id).get(pk=group_id)	
	except:
		raise Http404
	try:
		members=Membership.objects.filter(group=group)
	except:
		raise Http404
	
	profiles = []
	"""
	for memb in members:
		profiles.append(User_Profile.objects.filter(User_associated=memb.member))
	profiles = User_Profile.objects.filter(id__in=profiles)
	"""
	try:
		notes=Note.objects.filter(permission_group=group).order_by('-id')
	except:
		raise Http404
	return render(request, 'notes/view-individual-group.html', {"group": group,"notes":notes,"profiles":profiles})

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

@login_required(login_url='/accounts/login')
def edit_notes(request):
	note_id = request.POST.get('note-id')
	note = Note.objects.get(id=note_id)
	note_filedelete = Note.objects.get(id=note_id)
	

	if request.method=='POST':
		form = EditNotesForm(request.POST, request.FILES, instance=note)
		if form.is_valid():
			form.save()
			if form.cleaned_data["note_file"]:
				import os
				from django.conf import settings
				os.remove(os.path.join(settings.MEDIA_ROOT, str(note_filedelete.note_file)))
				
	else:
		form = EditNotesForm(instance=note, initial={"Description": note_filedelete.description, 
			"permission_public":note_filedelete.permission_public,
			"permission_group":note_filedelete.permission_group,})
	return render(request,'notes/edit-notes.html',{'form':form, 'note':note}, context_instance=RequestContext(request))


def relationship_request_sent(request):
	return render(request, 'notes/relationship-request-sent.html')

@login_required(login_url='/accounts/login')
def search_notes_by_tags(request):
	notes = None
	if request.method == 'POST':
		tag_id = request.POST.get('tag-id')
		note_from_notetag = NoteTag.objects.filter(tag=tag_id)
		note_ids = []
		for n in note_from_notetag:
			note_ids.append(n.note_id)
		notes = Note.objects.filter(id__in=note_ids)
	return render(request,'notes/search-notes-by-tags.html', {"notes":notes})

@login_required(login_url='/accounts/login')
def search_notes_by_tag(request):
	notes = None
	if request.method == 'POST':
		tag_id = request.POST.get('tag-id')
		note_from_notetag = NoteTag.objects.filter(tag=tag_id)
		note_ids = []
		for n in note_from_notetag:
			note_ids.append(n.note_id)
		notes = Note.objects.filter(id__in=note_ids)
	return render(request,'notes/search-notes-by-tag.html', {"notes":notes})

@login_required(login_url='/accounts/login')
def search_notes_by_subject(request):
	notes = None
	if request.method == 'POST':
		course_id = request.POST.get('course-id')
		course = Course.objects.get(pk=course_id)
		notes = Note.objects.filter(course=course)
		
	return render(request,'notes/search-notes-by-course.html', {"notes":notes})
