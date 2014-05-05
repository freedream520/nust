from django.db import models
from django.forms import ModelForm

# Create your models here.
class User(models.Model):
	"""docstring for User"""
	name = models.CharField(max_length=20)

class UserProfile(models.Model):
	"""docstring for UserProfile"""
	birth_date = models.CharField(max_length=20)#models.DateField(blank=True, null=True)
		

class UserForm(ModelForm):
	class Meta:
		model = User  

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user']