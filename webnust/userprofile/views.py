from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/account/login/')
def user_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/account/loggedin')
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm(instance=profile)

	args = {}
	args.update(csrf(request))

	args['form'] = form

	return render_to_response('profile.html', args)

def show_profile(request, user_id=1):   
	return render(request, 'show_profile.html', 
				{'profile': UserProfile.objects.get(id=user_id) })