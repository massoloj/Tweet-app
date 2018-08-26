from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class UserProfile(AbstractBaseUser):
	"""
	Custom user class.
	"""
	username = models.CharField( 'username', max_length=10,
				unique=True, db_index=True)
	email = models.EmailField('email address', unique=True)
	joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'username'
	
	def __str__(self):
		return self.username

class Invitation(models.Model):
	name = models.CharField(maxlength=50)
	email = models.EmailField()
	code = models.CharField(maxlength=20)
	sender = models.ForeignKey(User)
	
	def __str__(self):
	return u'%s, %s' % (self.sender.username, self.email)