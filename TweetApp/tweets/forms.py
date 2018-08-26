from django import forms
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class TweetForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,
														'cols': 85,
														'class':'form-control',
														'placeholder': 'Post a new Tweet'}),
												 max_length = 160)
	country = forms.CharField(widget=forms.HiddenInput())

class SearchForm(forms.Form):
	query  = forms.CharField(label='Enter a keyword to search for',
	widget = forms.TextInput(attrs={'size': 32, 'class':'form-control'}))

class LoginForm(forms.Form):

	username = forms.CharField(widget=forms.widgets.TextInput)
	password = forms.CharField(widget=forms.widgets.PasswordInput)

	class Meta:
		model = UserProfile
		fields = ['username', 'password']
