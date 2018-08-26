from django import forms
from django.utils.translation import gettext_lazy as _

class InvitationForm(forms.Form):
	email = forms.CharField(widget=forms.TextInput(attrs={'size':
	32, 'placeholder': _('Email Address of Friend to invite.'),
	'class':'form-control'}))