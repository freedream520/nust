from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

global USERNAME_LEN_MIN
USERNAME_LEN_MIN = 3
global USERNAME_LEN_MAX
USERNAME_LEN_MAX = 20
global PASSWORD_LEN_MIN
PASSWORD_LEN_MIN = 8
global PASSWORD_LEN_MAX
PASSWORD_LEN_MAX = 160

class SignupForm(forms.Form):
	"""Form for signing up"""
	username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input username'}))
	password = forms.CharField(max_length=160, widget=forms.PasswordInput(attrs={'class': 'input password'}))
	confirm = forms.CharField(max_length=160, widget=forms.PasswordInput(attrs={'class': 'input password confirm'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input email'}))

	def clean(self):
		"""Validates the submitted data in addition to the built-in functions"""
		cleaned_data = self.cleaned_data
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		confirm = cleaned_data.get('confirm')
		#email = cleaned_data.get('username')
		errors = []
		if User.objects.filter(username=username).count():
			errors.append(forms.ValidationError('Username is taken', code='username_exists'))
		if len(username) < USERNAME_LEN_MIN or len(username) > USERNAME_LEN_MAX:
			errors.append(forms.ValidationError('Invalid username', code='invalid_username'))
		if len(password) < PASSWORD_LEN_MIN or len(password) > PASSWORD_LEN_MAX:
			errors.append(forms.ValidationError('Invalid password', code='invalid_password'))
		if password != confirm:
			errors.append(forms.ValidationError('Passwords don\'t match', code='password_mismatch'))
		if errors:
			raise ValidationError(errors)
		return cleaned_data

class LoginForm(forms.Form):
	"""Form for logging in"""
	username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input username'}))
	password = forms.CharField(max_length=160, widget=forms.PasswordInput(attrs={'class': 'input password'}))