from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GENTLE_CHOICES = (
	('M', 'Male'), 
	('F', 'Female'), 
	('S', 'Secret'), 
)

SCHOOL_CHOICE = (
	('DG', 'dianguang'),
	('JX', 'jixie'),
	('CS', 'jisuanji'),
	('ZD', 'zidonghua'),
)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	gentle = models.CharField(max_length=1, choices=GENTLE_CHOICES, blank=True, null=True)
	email = models.EmailField(max_length=100, blank=True, null=True)
	weibo = models.URLField(max_length=200, blank=True, null=True)
	school = models.CharField(max_length=50, choices=SCHOOL_CHOICE, blank=True, null=True)
	major = models.CharField(max_length=50, blank=True, null=True)
	qq = models.CharField(max_length=12, blank=True, null=True)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])