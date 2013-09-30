# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

#from django.http import HttpResponse

#from polls.models import Choice, Poll

#def index(request):
#	return HttpResponse("Hello notes")

class IndexView(TemplateView):
    template_name = 'notes/index.html'

def view_individual_note(request):
	# get username

	# return username
	return render(request, 'notes/notes_view.html', {"username": "gjoh3342"})
	
#    context_object_name = 'latest_poll_list'

#    def get(self, request, *args, **kwargs):
#		return HttpResponse('Returning at IndexView.get()');

