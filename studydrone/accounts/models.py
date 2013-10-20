from django.db import models
from django.contrib.auth.models import User

import os
from uuid import uuid4

# Create your models here.
class User_Profile(models.Model):

	def profile_picture_rename(path):

		# Rename the picture to random filename for extra security if no pk is found
		def wrapper(instance, filename):
			ext = filename.split('.')[-1]
			if instance.pk:
				filename = '{}.{}'.format(instance.pk, ext)
			else:
				# set filename as random string
				filename = '{}.{}'.format(uuid4.hex, ext)
			# return the whole path to the file
			return os.path.join(path, filename)
		return wrapper	
	# User associated
	User_associated = models.ForeignKey(User)
	# Validated unikey
	Unikey_validated = models.BooleanField()
	# Unikey
	Unikey = models.CharField(max_length=8, unique=True)
	# Degree
	Degree = models.CharField(max_length=100)
	# Profile picture
	Profile_picture = models.ImageField(upload_to=profile_picture_rename('images_profile/'),blank=True, null=True, default='images_profile/sampleAvatar.png')
	# Points
	Points = models.BigIntegerField(default=200)
	# Year first enrolled
	Year_first_enrolled = models.PositiveSmallIntegerField()

	


