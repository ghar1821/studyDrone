# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

#from django.http import HttpResponse

#from polls.models import Choice, Poll

class IndexView(TemplateView):
    template_name = 'kebabs/index.html'
#    context_object_name = 'latest_poll_list'

#    def get(self, request, *args, **kwargs):
#		return HttpResponse('Returning at Indexview.get()');
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]
