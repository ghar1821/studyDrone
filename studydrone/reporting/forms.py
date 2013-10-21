from django import forms
from django.contrib.auth.models import User
from reporting.models import MaliciousReport

import datetime

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
