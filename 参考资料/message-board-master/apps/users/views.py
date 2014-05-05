from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render

from users.forms import LoginForm, SignupForm
from users.models import UserMessage


def users_index(request):
	"""Renders the users index page"""
	return render(request, 'users/index.html', {'title': 'Index', 'users': User.objects.filter()})


def users_signup(request):
	"""Renders the signup page, processes submitted data, and 
	creates a new user or displays errors if the inputs don't
	meet the requirements"""
	if request.user.is_authenticated():
		return redirect('/users/welcome?src=signup-redir')
	messages = []
	if request.method == 'POST':
		signup_form = SignupForm(request.POST)
		if signup_form.is_valid():
			try:
				username = signup_form.cleaned_data.get('username')
				password = signup_form.cleaned_data.get('password')
				email = signup_form.cleaned_data.get('email')
				user = User.objects.create_user(
							username=username,
							email=email,
							password=password
						)
				if user:
					auth_user = authenticate(username=username, password=password)
					if auth_user is not None:
						login(request, auth_user)
						return redirect('/users/welcome?src=signup')
					else:
						# Shouldn't happen
						messages.append('Password cannot contain non-ASCII characters')
				else:
					messages.append('User could not be created')
			except IntegrityError:
				# THis shoudln't happen
				messages.append('User already exists')
	else:
		signup_form = SignupForm()
	return render(request, 'users/signup.html', 
			{
				'title': 'Signup', 
				'form': signup_form,
				'messages': messages
			})


def users_login(request):
	"""Renders the user login page"""
	if request.user.is_authenticated():
		return redirect('/users/welcome?src=login-redir')
	message = '';
	login_form = None
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = authenticate(username=login_form.cleaned_data.get('username'), 
								password=login_form.cleaned_data.get('password'))
			if user is not None:
				if user.is_active:
					login(request, user)
					next_page = request.POST.get('next', False)
					if next_page:
						return redirect(next_page)
					else:
						return redirect('/users/welcome?src=login')
				else:
					message = 'Account disabled'
			else:
				message = 'Invalid login'
	else:
		login_form = LoginForm()
	next_page = request.GET.get('next', False)
	return render(request, 'users/login.html', 
			{
				'message': message, 
				'title': 'Login',
				'form': login_form,
				'next': next_page if next_page else ''
			})


def users_welcome(request):
	"""Renders the users welcome page"""
	if not request.user.is_authenticated():
		return redirect('login/?next=%s' % request.path)
	return HttpResponse('welcome %s' % request.user.username)


def users_profile(request, username=''):
	"""Renders a specified users profile page"""
	if not username:
		username = request.user.username
	user = None
	messages = None
	if User.objects.filter(username=username).count() > 0:
		user = User.objects.get(username=username)
		if request.method == 'POST' and request.user.is_authenticated():
			UserMessage.objects.create(
						content=request.POST.get('content', ''),
						user_to=user,
						user_from=request.user
					)
		messages = UserMessage.objects.filter(user_to=user)
	else:
		return redirect('/users')
	return render(request, 'users/profile.html', 
			{
				'title': '%s\'s profile' % username,
				'user': user,
				'logged_in': request.user.is_authenticated(),
				'current_user': request.user,
				'user_messages': messages
			})


def users_logout(request):
	"""Logs out the current user, if there is a session"""
	if not request.user.is_authenticated():
		return redirect('/users')
	logout(request)
	return redirect('/users')

