# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView

# Needed for templates
from django.template.loader import get_template
from django.template import Context

from django.http import HttpResponse

#def home(request):
#	return HttpResponse("Hello home base, you'll have a link to both apps")

class IndexView(TemplateView):
    template_name = 'index.html'
	
#    context_object_name = 'latest_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.order_by('-pub_date')[:5]

