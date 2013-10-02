from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models

# bulk 1 ###############################################
class Course(models.Model):
	# unit od study code
	code = models.CharField(max_length = 8, unique = True)
	title = models.CharField(max_length = 50)
	# typically 6
	credit_pt = models.IntegerField(default = 6)
	description = models.CharField(max_length = 200)
	# semester choices are s1 or s2
	s1 = 'S1'
	s2 = 'S2'
	OFFERED_SEM_CHOICES = (
		(s1, 'Semester 1'),
		(s2, 'Semester 2'),
	)
	sem = models.CharField(max_length = 2, choices = OFFERED_SEM_CHOICES, default = s1)
# many to many mapping for student enrollments in units
class Enrollment(models.Model):
	unit = models.ForeignKey('Course')
	student  = models.ForeignKey(User)

# Bulk 2 ###############################################

class Note(models.Model):
	download_count = models.IntegerField(default = 0)
	# for point tracking
	download_cost = models.IntegerField(default = 1)
	title = models.CharField(max_length = 100)
	description = models.CharField(max_length = 200)
	format = models.CharField(max_length = 10)
	# files are stored in the passed url 
	note_file = models.FileField(upload_to = '/var/www/studydrone/studydrone/media/notes_files')
	upload_time = models.DateTimeField(auto_now_add = True, blank = False)
	# this is tricky, if null accessed by all, otherwise exclusive to the group
	Permission = models.ForeignKey('Group', null = True)
	uploader = models.ForeignKey(User)
	# points to another note in the table
	extends = models.ForeignKey('Note', null = True)

class Tag(models.Model):
	tag = models.CharField(max_length = 20)

# many to many mapping for tags used on notes
class NoteTag(models.Model):
	note = models.ForeignKey('Note')
	tag = models.ForeignKey('Tag')

# Bulk 3 ###############################################

# Rating notes
class Rating(models.Model):
	given_by = models.ForeignKey(User)
	Note = models.ForeignKey('Note')
	# rating 1 to 5 stars
	rate = models.IntegerField(
		validators = [MaxValueValidator(5), MinValueValidator(1)],
		null = False)
	submission_time = models.DateTimeField(auto_now_add = True, blank = False)

# commenting on notes
class Comment(models.Model):
	given_by = models.ForeignKey(User)
	Note = models.ForeignKey('Note')
	comment_content = models.CharField(max_length = 300, null = False)
	submission_time = models.DateTimeField(auto_now_add = True, blank = False)

# reporting notes
class MaliciousReport(models.Model):
	reported_by = models.ForeignKey(User)
	Note = models.ForeignKey('Note')
	report_content = models.CharField(max_length = 300, null = False)
	submission_time = models.DateTimeField(auto_now_add = True, blank = False)

# Bulk 4 ###############################################

class Group(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	description = models.CharField(max_length = 200)
	created_since = models.DateTimeField(auto_now_add = True, blank = False)
	creator = models.ForeignKey(User)

# many to many mapping of groups and users
class Membership(models.Model):
	member = models.ForeignKey(User)
	group = models.ForeignKey('Group')

# Bulk 5 ###############################################

# reporting bugs or other
class Enhancement(models.Model):
	description = models.CharField(max_length = 300)
	reported_by = models.ForeignKey(User)
	report_time = models.DateTimeField(auto_now_add = True, blank = False)
	b = 'bug'
	s = 'suggestion'
	ENHANCEMENT_TYPES = (
		(b, 'bug'),
		(s, 'suggestion'),
	)
	report_type = models.CharField(max_length = 1, choices = ENHANCEMENT_TYPES, default = b)

# Bulk 6 ###############################################

# mailing component
class Message(models.Model):
	title = models.CharField(max_length = 50)
	body = models.CharField(max_length = 500)
	message_time = models.DateTimeField(auto_now_add = True, blank = False)
	sender = models.ForeignKey(User)

class Attachement(models.Model):
	file_attached = models.FileField(upload_to = '/var/www/studydrone/studydrone/media/messages_attachment')

# 3 way mapping for attachments, recipients and messages 
class SentMessage(models.Model):
	message = models.ForeignKey('Message')
	receiver = models.ForeignKey(User)
	attachement = models.ForeignKey('Attachement')
	
# END OF NOTES #########################################
