from django.db import models

from notes.models import Note
from django.contrib.auth.models import User

# Create your models here.
# reporting notes
class MaliciousReport(models.Model):
	reported_by = models.ForeignKey(User)
	note = models.ForeignKey(Note)
	report_content = models.CharField(max_length = 300, null = False)
	submission_time = models.DateTimeField(auto_now_add = True, blank = False)

