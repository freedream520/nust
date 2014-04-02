from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse
from django.views import generic

from polls.models import Choice, Poll

def IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		"""Return the last five published polls."""
		return Poll.objects.order_by('-pub_date')[:5]


def DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

def ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'


def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': p, 'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
