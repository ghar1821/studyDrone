from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_Profile(models.Model):
	# User associated
	User_associated = models.ForeignKey(User)
	# Validated unikey
	Unikey_validated = models.BooleanField()
	# Unikey
	Unikey = models.CharField(max_length=8, unique=True)
	# Degree
	Degree = models.CharField(max_length=100)
	# Profile picture
	Profile_picture = models.FilePathField(default=None,blank=True)
	# Points
	Points = models.BigIntegerField()
	# Year first enrolled
	Year_first_enrolled = models.PositiveSmallIntegerField()
		


