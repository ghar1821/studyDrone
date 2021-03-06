from django import forms
from django.contrib.auth.models import User

from notes.models import Message
from notes.models import MaliciousReport
# testing
# For uploading notes
from notes.models import Note, Tag, NoteTag

# Safe from injection, etc.
class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('title','body')
		exclude = ('message_time', 'sender')
	recipient = forms.CharField(max_length=100,required=True)

	def clean_recipient(self):
		post_recipient = self.clean_data['recipient']
		if not User.objects.filter(username=post_recipient).exists():
			raise forms.ValidationError("Username is not valid")
	def save(self, commit=True):
		self.clean_recipient()
		message = super(MessageForm, self).save(commit=False)
		message.title = self.cleaned_data['title']
		message.body = self.cleaned_data['body']
		if commit:
			message.save()

		return message

# Safe from injection, etc.
class ReportCreationForm(forms.ModelForm):
	class Meta:
		model = MaliciousReport
		fields = ('reported_by','note','report_content')

	def save(self, commit=True):
		malreport = super(ReportCreationForm, self).save(commit=False)
		malreport.reported_by = self.cleaned_data['reported_by']
		malreport.note = self.cleaned_data['note']
		malreport.report_content = self.cleaned_data['report_content']
		
		if commit:
			malreport.save()
		return malreport

# Uploading notes
class UploadNotesForm(forms.ModelForm):
	
	class Meta:
		model = Note
		fields = ('title', 'description', 'note_file','permission_public','tags','course','permission_group', 'extends')

	def update_tags(self):
		note = super(UploadNotesForm, self).save(commit=False)
		tags = self.cleaned_data.get('tags')
		for t in tags:
			tag = Tag.objects.get(tag=t)
			NoteTag.objects.create(tag=tag, note=note)

	def clean_title(self):
	    data = self.cleaned_data['title']
	    if Note.objects.filter(title=data).exists():
	        raise forms.ValidationError("This title is already in use!")
	    return data

	def save(self, commit=True):
		note = super(UploadNotesForm, self).save(commit=False)
		note.title = self.clean_title()
		
		noteFormat = self.cleaned_data['note_file'].name
		filenameList = noteFormat.split('.')

		if len(filenameList) == 1:
			note.format = 'None'
		else:
			note.format = filenameList.pop()
		if commit:
			note.save()
		return note
	

class UploadNotesTagsForm(forms.ModelForm):
	class Meta:
		model = NoteTag
		fields = ('note','tag')

class EditNotesForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ('description', 'note_file','permission_public','permission_group')
