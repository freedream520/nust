from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from account.forms import MyRegistrationForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
from notification.models import Notification

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/account/loggedin')
	else:
		return HttpResponseRedirect('/account/invalid')

def loggedin(request):
	n = Notification.objects.filter(user=request.user, viewed=False)
	return render_to_response('loggedin.html', {'full_name': request.user.username, 'notifications': n},)

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	return render_to_response('logout.html')
#TODO logout.html






def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/account/register_success')
		#TODO give tips when errors occur

	args = {}
	args.update(csrf(request))

	args['form'] = MyRegistrationForm()
	print args
	return render_to_response('register.html', args)

def register_success(request):
	return render_to_response('register_success.html')


class ContactWizard(SessionWizardView):
	template_name = "contact_form.html"

	def done(self, form_list, **kwargs):
		form_data = process_form_data(form_list)

		return render_to_response('done.html', {'form_data': form_data})

def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]

	# logr.debug(form_data[0]['subject'])
	# logr.debug(form_data[0]['sender'])
	# logr.debug(form_data[0]['message'])

	send_mail(form_data[0]['subject'],
			form_data[2]['message'],
			form_data[1]['sender'],
			['billgates@gmail.lol'],
			fail_silently=False,
			)

	return form_data