from django.shortcuts import render_to_response, render
from chat.models import Article , Comment
from django.http import HttpResponse
from chat.forms import ArticleForm , CommentForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.utils import timezone
from django.conf import settings



def articles(request):
	language = 'zh-CN'
	session_language = 'zh-CN'

	if 'lang' in request.COOKIES:
		language = request.COOKIES['lang']

	if 'lang' in request.session:
		session_language = request.session['lang']
		
	args = {}
	args.update(csrf(request))

	args['articles'] = Article.objects.all()
	args['language'] = language   
	args['session_language'] = session_language 

	return render_to_response('articles.html', args) 

def article(request, article_id=1):   
	return render(request, 'article.html', 
				{'article': Article.objects.get(id=article_id) })

def language(request, language='en-gb'):
	response = HttpResponse("setting language to %s" % language)

	response.set_cookie('lang', language)

	request.session['lang'] = language

	return response


def create(request):
	if request.POST:
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			a = form.save()
		
			#messages.add_message(request, messages.SUCCESS, "You Article was added")
			
			return HttpResponseRedirect('/t/all')
	else:
		form = ArticleForm()

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('create_article.html', args)

def like_article(request, article_id):
	if article_id:
		a = Article.objects.get(id=article_id)
		count = a.likes
		count += 1
		a.likes = count
		a.save()
		return HttpResponseRedirect('/t/%s' % article_id)

def search_titles(request):
	if request.method == "POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''
		
	if search_text:
		articles = Article.objects.filter(title__contains=search_text)

	return render_to_response('ajax_search.html', {'articles': articles})

def add_comment(request, article_id):
	a = Article.objects.get(id=article_id)

	if request.method == "POST":
		f = CommentForm(request.POST)
		if f.is_valid():
			c = f.save(commit=False)
			c.pub_date = timezone.now()
			c.article = a
			c.save()

			#messages.success(request, "You Comment was added")

			return HttpResponseRedirect('/t/%s' % article_id)

	else:
		f = CommentForm()

	args = {}
	args.update(csrf(request))

	args['article'] = a
	args['form'] = f

	return render_to_response('add_comment.html', args)

def delete_comment(request, comment_id):
	c = Comment.objects.get(id=comment_id)

	article_id = c.article.id

	c.delete()

	#messages.add_message(request, settings.DELETE_MESSAGE, "Your comment was deleted")

	return HttpResponseRedirect("/t/%s" % article_id)

	