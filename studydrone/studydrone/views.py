# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from django.http import HttpResponse

#from polls.models import Choice, Poll


def home(request):
	return HttpResponse("Hello home base, you'll have a link to both apps")

#class IndexView(generic.ListView):
#    template_name = 'notes/index.html'
#    context_object_name = 'latest_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]

