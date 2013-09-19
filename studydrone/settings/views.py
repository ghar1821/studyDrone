# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'settings/index.html'
#    context_object_name = 'latest_poll_list'

#    def get(self, request, *args, **kwargs):
#		return HttpResponse('Returning at IndexView.get()');

