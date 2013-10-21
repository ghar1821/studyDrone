from django import forms
from django.contrib.auth.models import User

from notes.models import Message, MessageSent
from notes.models import MaliciousReport

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
