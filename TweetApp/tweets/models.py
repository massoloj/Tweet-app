from django.db import models
from user_profile.models import UserProfile

class Tweet(models.Model):
	"""
	Tweet model
	"""
	user = models.ForeignKey(UserProfile)
	text = models.CharField(max_length=160)
	created_date = models.DateTimeField(auto_now_add=True)
	country = models.CharField(max_length=30)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.text

class HashTag(models.Model):
	"""
	HashTag model
	"""
	name = models.CharField(max_length=64, unique=True)
	tweet = models.ManyToManyField(Tweet)
	
	def __str__(self):
		return self.name

class UserFollower(models.Model):
	"""
	UserFollowers model
	"""
	user = models.OneToOneField(UserProfile)
	date = models.DateTimeField(auto_now_add=True)
	count = models.IntegerField(default=1)
	followers = models.ManyToManyField(UserProfile,
					related_name='followers')
	
	def __str__(self):
		return '%s, %s' % self.user, self.count