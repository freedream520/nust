from django.db import models

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date = models.DateTimeField('date published')
	likes = models.IntegerField(default=0)
	#thumbnail = models.FileField(upload_to=get_upload_file_name)
	#approved = models.BooleanField(default=False)

    
	def __unicode__(self):
		return self.title