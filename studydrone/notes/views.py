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

from notes.models import Note, Membership, Group,Comment, NoteTag, SentMessage, Message, MaliciousReport ,Rating, Course, Tag
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
def send_message_group(request):
	if request.POST:
		#validate input user
		post_recipient = request.POST["recipient"]
		group = Group.objects.get(pk=post_recipient)
		members = Membership.objects.filter(group=group)
		for m in members:
			if (User.objects.filter(pk=m.member.id).exists()):
				#Extract information
				recipient = User.objects.get(pk=m.member.id)
				post_title = '<Group ' + str(group.name) + '> ' + request.POST["title"]
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
	try:
		groups=Group.objects.filter(members=request.user.id)	
	except:
		raise Http404
	try:
		notes = Note.objects.filter(permission_public=True)
	except:
		raise Http404
	return render(request,'notes/browse-notes.html', {"notes":notes,"groups":groups})


# being edited
@login_required(login_url='/accounts/login')
def search_notes(request):
	notes = Note.objects.all()
	return render(request,'notes/search-notes.html', {"notes":notes})

#being edited
@login_required(login_url='/accounts/login')
def search_notes_results(request):
	post_search_author = request.POST["search-author"]
	
	post_search_include_tags = request.POST["search-include"]
	if post_search_include_tags > 0:
		post_search_include_tags.split()
		[x.strip() for x in post_search_include_tags]
	
	post_search_exclude_tags = request.POST["search-exclude"]
	if post_search_exclude_tags:
		post_search_exclude_tags.split()
		[x.strip() for x in post_search_exclude_tags]
	
	post_search_rating =  int(request.POST["search-rating"])

	post_search_date = int(request.POST["search-date"])
	
	#try:
	#results_notes = []
	#Note, Membership, Group,Comment, NoteTag, SentMessage, Message, MaliciousReport ,Rating
		# results_notes = Note.objects.filter(Q(uploader=User_author) | Q(tag__in=post_search_include_tags))#.exclude(tag__in=post_search_exclude_tags))
		#rating >= 1,2,3,4,5,
		#today(timestamp) - upload_time (less than: week, month, 6months, year)
	group = Group.objects.all()
	user_group = []
	for g in group:
		user_group.append(int(g.group_id))
	#author only
	if (post_search_author and not post_search_include_tags and not post_search_exclude_tags):
		results_notes = Note.objects.filter(Q(uploader_id = User_author) & 
			(Q(permission_public = True) | Q(permission_group__in = user_group) | 
				Q(uploader = request.user)))

	#tags to include only
	#elif (not post_search_author and post_search_include_tags and not post_search_exclude_tags):
	#	results_notes = Note.objects.filter(Q(tags__in = post_search_include_tags) & (Q(permission_public = True) | Q(permission_group__in = user_group) | Q(uploader = int(request.user)))
	#tags to exclude only
	# elif (not post_search_author and not post_search_include_tags and post_search_exclude_tags):	
	# 	results_notes = Note.objects.exclude(Q(tags__in = post_search_exclude_tags)).filter(
	# 		Q(permission_public = True) | Q(permission_group__in = user_group) | 
	# 			Q(uploader = request.user))
	# #author and tags to include only
	# elif (post_search_author and post_search_include_tags and not post_search_exclude_tags):	
	# 	results_notes = Note.objects.filter(Q(uploader = User_author) & 
	# 		Q(tags__in = post_search_include_tags) & (Q(permission_public = True) |
	# 			Q(permission_group__in = user_group) | Q(uploader = request.user)))
	# #author and tags to exclude only
	# elif (post_search_author and post_search_include_tags and not post_search_exclude_tags):	
	# 	results_notes = Note.objects.filter(Q(uploader = User_author) & 
	# 		(Q(permission_public = True) | Q(permission_group__in = user_group) | 
	# 			Q(uploader = request.user))).exclude(Q(tags__in = post_search_exclude_tags))
	# #tags to include and exclude only
	# elif (not post_search_author and post_search_include_tags and post_search_exclude_tags):	
	# 	results_notes = Note.objects.filter(Q(tags__in = post_search_include_tags) &
	# 		(Q(permission_public = True) | Q(permission_group__in = user_group) | 
	# 			Q(uploader = request.user))).exclude(Q(tags__in = post_search_exclude_tags))
	# #author and tags to include and tags to exclude
	elif (post_search_author and post_search_include_tags and post_search_exclude_tags):
		User_author = User.objects.get(username=post_search_author)	
	 	results_notes = Note.objects.filter(Q(uploader = User_author) & 
	 		Q(tags__in = post_search_include_tags) & (Q(permission_public = True) | Q(permission_group__in = user_group) | 
	 			Q(uploader = request.User))).exclude(Q(tags__in = post_search_exclude_tags))
	
	else:
		return redirect('/notes/search-notes')
			
	#except:
	#	raise Http404

	#if post_search_include_tags:
	#	results_notes = results_notes.filter(??check?? = post_search_include_tags)
 	#if post_search_exclude_tags:
	#	results_notes = results_notes.filter(??check?? != post_search_exclude_tags)
	# if post_search_author:
	# 	results_notes = results_notes.filter(??check?? = post_search_author)
 
	return render(request,'notes/search-notes-results.html', {"results_notes":results_notes})

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

			##points
			#give user points for uploading notes
			request_user_profile = User_Profile.objects.get(User_associated=request.user)
			request_user_points = request_user_profile.Points
			request_user_profile.Points = request_user_points+150
			request_user_profile.save()

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
				##points
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
					##points
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
					##points
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
	return redirect('/notes/')

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
		members=Membership.objects.filter(group=group).values_list('member')
	except:
		raise Http404
	
	profiles = User_Profile.objects.filter(User_associated__in=members)
	
	try:
		notes=Note.objects.filter(permission_group=group).order_by('-id')
	except:
		raise Http404

	group_title = '<Group '+ group.name + '>'
	messages_initial = Message.objects.filter(title__startswith=group_title)
	messages = messages_initial.distinct('title')
	"""
	list_of_messages_id = []
	for m in messages_initial:
		list_of_messages_id.append(m.id)
	
	for m in messages_initial:
		for inner_m in messages_initial:
			if m.id != inner_m.id and m.title == inner_m.title:
				list_of_messages_id.remove(inner_m.id)
	
	messages = Message.objects.filter(id__in=list_of_messages_id)
	"""
	return render(request, 'notes/view-individual-group.html', {"group": group,"notes":notes,"profiles":profiles, "messages":messages})

