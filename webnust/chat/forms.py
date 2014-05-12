from django import forms
from models import Article, Comment

class ArticleForm(forms.ModelForm):  

	class Meta:
		model = Article
		fields = ('title', 'body', 'thumbnail')

class CommentForm(forms.ModelForm):
    
	class Meta:
		model = Comment
		fields = ('body', 'thumbnail')