@login_required(login_url='/accounts/login')
def create_report(request):
	if request.POST:
		post_note = request.POST["note_id"]
		post_note = Note.objects.get(id=request.POST["note_id"])		
		post_report_content = request.POST["report_content"]
		
		malreport = MaliciousReport(reported_by=request.user,note=post_note,report_content=post_report_content)
		malreport.save()
		##points
		#give user points
		request_user_profile = User_Profile.objects.get(User_associated=request.user)
		request_user_points = request_user_profile.Points
		request_user_profile.Points = request_user_points+1
		request_user_profile.save()

		updateSessionPoints(request)

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
			if(note.note_file != note_filedelete.note_file):
			
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
		group = Membership.objects.filter(member=request.user)
		user_group = []
		for g in group:
			user_group.append(g.group.id)

		notes = Note.objects.filter(Q(id__in=note_ids) & (
			Q(permission_public=True) | Q(uploader=request.user) | 
				Q(permission_group__in=user_group) ))
		note_tag = Tag.objects.get(pk=tag_id)
	return render(request,'notes/search-notes-by-tags.html', {"notes":notes ,"note_tag":note_tag})

@login_required(login_url='/accounts/login')
def search_notes_by_tag(request):
	notes = None
	if request.method == 'POST':
		tag_id = request.POST.get('tag-id')
		note_from_notetag = NoteTag.objects.filter(tag=tag_id)
		note_ids = []
		for n in note_from_notetag:
			note_ids.append(n.note_id)
		group = Membership.objects.filter(member=request.user)
		user_group = []
		for g in group:
			user_group.append(g.group.id)

		notes = Note.objects.filter(Q(id__in=note_ids) & (
			Q(permission_public=True) | Q(uploader=request.user) | 
				Q(permission_group__in=user_group) ))
		note_tag = Tag.objects.get(pk=tag_id)
	return render(request,'notes/search-notes-by-tag.html', {"notes":notes, "note_tag":note_tag})

@login_required(login_url='/accounts/login')
def search_notes_by_subject(request):
	notes = None
	if request.method == 'POST':
		course_id = request.POST.get('course-id')
		course = Course.objects.get(pk=course_id)
		notes = Note.objects.filter(course=course)
		
	return render(request,'notes/search-notes-by-course.html', {"notes":notes})

@login_required(login_url='/accounts/login')
def delete_member(request):
	post_member_id = request.POST.get('member_id')	
	post_group_id = request.POST.get('group_id')	
	Membership.objects.get(group=post_group_id,member=post_member_id).delete()
	return redirect('/notes/view-individual-group/'+post_group_id)

@login_required(login_url='/accounts/login')
def delete_group(request):
	post_group_id = request.POST.get('group_id')	
	Group.objects.get(id=post_group_id).delete()
	return redirect('/notes/my-groups/')
